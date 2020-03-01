# Интернет магазин

## Методы REST API
Должны быть реализованые следующие методы:
* добавить новый товар;
* редактировать товар по `id`;
* удалить товар по `id`;
* получить определенный товар по `id`;
* получить полный список товаров.

Swagger схема находится на http://127.0.0.1:8081/swagger

## Товар
Описание товара состоит из:
- названия;
- уникального кода (`id`)
- категории число или название

## Запуск
Для запуска требуется собрать докер образ и запустить через `docker-compose`

```
cd shop-systems
docker build -t shop:latest . && docker-compose up
```