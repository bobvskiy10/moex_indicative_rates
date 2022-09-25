import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from moex_rates.constants import Constants


class Sender:
    def __init__(
        self,
        sender: List[str],
        getters: List[str],
        row_count: int = 0,
        path: str = Constants.ExcelDefaults.PATH,
    ) -> None:
        self.row_count = row_count
        self.path = path
        self.sender = sender[0]
        self.password = sender[1]
        self.getter = getters[0]
        self.copy = getters[1]
        self.getters_list = getters
        self.server = smtplib.SMTP(self.get_smtp_host())
        self.server.starttls()
        self.filename = Constants.EmailDefaults.FILENAME

    def get_smtp_host(self) -> str:
        domain = self.sender.split('@')[-1]
        return f'smtp.{domain}'

    @staticmethod
    def get_correct_form_of_word(count: int) -> str:
        message = f'{count}'
        if count % 100 in range(10, 20) or count % 10 in range(5, 10) or count % 10 == 0:
            message += ' строк'
        elif count % 10 == 1:
            message += ' строка'
        else:
            message += ' строки'
        return message

    def get_message_text(self) -> str:
        message = f'{self.get_correct_form_of_word(self.row_count)}\n'
        message += self.get_correct_form_of_word(self.row_count + 1)
        message += ', считая заголовки'
        return message

    def get_email(self) -> MIMEMultipart:
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.getter
        message['Subject'] = Constants.EmailDefaults.SUBJECT
        message['CC'] = self.copy
        message.attach(MIMEText(self.get_message_text()))
        try:
            attachment = MIMEBase('application', 'octet-stream')
            with open(self.path, 'rb', encoding=None) as file:
                attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename={self.filename}',
                )
                message.attach(attachment)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Can't open {self.path}. {e}") from None

        return message

    def send_message(self) -> None:
        message = self.get_email()

        try:
            self.server.login(self.sender, self.password)
            self.server.sendmail(self.sender, self.getters_list, message.as_string())
        except smtplib.SMTPAuthenticationError as e:
            raise smtplib.SMTPAuthenticationError(
                msg='Check your login and/or password.', code=e.smtp_code
            )
        except TypeError:
            raise TypeError('Incorrect message.') from None
