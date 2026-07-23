# Safe SQL Runner

Консольное приложение на Python для безопасного выполнения SQL-запросов к PostgreSQL.

## Возможности

- подключение к PostgreSQL через `.env`;
- выполнение только `SELECT`-запросов;
- автоматическое добавление `LIMIT 5`, если он отсутствует;
- обработка ошибок;
- вывод результатов в табличном виде.

## Требования

- Python 3.10+
- PostgreSQL

## Установка

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте файл `.env` по примеру `.env.example`.

Пример:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
```

## Запуск

```bash
python main.py
```

После запуска введите SQL-запрос.

Например:

```sql
SELECT * FROM students;
```

Если LIMIT отсутствует, программа автоматически выполнит:

```sql
SELECT * FROM students LIMIT 5;
```

Если попытаться выполнить:

```sql
DELETE FROM students;
```

будет выведено сообщение:

```
Ошибка: допускаются только SELECT-запросы.
```