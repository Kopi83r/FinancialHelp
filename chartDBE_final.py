import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
import os

# Set up the path for the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'scraped_data.csv')

# Read the CSV into a DataFrame
df = pd.read_csv(csv_path)

# Convert 'Data' column to datetime format and sort the DataFrame by 'Data'
df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')
df = df.sort_values('Data')

# Ensure that 'Wolumen' is numeric, convert if necessary
df['Wolumen'] = pd.to_numeric(df['Wolumen'], errors='coerce')

# Check for NaN values in 'Wolumen' and drop or fill them
df['Wolumen'].fillna(0, inplace=True)  # Fill NaN with 0 or choose another method

# Ensure other necessary columns are numeric and check for NaN values
for col in ['Max', 'Min', 'Zamknięcie', 'Otwarcie']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col].fillna(method='ffill', inplace=True)  # Forward fill NaNs

# Now proceed to calculate technical indicators

# RSI (Relative Strength Index)
df['RSI'] = ta.rsi(df['Zamknięcie'], length=14)

# STOCH (Stochastic Oscillator)
stoch_df = ta.stoch(df['Max'], df['Min'], df['Zamknięcie'], k=14, d=3)
df['STS'] = stoch_df['STOCHk_14_3_3']

# MACD (Moving Average Convergence Divergence)
macd_df = ta.macd(df['Zamknięcie'], fast=12, slow=26, signal=9)
df['MACD'] = macd_df['MACD_12_26_9']

# TRIX (Triple Exponential Average)
trix_df = ta.trix(df['Zamknięcie'], length=14, signal=9)
df['TRIX'] = trix_df['TRIX_14_9']

# Williams %R
df['WILLR'] = ta.willr(df['Max'], df['Min'], df['Zamknięcie'], length=10)

# CCI (Commodity Channel Index)
df['CCI'] = ta.cci(df['Max'], df['Min'], df['Zamknięcie'], length=14)

# ROC (Rate of Change)
df['ROC'] = ta.roc(df['Zamknięcie'], length=15)

# ULT (Ultimate Oscillator)
df['ULT'] = ta.uo(df['Max'], df['Min'], df['Zamknięcie'], short=7, medium=14, long=28)

# FI (Force Index)
df['FI'] = ta.efi(df['Zamknięcie'], df['Wolumen'], length=13)

# MFI (Money Flow Index)
df['MFI'] = ta.mfi(df['Max'], df['Min'], df['Zamknięcie'], df['Wolumen'], length=14)

# BOP (Balance of Power)
df['BOP'] = ta.bop(df['Otwarcie'], df['Max'], df['Min'], df['Zamknięcie'], length=14)

# EMV (Ease of Movement)
df['EMV'] = ta.eom(df['Max'], df['Min'], df['Zamknięcie'], df['Wolumen'], length=14)

# Generate Buy/Sell Signals for each indicator
# RSI Signal
df['RSI_Signal'] = 'Hold'
df.loc[df['RSI'] < 30, 'RSI_Signal'] = 'Buy'
df.loc[df['RSI'] > 70, 'RSI_Signal'] = 'Sell'

# STS Signal
df['STS_Signal'] = 'Hold'
df.loc[(df['STS'] < 20) & (df['STS'].shift(1) >= 20), 'STS_Signal'] = 'Buy'
df.loc[(df['STS'] > 80) & (df['STS'].shift(1) <= 80), 'STS_Signal'] = 'Sell'

# MACD Signal
df['MACD_Signal'] = 'Hold'
df.loc[(df['MACD'] > df['MACD'].shift(1)) & (df['MACD'].shift(1) < 0), 'MACD_Signal'] = 'Buy'
df.loc[(df['MACD'] < df['MACD'].shift(1)) & (df['MACD'].shift(1) > 0), 'MACD_Signal'] = 'Sell'

# TRIX Signal
df['TRIX_Signal'] = 'Hold'
df.loc[(df['TRIX'] > df['TRIX'].shift(1)) & (df['TRIX'].shift(1) < 0), 'TRIX_Signal'] = 'Buy'
df.loc[(df['TRIX'] < df['TRIX'].shift(1)) & (df['TRIX'].shift(1) > 0), 'TRIX_Signal'] = 'Sell'

# Williams %R Signal
df['WILLR_Signal'] = 'Hold'
df.loc[df['WILLR'] < -80, 'WILLR_Signal'] = 'Buy'
df.loc[df['WILLR'] > -20, 'WILLR_Signal'] = 'Sell'

# CCI Signal
df['CCI_Signal'] = 'Hold'
df.loc[df['CCI'] < -100, 'CCI_Signal'] = 'Buy'
df.loc[df['CCI'] > 100, 'CCI_Signal'] = 'Sell'

# ROC Signal
df['ROC_Signal'] = 'Hold'
df.loc[df['ROC'] > 0, 'ROC_Signal'] = 'Buy'
df.loc[df['ROC'] < 0, 'ROC_Signal'] = 'Sell'

# ULT Signal
df['ULT_Signal'] = 'Hold'
df.loc[df['ULT'] < 30, 'ULT_Signal'] = 'Buy'
df.loc[df['ULT'] > 70, 'ULT_Signal'] = 'Sell'

# FI Signal
df['FI_Signal'] = 'Hold'
df.loc[df['FI'] > 0, 'FI_Signal'] = 'Buy'
df.loc[df['FI'] < 0, 'FI_Signal'] = 'Sell'

# MFI Signal
df['MFI_Signal'] = 'Hold'
df.loc[df['MFI'] < 20, 'MFI_Signal'] = 'Buy'
df.loc[df['MFI'] > 80, 'MFI_Signal'] = 'Sell'

# BOP Signal
df['BOP_Signal'] = 'Hold'
df.loc[df['BOP'] > 0, 'BOP_Signal'] = 'Buy'
df.loc[df['BOP'] < 0, 'BOP_Signal'] = 'Sell'

# EMV Signal
df['EMV_Signal'] = 'Hold'
df.loc[df['EMV'] > 0, 'EMV_Signal'] = 'Buy'
df.loc[df['EMV'] < 0, 'EMV_Signal'] = 'Sell'

# Prepare hover text that includes the price values and signals
hover_text = [
    f'Date: {date}<br>' +
    f'Price Values:<br>' +
    f'Open: {open_}<br>' +
    f'High: {high}<br>' +
    f'Low: {low}<br>' +
    f'Close: {close}<br>' +
    f'Separator:*********####*******<br>' +
    f'Indicators:<br>' +
    f'RSI(14): {rsi:.2f} - {rsi_signal}<br>' +
    f'STS(14,3): {sts:.2f} - {sts_signal}<br>' +
    f'MACD(12,26,9): {macd:.2f} - {macd_signal}<br>' +
    f'TRIX(14,9): {trix:.2f} - {trix_signal}<br>' +
    f'Williams %R(10): {williams:.2f} - {williams_signal}<br>' +
    f'CCI(14): {cci:.2f} - {cci_signal}<br>' +
    f'ROC(15): {roc:.2f} - {roc_signal}<br>' +
    f'ULT(7,14,28): {ult:.2f} - {ult_signal}<br>' +
    f'FI(13): {fi:.2f} - {fi_signal}<br>' +
    f'MFI(14): {mfi:.2f} - {mfi_signal}<br>' +
    f'BOP(14): {bop:.2f} - {bop_signal}<br>' +
    f'EMV(14): {emv:.2f} - {emv_signal}'
    for date, open_, high, low, close, rsi, sts, macd, trix, williams, cci, roc, ult, fi, mfi, bop, emv, \
    rsi_signal, sts_signal, macd_signal, trix_signal, williams_signal, cci_signal, roc_signal, ult_signal, fi_signal, mfi_signal, bop_signal, emv_signal in zip(
        df['Data'],
        df['Otwarcie'],
        df['Max'],
        df['Min'],
        df['Zamknięcie'],
        df['RSI'],
        df['STS'],
        df['MACD'],
        df['TRIX'],
        df['WILLR'],
        df['CCI'],
        df['ROC'],
        df['ULT'],
        df['FI'],
        df['MFI'],
        df['BOP'],
        df['EMV'],
        df['RSI_Signal'], 
        df['STS_Signal'], 
        df['MACD_Signal'],
        df['TRIX_Signal'],
        df['WILLR_Signal'],
        df['CCI_Signal'],
        df['ROC_Signal'],
        df['ULT_Signal'],
        df['FI_Signal'],
        df['MFI_Signal'],
        df['BOP_Signal'],
        df['EMV_Signal']
    )
]

# Create the candlestick chart for stock prices
candlestick_fig = go.Figure(data=[go.Candlestick(
    x=df['Data'],
    open=df['Otwarcie'],
    high=df['Max'],
    low=df['Min'],
    close=df['Zamknięcie'],
    hoverinfo='text',
    hovertext=hover_text  # Set the custom hover text
)])

# Update the layout of the candlestick chart
candlestick_fig.update_layout(
    title='DBE Stock Price (2019-2024)',
    yaxis_title='Price',
    xaxis_title='Date',
    xaxis_rangeslider_visible=True
)

# Update the x-axis of the candlestick chart to exclude weekends
candlestick_fig.update_xaxes(
    rangebreaks=[dict(bounds=["sat", "mon"])],  # Hide weekends
    tickformat="%Y-%m-%d"
)

# Display the candlestick chart
candlestick_fig.show()
