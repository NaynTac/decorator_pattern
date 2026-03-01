import pytest

from unittest.mock import call
from main import *


def test_currencies(mocker) -> None:
	"""Тестирование базового класса"""

	# Патчим функцию запроса
	mock_get = mocker.patch("requests.get")

	# Подгатавливаем начальные данные
	some_data = {"data": "some_data"}
	c = Currencies()

	# Имитируем вызов метода get()
	mock_resp = mocker.Mock()
	mock_resp.raise_for_status.return_value = None
	mock_resp.json.return_value = some_data
	mock_get.return_value = mock_resp

	# Проверяем, что все вернулось верно
	assert c.get_currencies() == some_data


def test_currencies_csv(mocker) -> None:
	"""Тестирование CSV-декоратора"""

	c = Currencies()
	c_csv = CurrenciesDecoratorCSV(c)

	# Создаем закглушку для метода get_currencies() базового класса
	c_stub = mocker.stub()
	c_stub.return_value = {
		'Valute': {
			'AUD': {
				'ID': 'R1',
				'NumCode': '036',
				'CharCode': 'AUD',
				'Nominal': 1,
				'Name': 'Ав',
				'Value': 55,
				'Previous': 54
			}, 
			'AZN': {
				'ID': 'R0',
				'NumCode': '944',
				'CharCode': 'AZN',
				'Nominal': 1,
				'Name': 'Аз',
				'Value': 45, 
				'Previous': 42
			}
		}
	}

	mocker.patch.object(c, "get_currencies", c_stub)

	# Создаем Mock-объекты для open() и csv.DictWriter()
	mock_writer = mocker.Mock()
	mock_file = mocker.mock_open()
	mocker.patch("csv.DictWriter", return_value=mock_writer)
	mocker.patch('builtins.open', mock_file)

	# Предполагаемые данные
	expected_data = [
		{'Valute': 'AUD',
		'ID': 'R1',
		'NumCode': '036',
		'CharCode': 'AUD',
		'Nominal': 1,
		'Name': 'Ав',
		'Value': 55,
		'Previous': 54
		}, 
		{'Valute': 'AZN',
		'ID': 'R0',
		'NumCode': '944',
		'CharCode': 'AZN',
		'Nominal': 1,
		'Name': 'Аз',
		'Value': 45, 
		'Previous': 42
		}
	]

	# Вызов метода декоратора (CSV)
	c_csv.get_currencies()

	# Список вызовов с предполагаемыми данными
	expected_calls = [call(row) for row in expected_data]

	# Проверка корректного открытия файла
	mock_file.assert_called_once_with(mocker.ANY, "w", newline="")
	# Проверка корректных вызовов метода writerow()
	assert mock_writer.writerow.call_args_list == expected_calls


def test_currencies_yaml(mocker) -> None:
	"""Тестирование YAML-декоратора"""

	c = Currencies()
	c_yml = CurrenciesDecoratorYAML(c)

	expected_data = {
		'Valute': {
			'AUD': {
				'ID': 'R1',
				'NumCode': '036',
				'CharCode': 'AUD',
				'Nominal': 1,
				'Name': 'Ав',
				'Value': 55,
				'Previous': 54
			}, 
			'AZN': {
				'ID': 'R0',
				'NumCode': '944',
				'CharCode': 'AZN',
				'Nominal': 1,
				'Name': 'Аз',
				'Value': 45, 
				'Previous': 42
			}
		}
	}

	# Создаем закглушку для метода get_currencies() базового класса
	c_stub = mocker.stub()
	c_stub.return_value = expected_data

	mocker.patch.object(c, "get_currencies", c_stub)

	# Создаем Mock-объекты для open() и yaml.dump()
	mock_dump = mocker.Mock()
	mock_file = mocker.mock_open()
	mocker.patch("yaml.dump", mock_dump)
	mocker.patch('builtins.open', mock_file)

	c_yml.get_currencies()

	# Проверка корректного открытия файла
	mock_file.assert_called_once_with(mocker.ANY, "w", newline="")
	# Проверка корректного выполнения метода yaml.dump()
	mock_dump.assert_called_once_with(
		expected_data,
		mocker.ANY,
		allow_unicode=True
	)