from datetime import date
from smtplib import SMTPAuthenticationError
from typing import List
from re import fullmatch

from requests.exceptions import RequestException

from moex_rates.constants import Constants
from moex_rates.converter import Converter
from moex_rates.parser import Parser, ParsedRates
from moex_rates.sender import Sender


class Handler:
    def __init__(self) -> None:
        self.getter = Constants.EmailDefaults.GETTER
        self.sender = Constants.EmailDefaults.SENDER
        self.sender_pass = Constants.EmailDefaults.SENDER_PASS
        self.copy = Constants.EmailDefaults.COPY_MAIL

        try:
            self.parsed_dict = self.parse_site()
            self.rows_num = self.convert_to_excel()
            self.make_getter_address()
            self.send_email()
        except (
            ValueError,
            RequestException,
            PermissionError,
            SMTPAuthenticationError,
            FileNotFoundError,
        ) as e:
            print(e)

    def make_getter_address(self) -> None:
        address = input(
            'Enter getter address.\n'
            'if you want to send message to default address'
            f' {Constants.EmailDefaults.GETTER} '
            'enter empty string\n'
            '> ').replace(' ', '')
        if address != '':
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if fullmatch(regex, address):
                self.getter = address
            else:
                print(f"Incorrect address {address}")
        print(f'Getter address: {self.getter}')
        print(f'Sender address: {self.sender}')
        print(f'Copy address: {self.copy}')

    @staticmethod
    def parse_site() -> List[ParsedRates]:
        parser = Parser(day=date.today())
        return [parser.get_parsed_rates(rate_name=rate) for rate in parser.get_supported_rates()]

    def convert_to_excel(self) -> int:
        converter = Converter(*self.parsed_dict)
        converter.convert_excel()
        return converter.get_col_len()

    def send_email(self) -> None:
        sender = Sender(
            sender=[self.sender, self.sender_pass],
            getters=[self.getter, self.copy],
            row_count=self.rows_num,
            path=Constants.ExcelDefaults.PATH,
        )
        sender.send_message()
