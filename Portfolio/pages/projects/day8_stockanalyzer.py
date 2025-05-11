import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
sns.set()

# Fix yfinance import
import yfinance as yf

# Download S&P 500 data with correct syntax
raw_data = yf.download(
    tickers="^GSPC", 
    start="1994-01-07", 
    end=datetime.today().strftime('%Y-%m-%d'),  # Use today's date
    interval="1d"
)

# Create a copy of data with a 'Price' column for our technical indicators
data = raw_data.copy()
data['Price'] = data['Close']

# SMA Calculation
def calculate_sma(data, window):
    return data['Price'].rolling(window=window).mean()

# EMA Calculation
def calculate_ema(data, window):
    return data['Price'].ewm(span=window, adjust=False).mean()

# RSI Calculation
def calculate_rsi(data, window):
    delta = data['Price'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = pd.Series(gain).rolling(window=window).mean()
    avg_loss = pd.Series(loss).rolling(window=window).mean()
    
    # Handle division by zero
    avg_loss = avg_loss.replace(0, 0.00001)  
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return pd.Series(rsi, index=data.index)

# Bollinger Bands Calculation
def calculate_bollinger_bands(data, window):
    sma = data['Price'].rolling(window=window).mean()
    std_dev = data['Price'].rolling(window=window).std()
    upper_band = sma + (std_dev * 2)
    lower_band = sma - (std_dev * 2)
    return sma, upper_band, lower_band

# MACD Calculation
def calculate_macd(data):
    ema_12 = data['Price'].ewm(span=12, adjust=False).mean()
    ema_26 = data['Price'].ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# Calculate daily returns and cumulative returns
data['Daily_Return'] = data['Price'].pct_change()
data['Cumulative_Return'] = (1 + data['Daily_Return']).cumprod()

# Apply all technical indicators
data['SMA_20'] = calculate_sma(data, 20)
data['SMA_50'] = calculate_sma(data, 50)
data['SMA_200'] = calculate_sma(data, 200)
data['EMA_20'] = calculate_ema(data, 20)
data['RSI_14'] = calculate_rsi(data, 14)
data['MACD'], data['Signal'] = calculate_macd(data)
data['MACD_Histogram'] = data['MACD'] - data['Signal']
sma_20, data['Upper_Band'], data['Lower_Band'] = calculate_bollinger_bands(data, 20)

# Create subplots for different indicators
fig, axs = plt.subplots(4, 1, figsize=(16, 20), gridspec_kw={'height_ratios': [3, 1, 1, 1]})

# Plot 1: Price with SMAs and Bollinger Bands
axs[0].plot(data.index, data['Price'], label='S&P 500', color='blue', linewidth=1)
axs[0].plot(data.index, data['SMA_20'], label='SMA 20', color='orange', linewidth=0.8)
axs[0].plot(data.index, data['SMA_50'], label='SMA 50', color='green', linewidth=0.8)
axs[0].plot(data.index, data['SMA_200'], label='SMA 200', color='red', linewidth=0.8)
axs[0].plot(data.index, data['Upper_Band'], label='Upper Band', color='gray', linestyle='--', linewidth=0.8)
axs[0].plot(data.index, data['Lower_Band'], label='Lower Band', color='gray', linestyle='--', linewidth=0.8)
axs[0].fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='gray', alpha=0.1)
axs[0].set_title('S&P 500 with Technical Indicators (1994-Present)', fontsize=16)
axs[0].set_ylabel('Price', fontsize=12)
axs[0].legend()
axs[0].grid(True)

# Plot 2: Volume
axs[1].bar(data.index, data['Volume'], color='blue', alpha=0.5)
axs[1].set_ylabel('Volume', fontsize=12)
axs[1].grid(True)

# Plot 3: RSI
axs[2].plot(data.index, data['RSI_14'], label='RSI (14)', color='purple', linewidth=1)
axs[2].axhline(y=70, color='red', linestyle='--', alpha=0.5)
axs[2].axhline(y=30, color='green', linestyle='--', alpha=0.5)
axs[2].set_ylabel('RSI', fontsize=12)
axs[2].set_ylim(0, 100)
axs[2].grid(True)

# Plot 4: MACD
axs[3].plot(data.index, data['MACD'], label='MACD', color='blue', linewidth=1)
axs[3].plot(data.index, data['Signal'], label='Signal Line', color='red', linewidth=1)
axs[3].bar(data.index, data['MACD_Histogram'], label='MACD Histogram', color='green', alpha=0.5)
axs[3].set_ylabel('MACD', fontsize=12)
axs[3].set_xlabel('Date', fontsize=12)
axs[3].legend()
axs[3].grid(True)

plt.tight_layout()
plt.savefig('sp500_technical_analysis.png', dpi=300, bbox_inches='tight')  # Save high-res image
plt.show()

# Create a zoomed in view of the last 2 years
recent_years = 2
recent_data = data.iloc[-252*recent_years:]  # Approximately 252 trading days per year

fig, axs = plt.subplots(4, 1, figsize=(16, 20), gridspec_kw={'height_ratios': [3, 1, 1, 1]})

# Plot 1: Price with SMAs and Bollinger Bands (recent)
axs[0].plot(recent_data.index, recent_data['Price'], label='S&P 500', color='blue', linewidth=1.5)
axs[0].plot(recent_data.index, recent_data['SMA_20'], label='SMA 20', color='orange', linewidth=1)
axs[0].plot(recent_data.index, recent_data['SMA_50'], label='SMA 50', color='green', linewidth=1)
axs[0].plot(recent_data.index, recent_data['SMA_200'], label='SMA 200', color='red', linewidth=1)
axs[0].plot(recent_data.index, recent_data['Upper_Band'], label='Upper Band', color='gray', linestyle='--', linewidth=1)
axs[0].plot(recent_data.index, recent_data['Lower_Band'], label='Lower Band', color='gray', linestyle='--', linewidth=1)
axs[0].fill_between(recent_data.index, recent_data['Lower_Band'], recent_data['Upper_Band'], color='gray', alpha=0.1)
axs[0].set_title(f'S&P 500 with Technical Indicators (Last {recent_years} Years)', fontsize=16)
axs[0].set_ylabel('Price', fontsize=12)
axs[0].legend()
axs[0].grid(True)

# Plot 2: Volume (recent)
axs[1].bar(recent_data.index, recent_data['Volume'], color='blue', alpha=0.5)
axs[1].set_ylabel('Volume', fontsize=12)
axs[1].grid(True)

# Plot 3: RSI (recent)
axs[2].plot(recent_data.index, recent_data['RSI_14'], label='RSI (14)', color='purple', linewidth=1.5)
axs[2].axhline(y=70, color='red', linestyle='--', alpha=0.5)
axs[2].axhline(y=30, color='green', linestyle='--', alpha=0.5)
axs[2].set_ylabel('RSI', fontsize=12)
axs[2].set_ylim(0, 100)
axs[2].grid(True)

# Plot 4: MACD (recent)
axs[3].plot(recent_data.index, recent_data['MACD'], label='MACD', color='blue', linewidth=1.5)
axs[3].plot(recent_data.index, recent_data['Signal'], label='Signal Line', color='red', linewidth=1)
axs[3].bar(recent_data.index, recent_data['MACD_Histogram'], label='MACD Histogram', color='green', alpha=0.5)
axs[3].set_ylabel('MACD', fontsize=12)
axs[3].set_xlabel('Date', fontsize=12)
axs[3].legend()
axs[3].grid(True)

plt.tight_layout()
plt.savefig('sp500_recent_technical_analysis.png', dpi=300, bbox_inches='tight')  # Save high-res image
plt.show()

# Display performance metrics and summary statistics
print("S&P 500 Performance Summary")
print("===========================")

# Calculate overall performance
total_days = len(data)
total_years = total_days / 252  # Approximate trading days in a year
total_return = (data['Price'].iloc[-1] / data['Price'].iloc[0] - 1) * 100
annualized_return = ((1 + total_return/100) ** (1/total_years) - 1) * 100
volatility = data['Daily_Return'].std() * np.sqrt(252) * 100
max_drawdown = ((data['Price'] / data['Price'].cummax()) - 1).min() * 100
sharpe_ratio = annualized_return / volatility

print(f"\nLong-Term Performance (1994-Present):")
print(f"Total Return: {total_return:.2f}%")
print(f"Annualized Return: {annualized_return:.2f}%")
print(f"Annualized Volatility: {volatility:.2f}%")
print(f"Maximum Drawdown: {max_drawdown:.2f}%")
print(f"Sharpe Ratio (Rf=0): {sharpe_ratio:.2f}")

# Decade-by-decade performance
print("\nPerformance by Decade:")
decades = [
    ("1990s", "1994-01-01", "1999-12-31"),
    ("2000s", "2000-01-01", "2009-12-31"),
    ("2010s", "2010-01-01", "2019-12-31"),
    ("2020s", "2020-01-01", datetime.today().strftime('%Y-%m-%d'))
]

for decade in decades:
    decade_name, start_date, end_date = decade
    try:
        decade_data = data.loc[start_date:end_date]
        if len(decade_data) > 0:
            decade_return = (decade_data['Price'].iloc[-1] / decade_data['Price'].iloc[0] - 1) * 100
            decade_years = len(decade_data) / 252
            decade_annual_return = ((1 + decade_return/100) ** (1/decade_years) - 1) * 100
            decade_vol = decade_data['Daily_Return'].std() * np.sqrt(252) * 100
            decade_drawdown = ((decade_data['Price'] / decade_data['Price'].cummax()) - 1).min() * 100
            
            print(f"\n{decade_name}:")
            print(f"  Total Return: {decade_return:.2f}%")
            print(f"  Annualized Return: {decade_annual_return:.2f}%")
            print(f"  Volatility: {decade_vol:.2f}%")
            print(f"  Maximum Drawdown: {decade_drawdown:.2f}%")
            print(f"  Sharpe Ratio: {decade_annual_return / decade_vol:.2f}")
    except Exception as e:
        print(f"Error processing {decade_name}: {e}")

# Recent performance
print("\nRecent Performance:")
for period, days in [("1 Month", 22), ("3 Months", 66), ("6 Months", 126), ("1 Year", 252), ("YTD", None)]:
    try:
        if days:
            period_data = data.iloc[-days:]
        else:  # YTD
            start_of_year = f"{datetime.today().year}-01-01"
            period_data = data.loc[start_of_year:]
            
        period_return = (period_data['Price'].iloc[-1] / period_data['Price'].iloc[0] - 1) * 100
        
        print(f"{period}: {period_return:.2f}%")
    except Exception as e:
        print(f"Error processing {period}: {e}")

# Current technical status
latest = data.iloc[-1]
print("\nCurrent Technical Indicators:")
print(f"Price: ${latest['Price']:.2f}")
print(f"SMA 20: ${latest['SMA_20']:.2f} (Price is {'above' if latest['Price'] > latest['SMA_20'] else 'below'})")
print(f"SMA 50: ${latest['SMA_50']:.2f} (Price is {'above' if latest['Price'] > latest['SMA_50'] else 'below'})")
print(f"SMA 200: ${latest['SMA_200']:.2f} (Price is {'above' if latest['Price'] > latest['SMA_200'] else 'below'})")
print(f"RSI (14): {latest['RSI_14']:.2f} ({'Overbought' if latest['RSI_14'] > 70 else 'Oversold' if latest['RSI_14'] < 30 else 'Neutral'})")
print(f"MACD: {latest['MACD']:.4f}")
print(f"Signal: {latest['Signal']:.4f}")
print(f"MACD Histogram: {latest['MACD_Histogram']:.4f} ({'Bullish' if latest['MACD_Histogram'] > 0 else 'Bearish'})")
print(f"Bollinger Bands: ${latest['Lower_Band']:.2f} - ${latest['Upper_Band']:.2f}")
print(f"  Position: {('Above upper band' if latest['Price'] > latest['Upper_Band'] else 'Below lower band' if latest['Price'] < latest['Lower_Band'] else 'Within bands')}")

# Generate trading signals
print("\nTechnical Analysis Summary:")
signals = []

# RSI signals
if latest['RSI_14'] < 30:
    signals.append("Oversold (RSI < 30)")
elif latest['RSI_14'] > 70:
    signals.append("Overbought (RSI > 70)")

# MACD signals
if latest['MACD'] > latest['Signal'] and latest['MACD_Histogram'] > 0:
    signals.append("Bullish MACD crossover")
elif latest['MACD'] < latest['Signal'] and latest['MACD_Histogram'] < 0:
    signals.append("Bearish MACD crossover")

# Bollinger Bands signals
if latest['Price'] > latest['Upper_Band']:
    signals.append("Price above upper Bollinger Band (potential reversal)")
elif latest['Price'] < latest['Lower_Band']:
    signals.append("Price below lower Bollinger Band (potential reversal)")

# SMA signals
if latest['Price'] > latest['SMA_20'] > latest['SMA_50'] > latest['SMA_200']:
    signals.append("Strong bullish trend (Price > SMA20 > SMA50 > SMA200)")
elif latest['Price'] < latest['SMA_20'] < latest['SMA_50'] < latest['SMA_200']:
    signals.append("Strong bearish trend (Price < SMA20 < SMA50 < SMA200)")
elif latest['Price'] > latest['SMA_20'] and latest['Price'] > latest['SMA_50']:
    signals.append("Bullish trend (Price above major moving averages)")
elif latest['Price'] < latest['SMA_20'] and latest['Price'] < latest['SMA_50']:
    signals.append("Bearish trend (Price below major moving averages)")

# Golden/Death Cross
if data['SMA_50'].iloc[-20:].lt(data['SMA_200'].iloc[-20:]).any() and latest['SMA_50'] > latest['SMA_200']:
    signals.append("Recent Golden Cross (SMA50 crossing above SMA200)")
elif data['SMA_50'].iloc[-20:].gt(data['SMA_200'].iloc[-20:]).any() and latest['SMA_50'] < latest['SMA_200']:
    signals.append("Recent Death Cross (SMA50 crossing below SMA200)")

if signals:
    for signal in signals:
        print(f"- {signal}")
else:
    print("No strong trading signals detected currently")