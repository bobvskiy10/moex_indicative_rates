from datetime import datetime


class Constants:
    class UrlComponents:
        SCHEM = 'https'
        NETLOC = 'www.moex.com'
        PATH = '/export/derivatives/currency-rate.aspx'
        PARAMS = ''
        QUERY = {
            'language': 'en',
            'currency': '',
            'moment_start': '',
            'moment_end': '',
        }
        FRAGMENT = ''
        USD_RUB = 'USD_RUB'
        JPY_RUB = 'JPY_RUB'

    class DateComponents:
        DEFAULT_DATETIME = datetime.fromisoformat('2022-09-21 00:00:00')
        DEFAULT_TIME = DEFAULT_DATETIME.time()
        DEFAULT_DATE = DEFAULT_DATETIME.date()

    class ExcelDefaults:
        PATH = './rates.xlsx'
        SHEET_NAME = 'Курсы валют'
        ROWS_NAMES = [
            'Дата',
            'Курс USD_RUB',
            'Время',
            'Дата',
            'Курс JPY_RUB',
            'Время',
            'Результат',
        ]
        RUB_FORMAT = '* # ##0.0000 ₽'
        JPY_FORMAT = '* # ##0.0000 ¥'
        FINANCE_LEN = len('.0000 ₽')
        RUB_ROWS = [1, 4]
        RESULT_ROW = [6]

    class EmailDefaults:
        SENDER = 'moex.rates.prev.month@gmail.com'
        SENDER_PASS = 'dmzhmyoiumtmbxtd'
        GETTER = 'bobovskiy.10@yandex.ru'
        COPY_MAIL = 'bobovskiy.10@gmail.com'
        FILENAME = 'moex_inidicative_rates_previous_month.xlsx'
        SUBJECT = 'Индикативные курсы валют за прошлый месяц с сайта московской биржы'
        'IAVikharev@Greenatom.ru'
