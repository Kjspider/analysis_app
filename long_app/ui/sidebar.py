import streamlit as st
import pandas as pd

def sidebar_inputs():
    # ----------------------------------------
    # CSVから企業名と銘柄コードの対応表を読み込む
    # ----------------------------------------
    try:
        company_df = pd.read_csv("data/company_list.csv", encoding="utf-8")  # Shift_JISの場合は変更
        company_df.columns = company_df.columns.str.strip()  # 列名の空白除去
    except Exception as e:
        st.sidebar.error(f"企業リストの読み込みに失敗しました: {e}")
        st.stop()

    # 必要な列が存在するか確認
    if "銘柄名称" not in company_df.columns or "銘柄コード" not in company_df.columns:
        st.sidebar.error("CSVに '銘柄名称' または '銘柄コード' 列が見つかりません。")
        st.stop()

    # 銘柄名称 → 銘柄コードの辞書を作成
    company_dict = dict(zip(company_df["銘柄名称"], company_df["銘柄コード"]))

    # ----------------------------------------
    # サイドバーUI：企業名選択
    # ----------------------------------------
    selected_company = st.sidebar.selectbox("企業名を選んでください", list(company_dict.keys()))
    ticker = company_dict[selected_company]

    # ----------------------------------------
    # サイドバーUI：分析条件の入力
    # ----------------------------------------
    period = st.sidebar.selectbox("期間", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

    indicators = st.sidebar.multiselect(
        "表示する指標",
        ["移動平均線", "ボリンジャーバンド", "出来高", "VWAP", "VWAP累積"]
    )

    short_ma = st.sidebar.slider("短期移動平均（日）", 5, 30, 10)
    long_ma = st.sidebar.slider("長期移動平均（日）", 30, 120, 50)

    vwap_window = st.sidebar.selectbox("VWAPの期間（日数）", options=[5, 10, 20, 30, 60], index=2)

    financial_metrics = st.sidebar.multiselect(
        "表示する財務指標（財務グラフ）",
        ["売上高", "営業利益", "経常利益", "純利益", "EPS"],
        default=["売上高", "営業利益", "純利益"]
    )

    # ----------------------------------------
    # 入力値を返す
    # ----------------------------------------
    return ticker, period, indicators, short_ma, long_ma, vwap_window, financial_metrics