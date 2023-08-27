import psycopg2

from psycopg2.errors import UniqueViolation
from src.config import config


class DBManager:

    def __init__(self, database_name):
        self.params = config()
        self.params.update({'dbname': database_name})
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = '''
        SELECT company_name, COUNT(*) AS amount_vacancies
        FROM hh_table
        GROUP BY company_name;
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        query = '''
        SELECT * FROM hh_table;
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        query = '''
        SELECT
            (SELECT ROUND(AVG(vacancy_salary_from)) FROM hh_table WHERE  vacancy_salary_from <> 0)AS avg_salary_from,
            (SELECT ROUND(AVG(vacancy_salary_to)) FROM hh_table WHERE  vacancy_salary_to <> 0)AS avg_salary_to;
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        query = '''
        SELECT * FROM  hh_table
        where vacancy_salary_from >
            (SELECT ROUND(AVG(vacancy_salary_from)) FROM hh_table WHERE  vacancy_salary_from <> 0)
        AND vacancy_salary_to >
            (SELECT ROUND(AVG(vacancy_salary_to)) FROM hh_table WHERE  vacancy_salary_to <> 0)
        ORDER BY vacancy_salary_from DESC, vacancy_salary_to DESC;
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        query = '''
        SELECT *
        FROM  hh_table
        WHERE LOWER(vacancy_name) ILIKE %s;
        '''
        self.cursor.execute(query, (f'%{keyword}%',))
        result = self.cursor.fetchall()
        return result

    def insert_vacancies(self, **kwargs):
        """
        Добавляем вакансию в БД
        """
        query = '''
            INSERT INTO hh_table (company_name, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_currency,
                           vacancy_url)
            VALUES (%s,%s,%s,%s,%s,%s);
            '''
        params = list(kwargs.values())
        self.cursor.execute(query, params)



    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        return self.conn.close()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS hh_table
        (
            id SERIAL PRIMARY KEY,
            company_name VARCHAR(30) NOT NULL,
            vacancy_name VARCHAR(100) NOT NULL,
            vacancy_salary_from INTEGER NOT NULL,
            vacancy_salary_to INTEGER NOT NULL,
            vacancy_currency  VARCHAR(10),
            vacancy_url VARCHAR(100) NOT NULL
        );
        """
        self.cursor.execute(query)

    def delete_table(self):
        query = """
                DROP SCHEMA public CASCADE;
                CREATE SCHEMA public;
                """
        self.cursor.execute(query)

