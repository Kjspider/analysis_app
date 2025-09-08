# ----------------------------------------
# PER・PBRの取得と表示モジュール
# ----------------------------------------

import yfinance as yf
import streamlit as st

def fetch_per_pbr(ticker: str):
    """
    指定した銘柄コードからPER・PBRを取得します。
    """
    try:
        info = yf.Ticker(ticker).info
        price = info.get("currentPrice")
        eps = info.get("trailingEps")
        bps = info.get("bookValue")

        per = price / eps if price and eps else None
        pbr = price / bps if price and bps else None

        return per, pbr
    except Exception:
        return None, None

def display_per_pbr(per: float, pbr: float):
    """
    PER・PBRをStreamlit上に表示する。
    """
    st.caption("※ PER・PBRは直近の財務データ（過去12ヶ月）に基づいて算出されています。")
    st.write(f"PER: {per:.2f} 倍" if per else "取得失敗")
    st.write(f"PBR: {pbr:.2f} 倍" if pbr else "取得失敗")
    