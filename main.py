from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlalchemy import create_engine, cast, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

import csv

import json

from models import CsvFile, Base


# подруб алхимии
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwe45asd46@localhost/coords"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# сессия работы с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# экземпляр класса FastAPI и статика
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_upload_page() -> FileResponse:
    """Стартовая страничка приложения"""
    return FileResponse("static/upload.html")


@app.post("/api/routes")
async def upload_routes_file(file_format: str, file: UploadFile = File(...),
                             db: Session = Depends(get_db)) -> dict:
    """Функция на загрузку и сохранение в БД с точками маршрута"""

    try:
        # проверка, что это действительно csv (есть на фронте, но на всякий еще)
        if file_format.lower() != "csv":
            raise HTTPException(status_code=400,
                                detail="Only CSV format is supported")

        contents = await file.read()
        contents = contents.decode("utf-8")

        csv_lines = contents.strip().split('\n')
        # не > 100 строчек
        # иначе кол-во маршрутов будет стремиться к бесконечности
        if len(csv_lines) > 101:
            raise HTTPException(status_code=400,
                                detail="CSV file should "
                                       "have no more than 101 lines")

        # Создаем список для хранения данных из столбцов lng и lat
        lng_lat_data = []

        # Парсим содержимое CSV файла
        csv_data = csv.reader(contents.splitlines())
        for row in csv_data:
            if row[1] == "lat" or row[2] == 'lng':
                continue
            lng = row[1]  # Индекс 1 для столбца lng
            lat = row[2]  # Индекс 2 для столбца lat
            lng_lat_data.append((lng, lat))

        # Создаем объект CsvFile с данными lng и lat
        csv_file = CsvFile(filename=file.filename)
        # по сути, по тз нужны только точки
        csv_file.set_content(lng_lat_data)

        db.add(csv_file)
        db.commit()

        # сохраняем в бд лучший маршрут
        best_route = csv_file.get_ans_json()
        csv_file.best_route = json.dumps(best_route)
        db.commit()

        return {"status": best_route}

    except Exception as e:
        return {"status": "false", "error": f"{e}"}


@app.get("/api/routes/{route_id}")
async def get_optimal_route(route_id: int,
                            db: Session = Depends(get_db)) -> dict:
    """Получение оптимального маршрута по его id"""

    # Получаем объект CsvFile из базы данных по его id
    csv_file = db.query(CsvFile).filter(
        CsvFile.id == cast(route_id, Integer)).first()

    # Проверяем, найден ли маршрут с указанным ID
    if not csv_file:
        raise HTTPException(status_code=404, detail="Route not found")

    # Преобразуем поле best_route из JSON-строки обратно в словарь
    best_route = json.loads(csv_file.best_route)

    return best_route


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
