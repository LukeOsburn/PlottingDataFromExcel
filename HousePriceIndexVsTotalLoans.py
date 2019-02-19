import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import seaborn as sns

#Lets make a plot of total home loans from the Big Four Australian Banks
#Versus a capital weighted housing index

#We will use these data
HouseIndex= pd.read_excel("641601.xls", "Data1")

banks=pd.read_excel("monthly_banking_statistics_december_2018_back_series.xlsx", "Table 1") #This is a very large spreadsheet with many details from all Aussie banks
#banks=pd.read_excel("TEST.xlsx", "Sheet1") #Use this smaller version of the data for testing, runs much quicker

#what does the data look like?
print(HouseIndex.shape)
print(HouseIndex.columns.values)

#Select the part we wnat
HI=HouseIndex[['Residential Property Price Index ;  Weighted average of eight capital cities ;']]
print(HI)
print("This is what we want, a data frame with 2 columns, dates and house price index")

#what does the data look like?
print(banks.head())
print(banks.columns.values)


#Institutions=banks.loc[:,['Institution Name']]
Institutions=banks[['Institution Name']]
print(Institutions)
print("There are a lot of instiutions here but we only want the big four")
print("Going to have to filter")

#Drop missing values, should there be any
Institutions=Institutions.dropna()

#print("banks header")
#print(banks.head())

print("Use groupby and get_group to create dataframes with only the selected instiutions")

Institutions=banks.groupby('Institution Name', as_index=False)

ANZ=Institutions.get_group('Australia and New Zealand Banking Group Limited')
CBA=Institutions.get_group('Commonwealth Bank of Australia')
NAB=Institutions.get_group('National Australia Bank Limited')
WEST=Institutions.get_group('Westpac Banking Corporation')

#Lets look at what the data now looks like
print(ANZ)

print("Excellent, we have our data frames filtered by the institutions we want")
print("Now lets only select the columns we want")
print(ANZ.columns.values)

ANZ=ANZ[['Date','Owner','Investor']]
CBA=CBA[['Date','Owner','Investor']]
NAB=NAB[['Date','Owner','Investor']]
WEST=WEST[['Date','Owner','Investor']]

#Lets look at what the data now looks like
print(ANZ)

print("We want total loans, so add owner and investor loans together")
print("This creates a new column to our dataframe")
ANZ['ANZ Total Loans']=ANZ['Owner']+ANZ['Investor']
CBA['CBA Total Loans']=CBA['Owner']+CBA['Investor']
NAB['NAB Total Loans']=NAB['Owner']+NAB['Investor']
WEST['WEST Total Loans']=WEST['Owner']+WEST['Investor']

print("Lets set our index as date, will make plotting much eaiser")
ANZ=ANZ.set_index('Date')
CBA=CBA.set_index('Date')
NAB=NAB.set_index('Date')
WEST=WEST.set_index('Date')
HI.index = pd.to_datetime(HI.index)

#Lets look at what the data now looks like
print(ANZ)

BigFour= ANZ['ANZ Total Loans'] + CBA['CBA Total Loans']+WEST['WEST Total Loans']+NAB['NAB Total Loans']


print("Now we have total loans of the big four banks in a single column by year!")
print(BigFour)

print("Fantastic lets plots Total loans by the big four versus housing price index!")
fig = plt.figure(1, figsize=(6,6))
ax = fig.add_subplot(111)
ax.plot(BigFour,color='r')
ax.set_ylabel("Big Four Total Home Loans, $m",fontsize=14,color='r')

ax2 = ax.twinx()
ax2.plot(HI,color='g')
ax2.set_ylabel("Capital Weighted Housing Index",fontsize=14,color='g')
ax.set_xlabel('Year', fontsize=14, color='black')

plt.savefig('TotalloansVsHousePriceIndex.png', format='png', bbox_inches="tight")
