import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "Chocolate Sales.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")

    # Normalize column names
    df.columns = df.columns.str.strip()

    # Strip whitespace from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Parse Amount: remove currency symbols, commas, spaces; convert to float
    df["Amount"] = (
        df["Amount"].astype(str).str.replace(r"[^\d.]", "", regex=True).astype(float)
    )

    # Parse date (format: 04-Jan-22)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")

    # Derived metric
    df["revenue_per_box"] = df["Amount"] / df["Boxes Shipped"]

    return df
