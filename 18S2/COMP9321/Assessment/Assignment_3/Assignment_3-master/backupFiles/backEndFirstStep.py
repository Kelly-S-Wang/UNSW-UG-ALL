import pandas as pd
import requests
import json
from pymongo import MongoClient

def read_csv(csv_file):
    """
    To get housing price data, the source is stored as csv file
    1.read this csv file
    2.trasfer the csv file into datafram format
    """
    return pd.read_csv(csv_file)


def clean_dataframe(dataframe, print_column=True, print_rows=True):
	"""
	1.construte a datafram and rebuild the data
	2.filter the data that invalid or not needed.
	"""

    # print column names
    if print_column:
        print(",".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))

def classifation(dataframe):
	"""
	classify the datafram into two part, one for trainning, another one for prediction
	"""
    dataframe['Place of Publication'] = dataframe['Place of Publication'].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' '))

    new_date = dataframe['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    dataframe['Date of Publication'] = new_date

    return dataframe

def write_in_csv(dataframe, file):
    """
    the new datafrdame which must be written into a csv file
    """
    dataframe.to_csv(file, sep=',', encoding='utf-8')


