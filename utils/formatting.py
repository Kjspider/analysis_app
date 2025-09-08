def format_amount(value):
    if not value:
        return "取得失敗"
    elif value >= 1e12:
        return f"{value / 1e12:.2f} 兆円"
    elif value >= 1e8:
        return f"{value / 1e8:.2f} 億円"
    elif value >= 1e6:
        return f"{value / 1e6:.2f} 百万円"
    else:
        return f"{value:.0f} 円"
