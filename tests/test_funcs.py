import pytest
from funcs import get_range, get_body_insert


class TestGetRange:

    def test_get_range_no_params(self):
        """
        get_range() выбрасывает исключение при запуске без параметров.
        """
        with pytest.raises(Exception):
            get_range()

    def test_get_range_bad_params(self):
        """
        get_range() выбрасывает исключение, если
        на вход поданы неподходящие параметры.
        """
        print(get_range())
        with pytest.raises(Exception):
            get_range(1, 2, 3)

    def test_get_range_no_sheet(self):
        """
        get_range() возвращает правильный _range,
        если не указано название листа.
        """
        assert get_range('A1', 'B1') == 'A1:B1'

    def test_get_range_no_start(self):
        """
        get_range() возвращает правильный _range,
        если не указано начало интервала.
        """
        assert get_range(end='B1', sheet_name='Лист1') == 'Лист1!A:B1'

    def test_get_range_no_end(self):
        """
        get_range() возвращает правильный _range,
        если не указан конец интервала.
        """
        assert get_range(start='A1', sheet_name='Лист1') == 'Лист1!A1:Z'


class TestGetBodyInsert:

    def test_get_body_insert_no_params(self):
        """
        get_body_insert() выбрасывает исключение
        при запуске без параметров.
        """
        with pytest.raises(Exception):
            get_body_insert()

    def test_get_body_insert_bad_params(self):
        """
        get_body_insert() выбрасывает исключение, если
        на вход поданы неподходящие параметры.
        """
        with pytest.raises(Exception):
            get_body_insert(1, 2)

    def test_get_body_insert(self):
        """get_body_insert() возвращает правильный body."""
        expected = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": 'Лист1!A1:B1',
                    "values": [[1, 2, 3, 4, 5]]
                }
            ]
        }
        assert get_body_insert('Лист1!A1:B1', [[1, 2, 3, 4, 5]]) == expected
