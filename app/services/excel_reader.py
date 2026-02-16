import pandas as pd  # type: ignore


def load_excel(file):
    xls = pd.ExcelFile(file)
    sheets = {}

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet)
        df.columns = df.columns.str.strip()
        sheets[sheet] = df

    return sheets
