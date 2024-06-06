import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_data(ticker, period='1y'):
    stock_data = yf.download(ticker, period=period)
    return stock_data

def calculate_rsi(data, window=14):
    delta = data['Adj Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def momentum_trading_strategy(data, rsi_buy=30, rsi_sell=70):
    data['RSI'] = calculate_rsi(data)
    data['Signal'] = 0
    data['Signal'][data['RSI'] < rsi_buy] = 1
    data['Signal'][data['RSI'] > rsi_sell] = -1
    data['Position'] = data['Signal'].diff()
    return data

def backtest_strategy(data, initial_balance=10000):
    balance = initial_balance
    shares = 0
    for i in range(len(data)):
        if data['Position'][i] == 1:  # Buy signal
            shares = balance / data['Adj Close'][i]
            balance = 0
        elif data['Position'][i] == -1:  # Sell signal
            balance = shares * data['Adj Close'][i]
            shares = 0

    # Calculate final portfolio value
    if shares > 0:
        balance = shares * data['Adj Close'][-1]
    
    return balance

def main():
    ticker = 'AAPL'
    stock_data = get_stock_data(ticker)
    strategy_data = momentum_trading_strategy(stock_data)
    
    final_balance = backtest_strategy(strategy_data)
    print(f'Final portfolio value: ${final_balance:.2f}')

if __name__ == "__main__":
    main()