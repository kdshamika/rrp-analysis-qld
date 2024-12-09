"""

This Python code analyses quarterly regional retail electricity prices for Queensland (QLD). 
It examines price changes across different time periods, including daytime, evening and morning peak hours, as well as the solar period.
"""

#%% ----------------- Libraries -----------------------------
# Import numpy
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% ----------------- Set working directory and load files -----------------------------
# get the current working directory
working_dir = os.getcwd()  

# load prices
# these are prices which are the average of the trading intervals in each half hour, unit $/MWh
file_name_prices = 'QLD_Prices_CY21-CY23.csv'
file_path_prices = os.path.join(working_dir, file_name_prices)
prices = pd.read_csv(file_path_prices)

#%%
"""
Examine the prices DataFrame: Investigate the data over the given time period, focusing on the IndexTerm column. 

"""

# explore prices dataframe
print(prices.head())
print(prices.info())

print(prices.describe())

# convert SETTLEMENTDATE to datetime
prices['SETTLEMENTDATE'] = pd.to_datetime(prices['SETTLEMENTDATE'])  
prices.set_index('SETTLEMENTDATE', inplace=True)  # Set as index                   

# null values
def calculate_null_values(df):
    """
    Calculate and display the number of null values in each column of the dataframe.
    
    Input Parameters: dataframe to analyse       
    Output: a series showing the count of null values for each column
    """
    null_counts = df.isnull().sum()
    return null_counts
calculate_null_values(prices)

# print unique quarters
print(prices['IndexTerm'].unique())

# group by Year and calculate the count of records where each period is active (value = 1)
period_counts = prices.groupby('Year')[['Solar_Period', 'Evening_Peak', 'Morning_Peak']].sum()
print(period_counts)

# Plot the time series data
plt.figure(figsize=(10, 6))
prices['RRP'].plot(figsize=(10, 6), alpha=0.7)
plt.title("Time Series of Electricity Prices ")
plt.xlabel("Date")
plt.ylabel("Price ($/Mwh")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()


"""

Identify any unusual patterns or anomalies in the dataset. 
Explore potential reasons or events that may have caused these irregularities.

"""

# descriptive statistics of RRP by IndexTerm
descriptive_stats = prices.groupby('IndexTerm')['RRP'].describe()
print(descriptive_stats)
    
# figure 1: plot avg rrp for each quarter
# group by IndexTerm and calculate the average RRP for each quarter
avg_quarterly_price = prices.groupby('IndexTerm')['RRP'].mean()

# plott the quarterly price
plt.figure(figsize=(10, 6))

# plot the data as a line chart
avg_quarterly_price.plot(ax=plt.gca(), linestyle='-', marker='o', legend=True)

# customising the plot
plt.title('Average Quarterly Price by IndexTerm')
plt.xlabel('IndexTerm')
plt.ylabel('Average RRP ($/MWh)')
# ensure that all index terms (xticks) are shown on the x-axis
plt.xticks(ticks=np.arange(len(avg_quarterly_price)), labels=avg_quarterly_price.index, rotation=45)
plt.tight_layout()
plt.show()


# figure 2: Boxplots of RRP for IndexTerm
plt.figure(figsize=(12, 6))

# create a boxplot of RRP for each IndexTerm (quarter) where Evening Peak is active
sns.boxplot(x='IndexTerm', y='RRP', data=prices, palette='Set2')

# customise the plot
plt.title('Boxplot for RRP by IndexTerm')
plt.xlabel('IndexTerm')
plt.ylabel('RRP ($/MWh)')
plt.xticks(rotation=45)  
plt.tight_layout()
plt.show()

"""

Analyse price behaviour in different periods: Assess and compare electricity prices across the three distinct time periods: Evening Peak, Solar Period, and Morning Peak. 
Provide insights into the trends, variations, or notable differences observed in these time frames.

"""

# figure 3: plot average RRP by IndexTerm and periods (Evening_Peak, Solar_Period, Morning_Peak)
# filter data for Evening Peak
evening_peak_data = prices[prices['Evening_Peak'] == 1]
avg_evening_peak = evening_peak_data.groupby('IndexTerm')['RRP'].mean()

# filter data for Solar Period
solar_period_data = prices[prices['Solar_Period'] == 1]
avg_solar_period = solar_period_data.groupby('IndexTerm')['RRP'].mean()

# filter data for Morning Peak
morning_peak_data = prices[prices['Morning_Peak'] == 1]
avg_morning_peak = morning_peak_data.groupby('IndexTerm')['RRP'].mean()

# Plotting the average RRP for each period by quarter
plt.figure(figsize=(12, 6))

# Plot each period with a different line
plt.plot(avg_evening_peak, linestyle='-', marker='o', label='Evening Peak')
plt.plot(avg_solar_period, linestyle='-', marker='o', label='Solar Period')
plt.plot(avg_morning_peak, linestyle='-', marker='o', label='Morning Peak')

# customise the plot
plt.title('Average RRP by Period and IndexTerm')
plt.xlabel('IndexTerm')
plt.ylabel('Average RRP ($/MWh)')
plt.xticks(rotation=45)  
plt.legend(title='Period') 
plt.tight_layout()
plt.show()


# figure 4: boxplots for average RRP by IndexTerm and periods (Evening_Peak, Solar_Period, Morning_Peak)
# add a new column 'Period' to indicate the period
evening_peak_data['Period'] = 'Evening Peak'
solar_period_data['Period'] = 'Solar Period'
morning_peak_data['Period'] = 'Morning Peak'

# concatenate all the dataframes into one dataframe
all_periods_data = pd.concat([evening_peak_data, solar_period_data, morning_peak_data])

# plotting boxplots for each period by quarter (IndexTerm)
plt.figure(figsize=(14, 7))

# create a boxplot for each period by IndexTerm (quarter)
sns.boxplot(x='IndexTerm', y='RRP', hue='Period', data=all_periods_data, palette='Set2')

# customize the plot
plt.title('Boxplot of RRP for Each Period by Quarter (IndexTerm)')
plt.xlabel('Quarter (IndexTerm)')
plt.ylabel('RRP ($/MWh)')
plt.xticks(rotation=45) 
plt.tight_layout()
plt.show()


# Calculate descriptive statistics (mean, median, min, max, std) for RRP by Period and IndexTerm
descriptive_stats_by_period_indexterm = (
    all_periods_data.groupby(['Period', 'IndexTerm'])['RRP']
    .agg(['mean', 'median', 'min', 'max', 'std'])
    .reset_index()
)

# Pivot the data for better readability
pivot_table = descriptive_stats_by_period_indexterm.pivot(
    index='IndexTerm', 
    columns='Period', 
    values=['mean', 'median', 'min', 'max', 'std']
)

# Display the table with rounded values for easier readability
print(pivot_table.round(2))

