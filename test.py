from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CsvFile, Base  # Замени это на импорт своей модели
import numpy as np
from pprint import pprint
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing


# Создай соединение с базой данных
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwe45asd46@localhost/coords"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создай сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Выполни запрос на извлечение последнего элемента
last_element = session.query(CsvFile).order_by(CsvFile.id.desc()).first()

a = last_element
res = a.get_content()

from python_tsp.distances import great_circle_distance_matrix

sources = np.array(res)
distance_matrix = great_circle_distance_matrix(sources)

permutation, distance = solve_tsp_simulated_annealing(distance_matrix)

print(permutation)
for i in permutation:
       print(res[i])

