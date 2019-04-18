import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle

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
        #print(key) # key is all suburb name which has more than 80 rows
        good_suburb.append(key)

    # print('*****************************************')
    # print('good_suburb = ',good_suburb)
    # print('How many good_suburb above ?', len(good_suburb))
    # print('*****************************************')
    # Only keep those suburbs over 70 rows data and reset index
    df = df.loc[df['Suburb'].isin(good_suburb)]
    # Reset index start from 0
    df.reset_index(drop=True)
    df.index = range(len(df.index))
    #print(df)
    # return 的是数据 是只保留哪些有足够数据的区
    return df


# input arg df: df return by clean(df)
# input arg input_sub: suburb that customer inputing
def get_suburb_data(df,input_sub):
    df = df.groupby(['Suburb'])
    df = df.get_group(input_sub)
    df.reset_index(drop=True)
    df.index = range(len(df.index))
    #print(df)
    return df

    # 利用 Numpy 的函数定义训练并返回多项式回归模型的函数
    # deg 参数代表着模型参数中的 n, 即模型中多项式的次数
    # 返回的模型能够根据输入的 x (默认是 x0), 返回相应的预测的y
def get_model(deg):
    return lambda input_x=x0: np.polyval(np.polyfit(x, y, deg), input_x)
    # 模型做好以后 根据参数 n, 输入 x,y 返回相对应的损失
def get_cost(deg, input_x, input_y):
    return 0.5 * ((get_model(deg)(input_x) - input_y) ** 2).sum()


if __name__ == "__main__":
    csv_file = 'Melbourne_housing_FULL.csv'
    df = pd.read_csv(csv_file)

    df = clean(df)
    # print(df)
    # print(df.groupby('Suburb').size())
    # df.to_csv('cleanedDF.csv')

    # assume customer input a suburb = 'Port Melbourne'
    # input suburb
    input_sub = 'Richmond'
    suburb_df = get_suburb_data(df,input_sub)
    #suburb_df.to_csv('suburb_data.csv')
    ax = suburb_df.plot.scatter(x='Landsize', y='Price', label= input_sub, color = 'green')
    #plt.show()

    # x is list of landsize , y is list of price (float)
    x = suburb_df['Landsize'].tolist()
    y = suburb_df['Price'].tolist()
    #print(x,y)
    # 读取完数据后, 将他们转化为Numpy数组方便进一步的处理
    x,y = np.array(x), np.array(y)
    # 标准化
    x = ( x - x.mean() ) / x.std()
    # 将原始数据以散点图的形式画出
    plt.figure()
    plt.scatter(x,y, c='g', s=20)
    plt.show()

    # 在(-2,2) 这个区间上取100个点作为画图的基础.
    # x0 = np.linspace(-2,2,100)
    # 
    # # 定义测试参数集并根据它进行各种实验
    # test_set = (1,1.5,2)
    # for d in test_set:
    #     print(get_cost(d,x,y))
    # #画出相应的图像 来看拟合的程度
    # plt.scatter(x,y,c='g',s=20)
    # for d in test_set:
    #     plt.plot(x0, get_model(d)(), label= "degree ={}".format(d))
    # plt.xlim(-2,2)
    # # 将横轴,纵轴的范围分别限制在(-2,4), (10^5, 8*10^5)
    # plt.ylim(6e5, 8e5)
    # # 调用 legend 方法使曲线对相应的 label 正确显示
    # plt.legend()
    # plt.show()


    # print(good_suburb)
    # suburb_df = get_suburb_data(df,'Brunswick')
    # ax = suburb_df.plot.scatter(x='Landsize', y='Price', label= 'Brunswick',color = 'green')
    # suburb_df = get_suburb_data(df,'Fitzroy North')
    # ax = suburb_df.plot.scatter(x='Landsize', y='Price', label= 'Fitzroy North',color = 'blue',ax=ax)
    # suburb_df = get_suburb_data(df,'Port Melbourne')
    # ax = suburb_df.plot.scatter(x='Landsize', y='Price', label= 'Port Melbourne',color = 'red',ax=ax)
    # suburb_df = get_suburb_data(df,'Reservoir')
    # ax = suburb_df.plot.scatter(x='Landsize', y='Price', label= 'Reservoir',color = 'gold',ax=ax)
    # suburb_df = get_suburb_data(df,'Richmond')
    # ax = suburb_df.plot.scatter(x='Landsize', y='Price', label= 'Richmond',color = 'cyan',ax=ax)
    # plt.show()
    '''这里 show()出来的图片. 是否要把Landsize范围改成 250以内呢? 因为看图表名,大于250的数据趋势和小于250的不一样. Note, 从图表看, Reservoir这个区 预测的可能不准.
    # 如果条件是 Lansize <= 250 数据row条数在 70条以上, 满足条件的 good_suburb 有 5 个, 且趋势都差不多是递增的 这样会是总共 512条记录
    # 这样比较好拟合吧,拟合的好预测的才准咯 ? 我觉得.
    '''
