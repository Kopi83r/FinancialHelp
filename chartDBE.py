import pandas as pd
import plotly.graph_objects as go
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'scraped_data.csv')

df = pd.read_csv(csv_path)

# Convert 'Data' column to datetime with the correct format
df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')

df = df.sort_values('Data')

fig = go.Figure(data=[go.Candlestick(x=df['Data'],
                open=df['Otwarcie'],
                high=df['Max'],
                low=df['Min'],
                close=df['Zamknięcie'])])

fig.update_layout(
    title='DBE Stock Price (2019-2024)',
    yaxis_title='Price',
    xaxis_title='Date',
    xaxis_rangeslider_visible=True
)

fig.update_xaxes(
    rangebreaks=[dict(bounds=["sat", "mon"])],
    tickformat="%Y-%m-%d"
)

fig.show()
