import requests

from src.base_api import BaseApi


class HH(BaseApi):
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, url=url):
        super().__init__(url=url, number_of_vacancies=100)

    def _search_vacancies(self, employer_id, page=1):
        params = {
            'per_page': self.number_of_vacancies,
            'archived': False,
            'employer_id': employer_id,
            'page': page
        }
        return requests.get(url=self.url, params=params).json().get("items", [])

    def get_vacancies(self, employer_id):
        all_vacancies = []
        for page in range(20):
            page_vacancies = self._search_vacancies(employer_id, page=page)
            if len(page_vacancies) == 0:
                break
            all_vacancies.extend(page_vacancies)
        return all_vacancies
