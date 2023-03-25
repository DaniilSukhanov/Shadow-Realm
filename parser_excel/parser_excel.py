import pandas as pd
import const


class ExcelError(Exception):
    pass


class NotFoundMainSheet(ExcelError):
    pass


class ParserExcel:
    def __init__(self, filename: str):
        self.excel_table = pd.read_excel(filename, sheet_name=None)
        main_sheet = self.excel_table.get(const.ENTRY_POINT_NAME)
        if main_sheet is None:
            raise NotFoundMainSheet("В excel-файле нет точки вхождения.")
        self.main_sheet = main_sheet


if __name__ == "__main__":
    parser = ParserExcel("/Users/daniilsuhanov/Desktop/ExcelTest.xlsx")

