from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

import numpy as np
from scipy.spatial import distance

import json
import re

Base = declarative_base()


class CsvFile(Base):
    """Модель csv файла"""
    __tablename__ = 'csv_files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)

    def set_content(self, content):
        """Запись списка"""
        self.content = json.dumps(content)

    def get_content(self):
        """Получение списка"""
        loaded_json = json.loads(self.content) if self.content else []
        float_data = [[float(item) for item in sublist]
                      for sublist in loaded_json]
        return float_data

    def route_construction(self):
        """Нужен алгоритм Литтла?"""
        pass
