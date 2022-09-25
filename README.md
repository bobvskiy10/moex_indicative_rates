# Moex indicative rates application

## Установка

Для работы проекта нужны все зависимости из `requirments.txt`.
Для этого можно прописать в терминале (с поддержкой `make`):
```
make venv
```
Эта команада создаст виртуальное окружение со всеми зависимостями.\
Либо вы можете установить все зависимости на свой `python`.

## Запуск
### 1) Вариант с `make`
Для запуска с утилитой `make` введите в терминале:
```
make run
```
### 2) Альтернатива
Если вы создали виртуальное окружение, то сперва активируйте его.
Для Linux:
```
./.venv/bin/activate
```
Для Windows:
```
.\.venv\Scripts\activate
```
Затем введите:
```
python -m moex_rates
```
Для выхода из виртуально окружения введите:
```
deactivate
```

## Удаление venv
Чтобы удалить виртуальное окружение с помощью `make` введите:
```
make clean
```

---
Спасибо за прочтение!