import pandas as pd
import matplotlib.pyplot as plt



pd.set_option('expand_frame_repr', False)


csv_1='Melbourne_housing_FULL.csv'


df1 = pd.read_csv(csv_1, index_col=None)

analysis_df = df1[['Suburb', 'Price', 'Landsize']].dropna()


Abbotsford = analysis_df.loc[analysis_df['Suburb'] == 'Abbotsford']
Abbotsford = Abbotsford.loc[Abbotsford['Landsize'] <= 400]
Abbotsford = Abbotsford.loc[Abbotsford['Landsize'] > 0]

HeidelbergHeights = analysis_df.loc[analysis_df['Suburb'] == 'Heidelberg Heights']
HeidelbergHeights = HeidelbergHeights.loc[HeidelbergHeights['Landsize'] <= 400]
HeidelbergHeights = HeidelbergHeights.loc[HeidelbergHeights['Landsize'] > 0]

Niddrie = analysis_df.loc[analysis_df['Suburb'] == 'Niddrie']
Niddrie = Niddrie.loc[Niddrie['Landsize'] <= 400]
Niddrie = Niddrie.loc[Niddrie['Landsize'] > 0]


ax = Abbotsford.plot.scatter(x='Landsize', y='Price', label='Abbotsford')
ax = HeidelbergHeights.plot.scatter(x='Landsize', y='Price', label='HeidelbergHeights', color='green', ax=ax)
ax = Niddrie.plot.scatter(x='Landsize', y='Price', label='Niddrie', color='red', ax=ax)
plt.show()