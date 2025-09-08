# ----------------------------------------
# 必要なライブラリのインポート
# ----------------------------------------
import yfinance as yf
import pandas as pd

# ----------------------------------------
# 株価データの取得関数
# ----------------------------------------
def fetch_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    銘柄コードと期間を指定して株価データを取得します。
    """
    if not ticker:
        return pd.DataFrame()
    try:
        df = yf.download(ticker, period=period)
        df.dropna(inplace=True)
        return df
    except Exception:
        return pd.DataFrame()

