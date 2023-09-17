import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

N =  1000
zip_file_path = 'stock_prices.csv.zip'
stock_prices = pd.read_csv(zip_file_path, compression='zip')
#stock_prices = pd.read_csv("../input/jpx-tokyo-stock-exchange-prediction/train_files/stock_prices.csv")
stock_prices_data = pd.read_csv("stock_prices.csv")
stock_prices_temp = pd.read_csv("stock_prices.csv", nrows=N)
#stock_prices = pd.read_csv("stock_prices.csv")
#stock_list = pd.read_csv("stock_list.csv")

## start here
import py7zr



# Assuming the extracted files are named stock_prices.7z.001 and stock_prices.7z.002
file_names = ["stock_prices.7z.001", "stock_prices.7z.002"]

# Initialize an empty DataFrame to store the data
combined_df = pd.DataFrame()

# Read and concatenate the CSV files
for file_name in file_names:
    df = pd.read_csv(file_name)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# You now have the combined data in the combined_df DataFrame.
stock_list = combined_df

##end here
st.title(" :blue[Project 1:] ")
st.title(" :blue[JPX-Tokyo Stock Exchange Data] ")

st.header("Introduce the Problem")
st.write(
    """
    
    #
    The objective is to use the market data to rank the stocks. To see if theres any relation in volatility and to find if Sharpe ratio is a good ranking ratio.

    The biggest winners in the stock market are those who are able to identify solid under valued investments. One notably investor is Carl Icahn. He had a business model that involved taking a large stake in underbought companies he believed to be undervalued. He would make large profits by identifying and buying solid under valued stocks and sale his position after they became overvalued. He was labeled as a successful investor on Wall Street and a hostile activist shareholder because of his investment strategies and takeovers.

    In this analysis we will explore quantitative trading where predictions can be made. The financial data includes stock information and historical stock prices that can be analyzed. With over 2,000 stock data points we can analyze returns and movements. This will allow us rank using the Sharpe Ratio.

    Lets first start small by analyzing one stock then build from there.

    """
)

st.header("Introduce the Data")
st.write(
    """
    #
    
    
    The Data-set is from the Kaggle competition: JPX Tokyo Stock Exange Predict. 
    #
    https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/data

    The competition is described in the above link. 

    

    The data includes stock_list and different csv files:

        financials.csv
        options.csv
        secondary_stocks_prices.csv
        stock_prices.csv
        trads.csv

    Lets first load our data and do some manipulation in pandas to prepare it in a readable format.

    The Data-set contains quantitive data of 2,000 commonly traded stocks and options in the Japanese stock market. Some of the stock names include KYOKUYO CO, NIKKO EXCHANGE, and FIT Corporation from the years 2017 to 2021. Each security can be identified by a SecuritiesCode

    The columns included in the stock_price csv file:

    
            .

            RowId: Unique ID of price records
            
            Date: Trade date 
            
            SecuritiesCode: Local securities code 
            
            Open: First traded price on a day in JPY

            High: Highest traded price on a day in JPY

            Low: Lowest traded price on a day in JPY

            Close: Last traded price on a day in JPY

            Volume: Number of traded stocks on a day 
            
            AdjustmentFactor: Used to calculate price when split

            ExpectedDividend: Expected dividend value

            Target: Change ratio

    #           


    """

)
st.write(stock_prices_temp)
stock_prices.nunique()
sample_date = stock_prices.Date.unique()
st.write(sample_date)
summary_stats = stock_prices_data.describe()
st.write(summary_stats)



stock_prices["Date"] = pd.to_datetime(stock_prices["Date"])
stock_list["EffectiveDate"] = pd.to_datetime(stock_list["EffectiveDate"])
stock_list["Name"] = pd.DataFrame(stock_list["Name"])

mcd_info = stock_list[stock_list["Name"] == "McDonald's Holdings Company(Japan),Ltd."]
st.write("McDonald's Holdings Company(Japan),Ltd.", " Securities code: ", mcd_info)
tmpdf = stock_prices[stock_prices["SecuritiesCode"]==2702].reset_index(drop=True)
st.write(tmpdf.head(3))

#Currency in JPY to covert to USD to compare close amount
exchange_rate = .0068 # 1 USD to 146.78 JPY in September
jpy_at_close = tmpdf["Close"].values[0]
convert_usd = jpy_at_close * exchange_rate
st.write("Price is JPY", jpy_at_close, "Price in USD", convert_usd)


tmpdf = stock_prices[stock_prices["SecuritiesCode"] == 2702].reset_index(drop=True)

rate = 0.0068

# Function created
def jpy_to_usd(jpy, exchange_rate):
    return jpy * exchange_rate

# Columns to convert
columns_to_convert = ["Open", "High", "Low", "Close"]

# Convert JPY to USD
for column in columns_to_convert:
    tmpdf[column] = tmpdf[column].apply(lambda x: jpy_to_usd(x, rate))

st.write(tmpdf.head(3))

st.header("Pre-processing the Data")
st.write(
    """
    
    
    Lets look find a security code that relates to us:
    
    Mcdonalds is in Japan.
    The security code is 2702. It will be good to convert the price from JPY to USD so we can understand it better.
    
    
    """

)

st.write(
    """
    Lets use cardinality and correlation to elminate unuseful columns and rows

        - column RowID is in string format is not useful as SecurityCode. We can get the same information by calling this column.

        - column Date is useful since we need this to find the deviation

        - Price columns (High, Low, Open and Close) are useful but is in JPX not USD. It is also missing 7608 values. We will need to replace this by comparing it to the Volume column.

        - column Volue should have Nan for non trading days such as weekends. The missing values are related to the non trading days and can be replaced with 0 or NaN

    When Analyzing the data we should check for the number of NaN values for each column and if the Volume column contains the same number of 0's as the number of missing values in the Close column.

    We need to find a way to augment the data and replace values for the empty rows to fill Open, High, Low and Close.

    There was also some important things to consider such as the Equity Trading System failure on Oct 1, 2020 and other system failures for missing data

    pct_change()

    Pandas has a funtion that calculates the percentage of change between elements in a row from the previous row.

    Keep in mind volatility represents how large the stock prices swing around the average price. Less volitale means that the price is expected to stay around the average. There are several ways to measure volatility such as option pricing model and standard deviations of returns. 

    We also need to know the moving average which is the rolling mean or movin mean. It is the moving average that is used in time-series to capture the short-term swing while keeping up with the trends. The average can measure swings in seconds,minutes, hours and days or any selected time-frame. For our analysis we want to measure days and periods.

    
    """
)
#st.image(image3, caption=None)

st.header("Data Understanding/Visualization")
st.write(
    """
    We can visualise the data.
    Let's look at Mcdonalds stock and see the percentage of return as well as the closing price each day.
    And lets compare the amount of shares traded so we can see if it relates to the return or closing price.
    """
)

st.title("McDonald's Stock Metrics")

# Filter 
mcdonalds_train = stock_prices[stock_prices["SecuritiesCode"] == 2702]

mcdonalds_train['Close'] = mcdonalds_train['Close'].apply(lambda x: jpy_to_usd(x, rate))

# Calculate metrics
close_avg = mcdonalds_train.groupby('Date')['Close'].mean().rename('Closing Price (USD)')
returns = mcdonalds_train.groupby('Date')['Target'].mean().mul(100).rename('Average Return')
vol_avg = mcdonalds_train.groupby('Date')['Volume'].mean().rename('Volume')

# Plot the metrics for McDonald's stock using st.line_chart
st.line_chart(returns.rename('Stock Return (%)'))
st.line_chart(close_avg.rename('Closing Price (USD)'))
st.line_chart(vol_avg.rename('Shares Traded'))




st.header("Storytelling")
st.write(
    """
    The competition uses the Sharpe Ratio to evaluate and rank the 200 highest stocks.

    Sharpe Ratio is used to evaluate the daily spread of returns. Investopedia explains the Sharpe Ratio as a mathematical expression the measures risk and volatility. 

    The name comes from Economist William Sharpe in 1966 who called it a reward-to-variability ratio.

    The formula and calculation of the Sharpe Ratio:
    Return - Risk Free Rate/Theta

    
    """

)
#st.image(image5, caption=None)

st.write(
    """
    We are looking for something that has a small denominator compared to its numerator. This type of analysis is better when comparing stocks to its peers.

    The denominator is calculated by:

        Take the return variance(How far each number in a data set is from the average) from the average return in each of the incremental periods, square it, and sum the squares from all the incremental periods.

        Divide the sum by the number of incremental time periods.

        Take a square root of the quotient.

    The Sharpe Ratio can tell us the risk-adjusted relative return. It can compare a stocks historical amount relating to its benchmark to the expected variablity of the return. In other words the Sharpe Ratio compares reward to the risk.

    If we wanted to find the Sharpe Ratio for Mcdonalds holdings we would first find the average annual return and then compare it to a low-risk investment like a government bond or ETF. We would subtract rate of the bond from Mcdonalds stock rate and then divide it by the Standard Deviation rate of Mcdonalds stock. Sharpe Ratios above 1 are considered "good" and offers excess returns compared to its volatility. However investors usually compare stocks in a portfolio with those in the market sector. So if Mcdonalds is in a ETF it would be compared with stocks in the Consumer Discretionary sector in USA, but this is not the same sector in Japan.

    """
)


tmpdf['Year'] = tmpdf['Date'].dt.year
years = tmpdf.groupby('Year')['Target'].mean() * 100
yearly_avg_returns = years.to_dict()

sorted_yearly_avg_returns = dict(sorted(yearly_avg_returns.items()))
df = pd.DataFrame(list(sorted_yearly_avg_returns.items()), columns=['Year', 'Avg_return'])

st.title("Yearly Average Stock Returns (McDonald's)")

# Display the bar chart using st.bar_chart
st.bar_chart(df.set_index('Year'))


#st.image(image7, caption=None)

st.header("Impact Section")

st.write(
    """
    A strategy can be used to rank the stock using the Sharpe Ratio and seting a buy vs sell alert. The alert can get triggered if the ratio is above 1.5 and also if the price is below the historical close price.

    It will also be beneficial to keep track of trends and entry/exit timing. The trend can measure the current price relatice to the average high and low over the previous periods. The entry/exit measure the stock volume of buying and selling pressure. We can set a indicater to represent if the stock is oversold or overbought.
        
    """
)

st.write(
    """
    Sharpe Ratio is good formula but considers movement in either direction risky. In other words the Sharpe ratio creates a curve that the stock should follow and gives it a score or rank based off the closeness to that curve. Even if the price is above the curve then the rank can be skewed. Risk is assessed only off a deviation of the standard. It treats positive and negitive returns equally. Another fact about the Sharpe Ratio is uses a linear relationship meaning it expects the return to be equally impacted by the price. In reality investors consider the upside potential when buying stocks and other securites. Investors will buy volitile stocks with the potential of higher returns. An investor may ignore the ratio and sell, just so they can cut their loses. There are other variations of the Sharpe Ratio called Sortino Ratio that ignores the above-average returns and focus on the downside deviation to handle risk.

    """
)

mcdonalds_data = stock_prices[stock_prices["SecuritiesCode"] == 2702]
mcdonalds_data['Returns'] = mcdonalds_data['Close'].pct_change()

risk_free_rate = 0.02
time_periods = [1, 2]  # in years
sharpe_ratios = []

for period in time_periods:
    annualized_return = mcdonalds_data['Returns'].mean() * 252  # 252 trading days in a year
    annualized_std_dev = mcdonalds_data['Returns'].std() * (252 ** 0.5)  # Annualized standard deviation

    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_std_dev
    sharpe_ratios.append(sharpe_ratio)

sharpe_df = pd.DataFrame({'Time Period (Years)': time_periods, 'Sharpe Ratio': sharpe_ratios})

# Create a Streamlit app
st.title("McDonald's Stock Sharpe Ratios")

# Display the Sharpe ratios using st.line_chart
st.line_chart(sharpe_df.set_index('Time Period (Years)'))


st.header("References")
st.write(
    """
    https://www.investopedia.com/terms/s/sharperatio.asp

    https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/overview

    https://medium.com/codex/algorithmic-trading-with-relative-strength-index-in-python-d969cf22dd85

    https://www.investopedia.com/terms/m/macd.asp

    https://www.educba.com/moving-average-formula/

    https://www.alphacodingskills.com/pandas/notes/pandas-function-dataframe-pct-change.php

    https://www.kaggle.com/code/onurkoc83/technical-features-trading-strategy

    https://www.kaggle.com/code/ikeppyo/examples-of-higher-scores-than-perfect-predictions
    
    """
)
st.header("Code")
st.write("**https://github.com/Tower-Babel/project1/blob/main/online/jpx-stockprices.ipynb**")

