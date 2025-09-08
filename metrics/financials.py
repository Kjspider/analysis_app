# ----------------------------------------
# 財務情報の取得関数（売上・利益＋年度付き）
# ----------------------------------------
import streamlit as st
import yfinance as yf
import pandas as pd

from utils.formatting import format_amount


# 年度単位の財務情報（最新年度の単発表示）
def fetch_financials(ticker: str):
    try:
        t = yf.Ticker(ticker)
        df = t.financials
        latest_year = df.columns[0].year if not df.empty else None

        revenue = df.loc["Total Revenue"].iloc[0] if "Total Revenue" in df.index else None
        operating_income = df.loc["Operating Income"].iloc[0] if "Operating Income" in df.index else None
        pretax_income = df.loc["Pretax Income"].iloc[0] if "Pretax Income" in df.index else None
        net_income = df.loc["Net Income"].iloc[0] if "Net Income" in df.index else None

        return revenue, operating_income, pretax_income, net_income, latest_year
    except Exception:
        return None, None, None, None, None

# 純資産（BPS）の取得
def fetch_book_value(ticker: str):
    try:
        info = yf.Ticker(ticker).info
        bps = info.get("bookValue")
        return bps
    except Exception:
        return None

# Streamlit表示用：年度単位の財務情報
def display_financials(revenue, op_income, pretax_income, net_income, latest_year, bps):
    st.subheader("📋 財務情報")
    if latest_year:
        st.caption(f"※ 財務情報は {latest_year} 年度の決算に基づいています。")

    st.write(f"売上高: {format_amount(revenue)}")
    st.write(f"営業利益: {format_amount(op_income)}")
    st.write(f"経常利益: {format_amount(pretax_income)}")
    st.write(f"純利益: {format_amount(net_income)}")
    st.write(f"純資産（BPS）: {bps:.2f} 円" if bps else "取得失敗")


# 四半期データ（表表示用）
def fetch_financial_trends(ticker: str):
    try:
        t = yf.Ticker(ticker)
        df = t.quarterly_financials.T
        df.index = df.index.strftime("%Y-%m")

        df = df.rename(columns={
            "Total Revenue": "売上高",
            "Operating Income": "営業利益",
            "Pretax Income": "経常利益",
            "Net Income": "純利益"
        })

        eps = t.info.get("trailingEps")
        if eps:
            df["EPS"] = eps

        for col in ["営業利益", "経常利益", "純利益"]:
            if "売上高" in df.columns and col in df.columns:
                df[f"{col}率（%）"] = (df[col] / df["売上高"]) * 100

        return df
    except Exception:
        return pd.DataFrame()

# 年間データ（グラフ表示用）
def fetch_annual_financials(ticker: str):
    try:
        t = yf.Ticker(ticker)
        df = t.financials.T.copy()
        df.index = df.index.strftime("%Y")

        df = df.rename(columns={
            "Total Revenue": "売上高",
            "Operating Income": "営業利益",
            "Net Income": "純利益"
        })

        return df[["売上高", "営業利益","純利益"]]
    except Exception:
        return pd.DataFrame()