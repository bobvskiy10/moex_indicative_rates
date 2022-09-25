import pandas as pd

from moex_rates.constants import Constants
from moex_rates.parser import ParsedRates


class Converter:
    def __init__(self, table1: ParsedRates, table2: ParsedRates) -> None:
        self.table1 = table1.parsed_dict
        self.table2 = table2.parsed_dict
        self.df = self.convert_to_pandas()

    def convert_to_pandas(self) -> pd.DataFrame:
        df1 = pd.DataFrame(self.table1)
        df2 = pd.DataFrame(self.table2)
        df = pd.concat([df1, df2], axis=1)
        key1, key2 = df.keys()[1], df.keys()[4]
        df['Result'] = df[key1] / df[key2]
        return df

    def get_data_width(self, row_num: int) -> int:
        if (
            row_num not in Constants.ExcelDefaults.RUB_ROWS
            and row_num not in Constants.ExcelDefaults.RESULT_ROW
        ):
            r_len = self.df[self.df.keys()[row_num]].astype(str).map(len).max()
        else:
            r_len = Constants.ExcelDefaults.FINANCE_LEN + len(
                str(int(max(self.df[self.df.keys()[row_num]])))
            )
        return max(len(Constants.ExcelDefaults.ROWS_NAMES[row_num]), r_len) + 1

    def convert_excel(self) -> None:
        try:
            with pd.ExcelWriter(Constants.ExcelDefaults.PATH, engine='xlsxwriter') as writer:
                self.df.to_excel(
                    excel_writer=writer,
                    sheet_name=Constants.ExcelDefaults.SHEET_NAME,
                    index=False,
                    header=False,
                    startrow=1,
                )
                workbook = writer.book
                worksheet = writer.sheets[Constants.ExcelDefaults.SHEET_NAME]

                for col, data in enumerate(Constants.ExcelDefaults.ROWS_NAMES):
                    worksheet.write(0, col, data)
                rub_format = workbook.add_format({'num_format': Constants.ExcelDefaults.RUB_FORMAT})
                jpy_format = workbook.add_format({'num_format': Constants.ExcelDefaults.JPY_FORMAT})
                for i in range(len(Constants.ExcelDefaults.ROWS_NAMES)):
                    row_format = None
                    if i in Constants.ExcelDefaults.RUB_ROWS:
                        row_format = rub_format
                    elif i in Constants.ExcelDefaults.RESULT_ROW:
                        row_format = jpy_format
                    worksheet.set_column(i, i, self.get_data_width(i), row_format)
        except PermissionError:
            raise PermissionError(
                "Can't write in Excel file. Please close Excel file and/or change access rights."
            ) from None

    def get_col_len(self) -> int:
        return len(list(self.table1.items())[0][1])
