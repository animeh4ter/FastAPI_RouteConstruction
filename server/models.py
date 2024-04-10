from typing import Union

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.heuristics import solve_tsp_simulated_annealing

import numpy as np
from scipy.spatial import distance

import json

Base = declarative_base()


class CsvFile(Base):
    """Модель csv файла"""
    __tablename__ = "csv_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    best_route = Column(Text)

    def set_content(self, content:  list[Union[tuple[str, str], list[float]]]):
        """Запись списка координат"""
        self.content = json.dumps(content)

    def _get_content(self):
        """Получение списка координат"""
        loaded_json = json.loads(self.content) if self.content else []
        float_data = [[float(item) for item in sublist]
                      for sublist in loaded_json]
        return float_data

    def _route_construction(self):
        """
        https://pypi.org/project/python_tsp/
        solve_tsp_simulated_annealing работает намного быстрее, НО менее точно,
        поэтому пренебрегаем точностью на больших масштабах

        p.s. Для файла example.csv с ~34000 координат кол-во маршрутов стремится
        к бесконечности
        """

        coords_list = self._get_content()

        sources = np.array(coords_list)
        # перегоняем в матрицу расстояний координаты
        distance_matrix = great_circle_distance_matrix(sources)

        # дистанция не важна, важны только сами перестановки? т.е. путь
        permutation, _ = solve_tsp_simulated_annealing(distance_matrix)

        route_list = [{"lat": coords_list[i][0], "lng": coords_list[i][1]}
                      for i in permutation]
        return route_list

    def get_ans_json(self):
        try:
            best_route = self._route_construction()
            self.best_route = best_route

            json_data = {
                "id": self.id,
                "points": best_route
            }

            return json_data
        except Exception as e:
            return {'error': e}
