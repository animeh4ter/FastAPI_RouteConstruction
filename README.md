
🔥 FastAPI приложение для расчёта оптимального маршрута

**POST /api/routes** - создание маршрута

**GET /api/routes/{id}** - получение маршрута по id

В endpoint POST /api/routes?format=csv загружается csv файл с точками маршрута: пример файла:

[example.csv](https://prod-files-secure.s3.us-west-2.amazonaws.com/56b261ac-032c-4a60-9a87-b00f64f920b2/bf3bdbfa-3a09-425a-b881-3006c5d84b14/example.csv)

Первая точка в массиве является стартом маршрута.

Из переданных точек составляется оптимальный маршрут и возвращается в следующем виде:

[Untitled](https://imgur.com/a/RkZTN5P)

В endpoint-е GET /api/routes/{id} запрашивается раннее созданный оптимальный маршрут, виде ответа как в endpoint-е POST /api/routes?format=csv
