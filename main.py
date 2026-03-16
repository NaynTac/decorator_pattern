from abc import ABCMeta, abstractmethod
from datetime import date


class CurrenciesABC():
    """Абстрактный класс с описанем используемых методов"""
    __metaclass__=ABCMeta

    @abstractmethod
    def get_currencies():
        """Получение данных о валютах"""


class Currencies(CurrenciesABC):
    """
    Основной класс, содержащий метод
    для получения курса валют в формате JSON
    """

    def get_currencies(self,
        url: str="https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
        """
        Функция, возвращающая полученные JSON данные в виде словаря dict

        Аргументы:
        - url: str – url для запроса
        """ 
        import requests

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        return data


class Decorator(CurrenciesABC):
    """Базовый класс декоратора"""

    _currencies_obj = None

    def __init__(self, currencies: Currencies) -> None:
        self._currencies_obj = currencies

    @property
    def currencies_obj(self) -> Currencies:
        return self._currencies_obj

    def get_currencies(self) -> dict:
        return self._currencies_obj.get_currencies()


class CurrenciesDecoratorCSV(Decorator):
    """
    Декоратор класса Currencies, с измененным основным методом
    для получения данных в формате CSV и записи их в файл
    """
    
    def get_currencies(self) -> None:
        import csv

        with open(f"data/csv-{date.today()}.csv", "w", newline="") as csv_f:

            headers = [
                "Valute",
                "ID",
                "NumCode",
                "CharCode",
                "Nominal",
                "Name",
                "Value",
                "Previous"
                ]

            # Создаем объект записи CSV-файла
            writer = csv.DictWriter(csv_f, fieldnames=headers)
            data = self.currencies_obj.get_currencies()
            # Записываем заголовки в файл
            writer.writeheader()

            # Преобразуем JSON-формат в CSV-формат и записываем данные в файл
            for key, values in data["Valute"].items():
                row = {"Valute": key} | values
                writer.writerow(row)


class CurrenciesDecoratorYAML(Decorator):
    """
    Декоратор класса Currencies, с измененным основным методом
    для получения данных в формате YAML и записи их в файл
    """
    
    def get_currencies(self) -> None:
        import yaml

        data = self.currencies_obj.get_currencies()

        with open(f"data/yaml-{date.today()}.yaml", "w", newline="") as yaml_f:
            # Записываем данные в файл, с разрешением на unicode
            yaml.dump(data, yaml_f, allow_unicode=True)