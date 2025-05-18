import plotly.graph_objects as go

# Sample data
stocks = ["AAPL", "GOOG", "MSFT", "AMZN"]
opens = [148, 2780, 325, 3480]  # Opening prices
highs = [150, 2800, 330, 3500]  # Max price of the day
lows = [145, 2750, 320, 3450]  # Min price of the day
closes = [149, 2790, 322, 3490]  # Closing prices

# Calculate percentage changes relative to open price
opens_pct = [0] * len(opens)  # Open price is the reference (0%)
highs_pct = [(h - o) / o * 100 for h, o in zip(highs, opens)]
lows_pct = [(l - o) / o * 100 for l, o in zip(lows, opens)]
closes_pct = [(c - o) / o * 100 for c, o in zip(closes, opens)]

# Create candlestick chart with percentage changes
fig = go.Figure(data=[go.Candlestick(
    x=stocks,
    open=opens_pct,
    high=highs_pct,
    low=lows_pct,
    close=closes_pct,
    increasing_line_color="green",
    decreasing_line_color="red"
)])

fig.update_layout(
    title="Stock Percentage Change (Open-Close Body & High-Low Wicks)",
    xaxis_title="Stock",
    yaxis_title="Percentage Change (%)",
    xaxis_rangeslider_visible=False
)

fig.show()