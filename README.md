
🔥 FastAPI приложение для расчёта оптимального маршрута

**POST /api/routes** - создание маршрута

**GET /api/routes/{id}** - получение маршрута по id

В endpoint POST /api/routes?format=csv загружается csv файл с точками маршрута: пример файла:

[example.csv](https://drive.google.com/file/d/1L1xoLdFR_h7eOsBoVDewp2SnoSVyWeAX/view?usp=sharing)

Первая точка в массиве является стартом маршрута.

Из переданных точек составляется оптимальный маршрут и возвращается в следующем виде:

[Untitled](https://imgur.com/a/RkZTN5P)

В endpoint-е GET /api/routes/{id} запрашивается раннее созданный оптимальный маршрут, виде ответа как в endpoint-е POST /api/routes?format=csv (картинка выше)
