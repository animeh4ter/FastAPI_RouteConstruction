from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

import csv

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

        # Добавляем объект в сессию базы данных и сохраняем изменения
        db.add(csv_file)
        db.commit()

        return {"status": "true"}

    except Exception as e:
        return {"status": "false", "error": f"{e}"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
