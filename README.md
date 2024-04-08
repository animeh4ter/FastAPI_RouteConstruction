
🔥 FastAPI приложение для расчёта оптимального маршрута

**POST /api/routes** - создание маршрута

**GET /api/routes/{id}** - получение маршрута по id

В endpoint POST /api/routes?format=csv загружается csv файл с точками маршрута: пример файла:

[example.csv](https://prod-files-secure.s3.us-west-2.amazonaws.com/56b261ac-032c-4a60-9a87-b00f64f920b2/bf3bdbfa-3a09-425a-b881-3006c5d84b14/example.csv)

Первая точка в массиве является стартом маршрута.

Из переданных точек составляется оптимальный маршрут и возвращается в следующем виде:

[Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/56b261ac-032c-4a60-9a87-b00f64f920b2/e6477720-a387-4bff-86cf-08cfa77763d1/Untitled.png)

В endpoint-е GET /api/routes/{id} запрашивается раннее созданный оптимальный маршрут, должен возвращаться ответ в следующем виде:

[Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/56b261ac-032c-4a60-9a87-b00f64f920b2/0b7feef4-039e-4db7-9109-ee09fdef8935/Untitled.png)
