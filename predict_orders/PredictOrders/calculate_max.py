import pandas as pd 
import numpy as np 
import math
from datetime import datetime
import warnings 
warnings.filterwarnings('ignore')


def read_data(input_df):
    # df = pd.read_csv(path, header=None)
    # columns = ['IdHdr', 'IdClient', 'ClientName', 'Amount', 'DscItem',
    #            'IdItem', 'Date', 'ItemType', 'IdItemType', 'min']
    # input_df.columns = columns
    input_df['Date'] = pd.to_datetime(input_df['Date'], format='%Y-%m-%d %H:%M:%S.%f')
    input_df['Date'] = input_df["Date"].dt.date
    # sort values base on date column 
    df = input_df.sort_values(by='Date')
    return df


def make_period_time(df: pd.DataFrame, days:int=91):
    now = datetime.today().date()
    df['Now'] = now
    df['Now'] = pd.to_datetime(df['Now'])
    # now = pd.to_datetime('2023-11-24')
    # now = now.date()
    df['Date'] = pd.to_datetime(df['Date'])
    # print(df.info())
    df['Recently'] = df['Now'] - df['Date']

    def make_true(column):
        if column.days > days:
            return False
        else:
            return True
    
    df['Assess'] = df['Recently'].apply(make_true)
    df1 = df[df['Assess'] == True]
    return df1 


def calculate_max_orders(period_df: pd.DataFrame, std_criterion:float=2):
    list_names = period_df['ClientName'].unique()
    list_items = period_df['DscItem'].unique()
    
    period_df['Mean'] = 0.
    period_df['Std'] = 0.
    for name in list_names[0:]:
        for item in list_items[0:]:
            if item in (period_df[period_df['ClientName'] == name]['DscItem'].unique()):
                items = period_df[(period_df['ClientName']==name) & (period_df['DscItem']==item)]['Amount']
                mean = items.mean()
                std = items.std()
                period_df.loc[(period_df['ClientName'] == name) & (period_df['DscItem'] == item), 'Mean'] = mean
                period_df.loc[(period_df['ClientName'] == name) & (period_df['DscItem'] == item), 'Std'] = std
    
    period_df['Std'] = period_df['Std'].fillna(0)
    period_df['StdCriterion'] = std_criterion
    period_df['Max'] = (period_df['Std'] * period_df['StdCriterion']) + period_df['Mean']
    period_df['Max'] = period_df['Max'].apply(lambda x: math.ceil(x))
    
    return period_df


def find_max(dataframe: pd.DataFrame):
    df = read_data(dataframe)
    period_df = make_period_time(df)
    last_df = calculate_max_orders(period_df, std_criterion=2.0)
    # max_value = last_df[(last_df['IdClient']==id_client) & (last_df['IdItem']==id_item)]['Max']
    # max_value = max_value.iloc[-1]
    max_df = last_df[['IdClient', 'IdItem', 'IdItemType', 'min', 'Std', 'StdCriterion', 'Max']]
    max_df = max_df.drop_duplicates()
    # max_df.sort_values(by=max_df['IdClient'])
    return max_df


# print(find_max(id_client=21707222, id_item=1183701))
# max_df = find_max()
# print(max_df)
