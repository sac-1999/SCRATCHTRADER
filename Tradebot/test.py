import pandas as pd
import plotly.graph_objects as go

def get_stock_data():
    df = pd.read_csv('./data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df = df.resample('15min').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    })
    df.reset_index(inplace=True)
    return df

df = get_stock_data()

# Define the full date range
full_range = pd.date_range(start=df['timestamp'].min(), end=df['timestamp'].max(), freq='15T')
df_resampled = df.set_index('timestamp').reindex(full_range).reset_index()
df_resampled.rename(columns={'index': 'timestamp'}, inplace=True)
print(df)
# Identify missing timestamps
missing_dates = df_resampled[df_resampled.isnull().any(axis=1)]['timestamp']
print(missing_dates)
# Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=df_resampled['timestamp'],
    open=df_resampled['open'],
    high=df_resampled['high'],
    low=df_resampled['low'],
    close=df_resampled['close'],
    increasing_line_color='green',
    decreasing_line_color='red'
)])

# Update layout to hide missing time periods
fig.update_layout(
    title='Continuous Candlestick Chart',
    xaxis_title='Date',
    yaxis_title='Price',
    xaxis_rangeslider_visible=False,
    xaxis=dict(
        rangebreaks=[
            dict(values=missing_dates)
        ]
    )
)

fig.show()
