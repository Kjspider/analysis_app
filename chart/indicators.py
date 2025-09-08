import pandas as pd

def add_vwap(df: pd.DataFrame) -> pd.DataFrame:
    # 累積VWAPと乖離率
    tp = (df["High"] + df["Low"] + df["Close"]) / 3
    volume = df["Volume"]
    vwap = (tp * volume).cumsum() / volume.cumsum()
    df["VWAP"] = vwap
    df["VWAP乖離率"] = ((df["Close"] - df["VWAP"]) / df["VWAP"]) * 100
    return df

def add_vwap_rolling(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    # 期間指定VWAP（移動平均線風）
    tp = (df["High"] + df["Low"] + df["Close"]) / 3
    volume = df["Volume"]
    df[f"VWAP_{window}日"] = (tp * volume).rolling(window=window).sum() / volume.rolling(window=window).sum()
    return df