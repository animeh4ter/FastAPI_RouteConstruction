import unittest
from server.models import CsvFile


class TestCsvFile(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр класса CsvFile для тестирования
        self.csv_file = CsvFile()

    def test_route_construction(self):
        # Подготавливаем небольшие входные данные
        content = [[55.75222, 37.61556], [48.85341, 2.3488],
                   [51.50939, -0.11832]]
        self.csv_file.set_content(content)

        # вызываем тестируемый метод
        route_list = self.csv_file._route_construction()

        # проверяем, что результат не пустой
        self.assertIsNotNone(route_list)

        # проверяем, что результат содержит ожидаемое количество точек
        expected_num_points = len(content)
        self.assertEqual(len(route_list), expected_num_points)

        # проверяем структуру каждой точки
        for point in route_list:
            self.assertIn('lat', point)
            self.assertIn('lng', point)
            self.assertIsInstance(point['lat'], float)
            self.assertIsInstance(point['lng'], float)


if __name__ == '__main__':
    unittest.main()
