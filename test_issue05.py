import urllib.request
import json
from unittest.mock import MagicMock
from unittest.mock import patch
import unittest

API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год
    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


class timetester(unittest.TestCase):

    def test_time(self):
        our_year = 2020
        mock = what_is_year_now()
        mock = MagicMock(return_value=2020)
        assert what_is_year_now() == our_year

    def test_time2(self):
        our_year = 2020
        mock1 = what_is_year_now()
        mock1 = MagicMock(return_value=2010)
        assert mock1 != our_year

    def test_time3(self):
        our_year = 2000
        mock2 = what_is_year_now()
        mock2= MagicMock(return_value=2020)
        assert mock2 != our_year


if __name__ == '__main__':
    unittest.main()

