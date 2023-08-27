from abc import abstractmethod, ABC


class BaseApi(ABC):
    def __init__(self, url='', number_of_vacancies=10):
        self.url = url
        self.number_of_vacancies = number_of_vacancies

    @abstractmethod
    def _search_vacancies(self, employer_id, page=0):
        pass
    @abstractmethod
    def get_vacancies(self, employer_id):
        pass
