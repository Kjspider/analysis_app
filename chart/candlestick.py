import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def plot_candlestick(df: pd.DataFrame, ticker: str, indicators: list, short_ma: int, long_ma: int):
    # ----------------------------------------
    # データ前処理：型変換と欠損除去
    # ----------------------------------------

    # MultiIndexカラムをフラットに変換（必要なら）
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 日付インデックスを datetime 型に変換
    df.index = pd.to_datetime(df.index)

    # 必要なカラムを float 型に変換（安全に）
    for col in ["Open", "High", "Low", "Close"]:
        if col in df.columns and isinstance(df[col], pd.Series):
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 欠損値を除去（ローソク足描画に必要なカラム）
    df.dropna(subset=["Open", "High", "Low", "Close"], inplace=True)

    # ----------------------------------------
    # グラフオブジェクトを初期化
    # ----------------------------------------
    fig = go.Figure()

    # ローソク足チャートを追加
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="価格"
    ))

    # ----------------------------------------
    # 移動平均線（短期・長期）を追加
    # ----------------------------------------
    if "移動平均線" in indicators:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"].rolling(window=short_ma).mean(),
            mode="lines",
            name=f"短期MA({short_ma})",
            line=dict(color="blue")
        ))
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"].rolling(window=long_ma).mean(),
            mode="lines",
            name=f"長期MA({long_ma})",
            line=dict(color="orange")
        ))

    # ----------------------------------------
    # ボリンジャーバンド（±2σ）を追加
    # ----------------------------------------
    if "ボリンジャーバンド" in indicators:
        ma = df["Close"].rolling(window=20).mean()
        std = df["Close"].rolling(window=20).std()
        upper = ma + 2 * std
        lower = ma - 2 * std
        fig.add_trace(go.Scatter(
            x=df.index,
            y=upper,
            name="BB上限",
            line=dict(color="green", dash="dot")
        ))
        fig.add_trace(go.Scatter(
            x=df.index,
            y=lower,
            name="BB下限",
            line=dict(color="green", dash="dot")
        ))
    # ----------------------------------------
    # VWAPラインを追加（主軸に重ねて表示）
    # ----------------------------------------
    if "VWAP" in indicators and "VWAP" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["VWAP"],
            mode="lines",
            name="VWAP",
            line=dict(color="purple", dash="dot")
        ))

     # ----------------------------------------
    # 期間指定VWAP（例：VWAP_20日）を追加
    # ----------------------------------------
    for col in df.columns:
        if col.startswith("VWAP_") and col.endswith("日") and "VWAP" in indicators:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[col],
                mode="lines",
                name=col,
                line=dict(color="purple", dash="dash")
            ))
    # ----------------------------------------
    # 出来高バーを追加（第二軸に表示）
    # ----------------------------------------
    if "出来高" in indicators and "Volume" in df.columns:
        fig.add_trace(go.Bar(
            x=df.index,
            y=df["Volume"],
            name="出来高",
            marker_color="gray",
            opacity=0.3,
            yaxis="y2"  # 第二軸に割り当て
        ))

    # ----------------------------------------
    # グラフのレイアウト設定（第二軸含む）
    # ----------------------------------------
    fig.update_layout(
        title=f"{ticker} の株価チャート",
        xaxis_title="日付",
        yaxis_title="価格",
        xaxis_rangeslider_visible=False,
        yaxis2=dict(
            title="出来高",
            overlaying="y",
            side="right",
            showgrid=False
        )
    )

    # ----------------------------------------
    # Streamlit上にチャートを表示
    # ----------------------------------------
    st.plotly_chart(fig, use_container_width=True)