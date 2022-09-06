from .conftest import test_spreadsheet, SPREADSHEET_ID


class TestSpreadsheetGet:

    def test_get_sheet_format(self):
        """get_sheet() возвращает данные в виде списка списков."""
        data = test_spreadsheet.get_sheet()
        assert isinstance(data, list) and \
            all(isinstance(element, list) for element in data), (
                'Данные возвращаются в неверном формате'
        )

    def test_get_sheet(self):
        """get_sheet() возвращает все данные с листа."""
        assert test_spreadsheet.get_sheet() == [
            ['Name', 'Age', 'Strength', 'Agility', 'Intelligence'],
            ['Vasya', '21', '10', '3', '1'],
            ['Petya', '42', '3', '7', '9'],
            ['Masha', '25', '5', '9', '5']
        ]

    def test_get_format(self):
        """get() возвращает данные в виде списка списков."""
        data = test_spreadsheet.get('A1:E1')
        assert isinstance(data, list) and \
            all(isinstance(element, list) for element in data), (
                'Данные возвращаются в неверном формате'
        )

    def test_get_empty_cell(self):
        """
        get() возвращает пустую строку в двух вложенных
        списках при получении данных из пустой ячейки.
        """
        assert test_spreadsheet.get('A10') == [['']], (
            'Данные возвращаются в неверном формате'
        )

    def test_get_one_cell(self):
        """get() получает данные из одной ячейки."""
        assert test_spreadsheet.get('A1') == [['Name']]

    def test_get_one_row(self):
        """get() получает данные из одного ряда."""
        assert test_spreadsheet.get('A1:E1') == [
            ['Name', 'Age', 'Strength', 'Agility', 'Intelligence']
        ]

    def test_get_multiple_rows(self):
        """get() получает данные из нескольких рядов."""
        assert test_spreadsheet.get('A1:E2') == [
            ['Name', 'Age', 'Strength', 'Agility', 'Intelligence'],
            ['Vasya', '21', '10', '3', '1']
        ]

    def test_get_multiple_rows_with_empty_cells(self):
        """
        get() получает данные из нескольких рядов,
        обрезая лишние пустые ячейки по бокам.
        """
        assert test_spreadsheet.get('A1:F2') == [
            ['Name', 'Age', 'Strength', 'Agility', 'Intelligence'],
            ['Vasya', '21', '10', '3', '1']
        ]

    def test_get_sheet_url(self):
        """
        Проверка работы функции генерации
        ссылки на таблицу get_sheet_url()
        """
        assert test_spreadsheet.get_sheet_url() == (
            'https://docs.google.com/spreadsheets/d/'
            '1uRuwSNBwgPXXeemF2GVtYIm_zJu4qUexnozqLa-2PkU/edit#gid=0'
        )


class TestSpreadsheetInsert:

    def test_insert_success_return(self, clear_data):
        """insert() возвращает True в случае успешной вставки."""
        values = [['Kolya', '69', '10', '10', '10']]
        assert test_spreadsheet.insert(values, 'A5', 'E5', 'Лист2'), (
            'Успешная вставка не возвращает True'
        )

    def test_insert_fail_return(self):
        """insert() возвращает False в случае неудачной вставки."""
        values = [['Kolya', '69', '10', '10', '10']]
        assert not test_spreadsheet.insert(
            values, 'A5', 'E5', 'DoesNotExist'
        ), (
            'Неудачная вставка не возвращает False'
        )

    def test_insert_no_params(self, clear_data):
        """
        insert() вставляет данные в начало таблицы
        в случае, если координаты не указаны.
        """
        values = [['Kolya', '69', '10', '10', '10']]
        test_spreadsheet.insert(values, sheet_name='Лист2')
        data = test_spreadsheet.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Лист2!A1:E1'
        ).execute()
        assert data['values'] == values

    def test_insert_params(self, clear_data):
        """insert() вставляет данные в указанные координаты."""
        values = [['Kolya', '69', '10', '10', '10']]
        test_spreadsheet.insert(values, 'A5', 'E5', 'Лист2')
        data = test_spreadsheet.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Лист2!A5:E5'
        ).execute()
        assert data['values'] == values

    def test_insert_bad_params(self, clear_data):
        """insert() не вставляет данные, если интервал задан неверно."""
        values = [['Kolya', '69', '10', '10', '10']]
        test_spreadsheet.insert(values, 'A1', 'E5', 'Лист2')
        data = test_spreadsheet.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Лист2!A1:E5'
        ).execute()
        assert 'values' not in data, (
            'Данные были вставлены, несмотря на неверно заданный интервал'
        )


class TestSpreadsheetClear:

    def test_clear(self, clear_data):
        """clear() удаляет данные из указанных ячеек."""
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': [
                {
                    'range': 'Лист2!A5:E5',
                    'values': [['Kolya', '69', '10', '10', '10']]
                }
            ]
        }

        test_spreadsheet.service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()

        test_spreadsheet.clear('Лист2!A5:E5')

        data = test_spreadsheet.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Лист2!A5:E5'
        ).execute()
        assert 'values' not in data
