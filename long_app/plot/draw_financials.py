# ----------------------------------------
# 年間財務データの複合グラフ（売上高＋利益率）※単位自動調整
# ----------------------------------------
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 金額に応じて単位を判定する関数
def determine_unit(value):
    if value >= 1e12:
        return "兆円", 1e12
    elif value >= 1e8:
        return "億円", 1e8
    elif value >= 1e6:
        return "百万円", 1e6
    else:
        return "円", 1

# 複合グラフ本体
def plot_annual_financial_ratio_chart(df: pd.DataFrame):
    """
    売上高（棒）＋営業利益率・純利益率（折れ線）を表示する複合グラフ
    単位は企業規模に応じて自動調整
    """
    if df.empty or not all(col in df.columns for col in ["売上高", "営業利益", "純利益"]):
        st.warning("表示に必要な財務データが不足しています。")
        return

    # 売上高の最大値から適切な単位を決定
    unit_label, unit_scale = determine_unit(df["売上高"].max())

    # 単位変換と利益率計算
    df[f"売上高（{unit_label}）"] = df["売上高"] / unit_scale
    df["営業利益率（%）"] = df["営業利益"] / df["売上高"] * 100
    df["純利益率（%）"] = df["純利益"] / df["売上高"] * 100

    st.subheader("📊 年間財務推移（売上高＋利益率）")

    fig = go.Figure()


    # 売上高（棒グラフ・左軸）
    fig.add_trace(go.Bar(
        x=df.index,
        y=df[f"売上高（{unit_label}）"],
        name=f"売上高（{unit_label}）",
        yaxis="y1",
        marker=dict(color="#7f7f7f")  # ← 修正ポイント
    ))

    # 営業利益率（折れ線・右軸）
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["営業利益率（%）"],
        name="営業利益率（%）",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#ff7f0e", width=2)
    ))

    # 純利益率（折れ線・右軸）
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["純利益率（%）"],
        name="純利益率（%）",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#d62728", dash="dot", width=2)
    ))

    # レイアウト調整
    fig.update_layout(
        xaxis=dict(title="年度"),
        yaxis=dict(title=f"売上高（{unit_label}）", side="left"),
        yaxis2=dict(title="利益率（%）", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.1),
        height=500,
        margin=dict(t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)