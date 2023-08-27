--Создание таблицы всех вакансий
CREATE TABLE IF NOT EXISTS table_name
(
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(30) NOT NULL,
    vacancy_name VARCHAR(100) NOT NULL,
    vacancy_salary_from INTEGER NOT NULL,
    vacancy_salary_to INTEGER NOT NULL,
    vacancy_currency  VARCHAR(10),
    vacancy_url VARCHAR(100) NOT NULL
);
--Заполнение таблицы всех вакансий
INSERT INTO table_name (company_name, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_currency,
                           vacancy_url)
VALUES (%s,%s,%s,%s,%s,%s);
--Удаление таблиц
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

--Компании с количеством вакакансий
SELECT company_name, COUNT(*) AS amount_vacancies
FROM hh_table
GROUP BY company_name;

--Получение всех вакансий
SELECT * FROM hh_table;

--Средняя зарплата
SELECT
    (SELECT ROUND(AVG(vacancy_salary_from)) FROM hh_table WHERE  vacancy_salary_from <> 0)AS avg_salary_from,
    (SELECT ROUND(AVG(vacancy_salary_to)) FROM hh_table WHERE  vacancy_salary_to <> 0)AS avg_salary_to;

--Вакансии с зарплатой выше средней
SELECT * FROM  hh_table
where vacancy_salary_from >
    (SELECT ROUND(AVG(vacancy_salary_from)) FROM hh_table WHERE  vacancy_salary_from <> 0)
AND vacancy_salary_to >
    (SELECT ROUND(AVG(vacancy_salary_to)) FROM hh_table WHERE  vacancy_salary_to <> 0)
ORDER BY vacancy_salary_from DESC, vacancy_salary_to DESC;

--Вакансии с ключевым словом
SELECT *
FROM  hh_table
WHERE LOWER(vacancy_name) ILIKE %s;



