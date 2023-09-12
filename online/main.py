import streamlit as st
from PIL import Image

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
image1 = Image.open("online/img_1.jpg")
image2 = Image.open("online/img_2.jpg")
image3 = Image.open("online/img_3.jpg")
image4 = Image.open("online/img_4.jpg")
image5 = Image.open("online/img_5.jpg")
image6 = Image.open("online/img_6.jpg")
image7 = Image.open("online/img_7.jpg")

st.image(image1, caption=None)
st.image(image2, caption=None)

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
st.image(image3, caption=None)

st.header("Data Understanding/Visualization")
st.write(
    """
    We can visualise the data.
    Let's look at Mcdonalds stock and see the percentage of return as well as the closing price each day.
    And lets compare the amount of shares traded so we can see if it relates to the return or closing price.
    """
)
st.image(image4, caption=None)

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
st.image(image5, caption=None)

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

st.image(image6, caption=None)


st.image(image7, caption=None)

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
st.write("https://github.com/Tower-Babel/project1/blob/main/online/jpx-stockprices.ipynb")
