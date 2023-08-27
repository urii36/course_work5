from database.db_manager import DBManager
from src.config import EMPLOYER_MAP
from src.hh_api import HH
from utils.currency_convertor import get_currency_converter


def main():
    # Создаем экземпляр класса DBManager
    db_manager = DBManager('hh_parser')
    hh = HH()
    db_manager.delete_table()
    db_manager.create_table()
    for employer_name, employer_id in EMPLOYER_MAP.items():
        compnay_vacancies = hh.get_vacancies(employer_id)

        for vacancy in compnay_vacancies:
            vacancy_name = vacancy["name"]
            vacancy_url = vacancy["alternate_url"]
            vacancy_from = int(
                vacancy["salary"]["from"]) if vacancy.get("salary") is not None and vacancy["salary"].get(
                "from") is not None else 0
            vacancy_to = int(
                vacancy["salary"]["to"]) if vacancy.get("salary") is not None and vacancy["salary"].get(
                "to") is not None else 0
            if vacancy.get("salary") and vacancy["salary"]["currency"] not in ["RUR", "RUB"]:
                vacancy_from = get_currency_converter(vacancy["salary"]["currency"])
                vacancy_to = get_currency_converter(vacancy["salary"]["currency"])

            vacancy_currency = "RUR"

            db_manager.insert_vacancies(company_name=employer_name,
                                        vacancy_name=vacancy_name, vacancy_salary_from=vacancy_from,
                                        vacancy_salary_to=vacancy_to, vacancy_currency=vacancy_currency,
                                        vacancy_url=vacancy_url
                                        )
    while True:
        print("Выберите действие:")
        print("1. Получить список всех компаний и количество вакансий у каждой компании")
        print("2. Получить список всех вакансий")
        print("3. Получить среднюю зарплату по вакансиям")
        print("4. Получить список вакансий с зарплатой выше средней")
        print("5. Получить список вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            # Получить список всех компаний и количество вакансий
            companies_vacancies = db_manager.get_companies_and_vacancies_count()
            print("Список компаний и количество вакансий:")
            for company, count in companies_vacancies:
                print(f"Компания: {company}, Количество вакансий: {count}")
            print()

        elif choice == "2":
            # Получить список всех вакансий
            all_vacancies = db_manager.get_all_vacancies()
            for vacancy in all_vacancies:
                print(vacancy)


        elif choice == "3":
            # Получить среднюю зарплату по вакансиям
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {round(avg_salary)}")
            print()

        elif choice == "4":
            # Получить список вакансий с зарплатой выше средней
            high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            print("Список вакансий с зарплатой выше средней:")
            for vacancy in high_salary_vacancies:
                print(vacancy)  # Предполагается, что vacancy - это кортеж с данными вакансии
            print()

        elif choice == "5":
            # Получить список вакансий по ключевому слову
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(f"Список вакансий с ключевым словом '{keyword}':")
            for vacancy in keyword_vacancies:
                print(vacancy)  # Предполагается, что vacancy - это кортеж с данными вакансии
            print()

        elif choice == "0":
            # Выход из программы
            break

        else:
            print("Неверный выбор. Попробуйте еще раз.")

    # Закрываем соединение с базой данных
    db_manager.close_connection()


if __name__ == "__main__":
    main()
