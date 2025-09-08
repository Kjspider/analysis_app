import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def plot_daily_change(df: pd.DataFrame):
    """
    株価データから騰落率（前日比）を計算し、折れ線グラフで表示します。
    0%ラインを強調表示します。
    """
    if "Close" not in df.columns:
        st.warning("終値（Close）が見つかりません。騰落率を表示できません。")
        return

    # 騰落率の計算
    df["騰落率（%）"] = df["Close"].pct_change() * 100

    # 折れ線グラフ（Plotly Express）
    fig = px.line(
        df,
        x=df.index,
        y="騰落率（%）",
        title="📊 騰落率の推移（日次）",
        labels={"騰落率（%）": "騰落率（%）", "index": "日付"},
        markers=True
    )

    # 0%ラインを追加（赤の破線）
    fig.add_shape(
        type="line",
        x0=df.index.min(),
        x1=df.index.max(),
        y0=0,
        y1=0,
        line=dict(color="black", width=2, dash="solid"),
        xref="x",
        yref="y"
    )

    # 表示
    st.plotly_chart(fig, use_container_width=True)