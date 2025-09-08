# ----------------------------------------
# StreamlitでWebアプリを構築
# ----------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------
# 必要な関数をインポート
# ----------------------------------------
from ui.sidebar import sidebar_inputs              # サイドバー入力

from fetch.stock_data import fetch_stock_data      #株価データなど取得
from metrics.valuation import fetch_per_pbr, display_per_pbr
from metrics.financials import fetch_financials, fetch_book_value, display_financials
from chart.candlestick import plot_candlestick     # チャート描画
from chart.indicators import add_vwap              # VWAP計算
from chart.indicators import add_vwap_rolling      # 移動VWAP計算
from plot.draw_metrics import plot_daily_change    # 騰落率グラフ
from metrics.financials import fetch_financial_trends
from metrics.financials import fetch_annual_financials
from plot.draw_financials import plot_annual_financial_ratio_chart
import datetime



# ----------------------------------------
# アプリタイトルの表示
# ----------------------------------------
st.title("📈 個別銘柄チェック")

# ----------------------------------------
# サイドバーからの入力を取得
# ----------------------------------------
ticker, period, indicators, short_ma, long_ma, vwap_window, financial_metrics = sidebar_inputs()


# ----------------------------------------
# 株価データを取得
# ----------------------------------------
df = fetch_stock_data(ticker, period)

# カラムがMultiIndexの場合はフラット化
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# ----------------------------------------
# データが取得できた場合の処理
# ----------------------------------------
if df.empty:
    st.error("データ取得に失敗しました。")
else:
    # ----------------------------------------
    # PER・PBRの取得（常時表示）
    # ----------------------------------------
    per, pbr = fetch_per_pbr(ticker)

    # ----------------------------------------
    # 指標に応じて加工処理（VWAPなど）
    # ----------------------------------------
    if "VWAP累積" in indicators:
        df = add_vwap(df)

    if "VWAP" in indicators and vwap_window is not None:
        df = add_vwap_rolling(df, window=vwap_window)

    # ----------------------------------------
    # チャート描画（先頭に表示）
    # ----------------------------------------
    plot_candlestick(df, ticker, indicators, short_ma, long_ma)
    # ----------------------------------------
    #  騰落率グラフ
    # ----------------------------------------

    plot_daily_change(df)

    # ----------------------------------------
    # 下部に2カラムで情報表示
    # ----------------------------------------
    col1, col2 = st.columns(2)


    # ----------------------------------------
    # 左側：# 財務情報の取得と表示（常時）
    # ----------------------------------------
    
    revenue, op_income, pretax_income, net_income, latest_year = fetch_financials(ticker)
    bps = fetch_book_value(ticker)

    with col1:
        display_financials(revenue, op_income, pretax_income, net_income, latest_year, bps)
    # ----------------------------------------
    # 右側：株価情報＋PER・PBR（常時表示）
    # ----------------------------------------
    per, pbr = fetch_per_pbr(ticker)

    # 表示（右カラム）
    with col2:
        st.subheader("📈 株価情報")
        display_per_pbr(per, pbr)

    # 財務データ取得
    # ----------------------------------------
    financial_df = fetch_financial_trends(ticker)
    # ----------------------------------------
    # 4半期データ表
    # ----------------------------------------
    quarterly_df = fetch_financial_trends(ticker)
    st.subheader("📋 四半期財務データ（額＋率）")
    st.dataframe(quarterly_df[["売上高", "営業利益", "営業利益率（%）", "純利益", "純利益率（%）"]].style.format({
        "売上高": "{:,.0f}",
        "営業利益": "{:,.0f}",
        "営業利益率（%）": "{:.1f}%",
        "純利益": "{:,.0f}",
        "純利益率（%）": "{:.1f}%"
    }))

    # ----------------------------------------
    # 年間財務グラフ
    # ----------------------------------------
    annual_df = fetch_annual_financials(ticker)

    if not annual_df.empty:
        plot_annual_financial_ratio_chart(annual_df)

    