import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle

import os

pd.set_option('expand_frame_repr', False)

def clean(df):
    global good_suburb
    # Drop row with Na
    df = df[['Suburb','Price', 'Landsize']].dropna()
    # Keep rows where all values are not equal to 0
    df = df[(df != 0).all(1)]
    # Keep rows where 'Landsize' <= 250
    df = df[df['Landsize'] <= 250]
    suburb_group = df.groupby('Suburb').filter(lambda x: len(x) > 70).groupby('Suburb')

    good_suburb = []
    for key, item in suburb_group:
        good_suburb.append(key)
    df = df.loc[df['Suburb'].isin(good_suburb)]
    df.reset_index(drop=True)
    df.index = range(len(df.index))
    #df.to_csv('cleaned.csv')
    return df


# input arg df: df return by clean(df)
# input arg input_sub: suburb that customer inputing
def get_suburb_data(df,input_sub):
    df = df.groupby(['Suburb'])
    df = df.get_group(input_sub)
    df.reset_index(drop=True)
    df.index = range(len(df.index))
    return df

def predict(input_sub,input_size):
        csv_file = 'Melbourne_housing_FULL.csv'
        df = pd.read_csv(csv_file)
        df = clean(df)
        suburb_df = get_suburb_data(df,input_sub)

        datasets_X = suburb_df['Landsize'].tolist()
        datasets_Y = suburb_df['Price'].tolist()

        length =len(datasets_X)
        datasets_X= np.array(datasets_X).reshape([length,1])
        datasets_Y=np.array(datasets_Y)

        minX =min(datasets_X)
        maxX =max(datasets_X)
        X=np.arange(minX,maxX).reshape([-1,1])

        linear =linear_model.LinearRegression()
        linear.fit(datasets_X,datasets_Y)
        # return y which is the predict_price  y = a*x + b
        y = linear.coef_ * input_size + linear.intercept_
        y = round(float(y),2)

        # data visilation
        plt.scatter(datasets_X,datasets_Y,color='red')
        plt.plot(X,linear.predict(X),color='blue')
        plt.xlabel('Landsize')
        plt.ylabel('Price')
        plt.title(input_sub)
        #plt.show()
        if not os.path.isfile('./' + input_sub + '.png'):
            plt.savefig('{}.png'.format(input_sub))
        
        return y
# print(predict('Brunswick',123))
''' Showing how to use my predict() fuction
    $ pwd
    $ python3
    >> from predict import *
    >> predict_price = predict('Richmond', 100)
    >> print('predict_price = ', predict_price)
    >> predict_price = 115000.00

    $ pwd
    $ ls
    and you will see there is a picture file saved, named "Richmond.pdf"
'''
