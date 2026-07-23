import os
import re

import psycopg2
from dotenv import load_dotenv


DEFAULT_LIMIT = 5


def connect_db():
    load_dotenv()

    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
    except Exception as error:
        print(f"Не удалось подключиться к базе данных:\n{error}")
        return None


def validate_query(query: str) -> bool:
    query = query.strip().rstrip(";")

    if ";" in query:
        return False

    return query.lower().startswith("select")


def prepare_query(query: str) -> str:
    query = query.strip().rstrip(";")

    if re.search(r"\blimit\s+\d+\s*$", query, re.IGNORECASE):
        return query

    return f"{query} LIMIT {DEFAULT_LIMIT}"


def print_result(cursor):
    rows = cursor.fetchall()

    if not rows:
        print("Запрос выполнен. Данные отсутствуют.")
        return

    headers = [column[0] for column in cursor.description]

    widths = []

    for index in range(len(headers)):
        width = len(headers[index])

        for row in rows:
            width = max(width, len(str(row[index])))

        widths.append(width)

    header_line = " | ".join(
        headers[i].ljust(widths[i]) for i in range(len(headers))
    )

    print(header_line)
    print("-" * len(header_line))

    for row in rows:
        print(
            " | ".join(
                str(row[i]).ljust(widths[i]) for i in range(len(row))
            )
        )


def execute_query(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            print_result(cursor)

    except Exception as error:
        connection.rollback()
        print(f"Ошибка выполнения SQL:\n{error}")


def main():
    connection = connect_db()

    if connection is None:
        return

    try:
        sql = input("Введите SQL-запрос: ")

        if not validate_query(sql):
            print("Ошибка: допускаются только SELECT-запросы.")
            return

        sql = prepare_query(sql)

        print(f"\nВыполняется:\n{sql}\n")

        execute_query(connection, sql)

    except KeyboardInterrupt:
        print("\nРабота программы остановлена.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
