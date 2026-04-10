import pandas as pd


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.set_index("Date")
        .resample("ME")["Amount"]
        .sum()
        .reset_index()
        .rename(columns={"Date": "Month", "Amount": "Revenue"})
    )


def rep_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("Sales Person")
        .agg(Revenue=("Amount", "sum"), Boxes=("Boxes Shipped", "sum"))
        .reset_index()
    )
    summary["Revenue per Box"] = summary["Revenue"] / summary["Boxes"]
    return summary.sort_values("Revenue", ascending=False)


def country_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Country")
        .agg(Revenue=("Amount", "sum"), Boxes=("Boxes Shipped", "sum"))
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )


def product_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("Product")
        .agg(Revenue=("Amount", "sum"), Boxes=("Boxes Shipped", "sum"))
        .reset_index()
    )
    summary["Revenue per Box"] = summary["Revenue"] / summary["Boxes"]
    return summary.sort_values("Revenue", ascending=False)


def mom_growth(monthly: pd.DataFrame) -> pd.DataFrame:
    monthly = monthly.copy()
    monthly["MoM Growth %"] = monthly["Revenue"].pct_change() * 100
    return monthly
