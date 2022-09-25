from datetime import date, datetime, timedelta
from typing import Any, List, Dict
from urllib.parse import urlencode, urlunparse
from xml.dom import minidom

import requests

from moex_rates.constants import Constants


class ParsedRates:
    def __init__(self, rate_name: str, parsed_dict: Dict[datetime, float]) -> None:
        self._parsed_dict = {
            f'Date {rate_name}': [key.date() for key in parsed_dict.keys()],
            rate_name: [value for value in parsed_dict.values()],
            f'Time {rate_name}': [key.time() for key in parsed_dict.keys()],
        }

    @property
    def parsed_dict(self) -> Dict[str, List[Any]]:
        return self._parsed_dict.copy()


class Parser:
    def __init__(
        self,
        day: date = Constants.DateComponents.DEFAULT_DATE,
        rate_name: str = Constants.UrlComponents.USD_RUB,
    ) -> None:
        last_day = day.replace(day=1) - timedelta(days=1)
        self.start_date = last_day.replace(day=1)
        self.end_date = last_day
        self.supported_rates = [
            Constants.UrlComponents.USD_RUB,
            Constants.UrlComponents.JPY_RUB,
        ]
        if rate_name not in self.supported_rates:
            rate_name = Constants.UrlComponents.USD_RUB
        self.current_rate = rate_name
        self.query = Constants.UrlComponents.QUERY
        self.query.update(
            {
                'currency': self.current_rate,
                'moment_start': str(self.start_date),
                'moment_end': str(self.end_date),
            }
        )
        self.url = ''
        def_dict = {Constants.DateComponents.DEFAULT_DATETIME: 0.}
        self.parsed_rates = ParsedRates(rate_name=rate_name, parsed_dict=def_dict)

    def get_supported_rates(self) -> List[str]:
        return self.supported_rates.copy()

    def make_url(self, rate_name: str = Constants.UrlComponents.USD_RUB) -> None:
        self.current_rate = rate_name
        self.query['currency'] = self.current_rate
        url = urlunparse(
            (
                Constants.UrlComponents.SCHEM,
                Constants.UrlComponents.NETLOC,
                Constants.UrlComponents.PATH,
                Constants.UrlComponents.PARAMS,
                urlencode(self.query),
                Constants.UrlComponents.FRAGMENT,
            )
        )
        self.url = url

    def get_web_xml(self, rate_name: str = Constants.UrlComponents.USD_RUB) -> requests.Response:
        if rate_name not in self.supported_rates:
            raise ValueError("Can't get rates. Consider changing rates name.")
        if self.url == '' or rate_name != self.current_rate:
            self.make_url(rate_name=rate_name)

        try:
            req = requests.get(self.url, timeout=10)
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise requests.exceptions.ConnectionError(f'Error connecting to the site: {e}')
        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout('Request timeout. Try again later.') from None
        except requests.exceptions.TooManyRedirects:
            raise requests.exceptions.TooManyRedirects(
                'Too many redirects. Consider changing date and/or currency rates name.'
            ) from None

        return req

    def parse_rates(self, rate_name: str) -> None:
        web_file = self.get_web_xml(rate_name)
        dom = minidom.parseString(web_file.content)
        rates_info = dom.getElementsByTagName('rtsdata')
        if rates_info.length == 0:
            raise ValueError("Can't get rates. Consider changing date and/or currency rates name.")
        elements = dom.getElementsByTagName('rate')
        if elements.length == 0:
            raise ValueError("Can't get rates. Consider changing date and/or currency rates name.")
        clearing_time = Constants.DateComponents.DEFAULT_TIME
        parsed_dict: [datetime, float] = {}
        for node in elements:
            rate_value = float(node.getAttribute('value'))
            rate_datetime = datetime.fromisoformat(node.getAttribute('moment'))
            if rate_datetime.time() > clearing_time:
                parsed_dict = {}
                clearing_time = rate_datetime.time()
            if rate_datetime.time() == clearing_time:
                parsed_dict[rate_datetime] = rate_value
        self.parsed_rates = ParsedRates(rate_name=rate_name, parsed_dict=parsed_dict)

    def get_parsed_rates(
        self, rate_name: str = Constants.UrlComponents.USD_RUB
    ) -> ParsedRates:
        self.parse_rates(rate_name)
        return self.parsed_rates
