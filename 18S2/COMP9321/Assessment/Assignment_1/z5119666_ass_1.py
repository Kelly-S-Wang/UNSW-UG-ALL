import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# Print dataframe
def print_dataframe(df, print_column=True, print_rows=True):
    if print_column:
        print(','.join([c for c in df]))
    if print_rows:
        for index, row in df.iterrows():
            print(','.join([str(row[c]) for c in df]))


# Merge the two datasets Olympics_dataset1.csv and Olympics_dataset2.csv and display the first five rows (do not concatenate the datasets).
def question_1():
	# Load csv file
	df1 = pd.read_csv('Olympics_dataset1.csv', skiprows=1)
	df2 = pd.read_csv('Olympics_dataset2.csv', skiprows=1)

	# Merge 2 files
	df = pd.merge(df1, df2, how='left', left_on=['Unnamed: 0'], right_on=['Unnamed: 0'])
	
	# Rename to meaningful names
	column_names = {'Unnamed: 0': 'Country', 
	'Number of Games the country participated in_x': 'Number of Games the country participated in summer',
	'Gold_x': 'Gold_summer',
	'Silver_x': 'Silver_summer',
	'Bronze_x': 'Bronze_summer',
	'Total_x': 'Total_summer',
	'Number of Games the country participated in_y': 'Number of Games the country participated in winter',
	'Gold_y': 'Gold_winter',
	'Silver_y': 'Silver_winter',
	'Bronze_y': 'Bronze_winter',
	'Total_y': 'Total_winter',
	'Number of Games the country participated in.1': 'Number of Games the country participated in total',
	'Gold.1': 'Gold_total',
	'Silver.1': 'Silver_total',
	'Bronze.1': 'Bronze_total',
	'Total.1': 'Total_total'}
	df.rename(columns=column_names, inplace=True)
	df.reset_index(drop=True, inplace=True)

	# Print the first 5 rows
	print_dataframe(df.head(5))
	return df


# Set the index as the country name and then display the first country in the Dataframe. 
def question_2(df):
	# Set country as index
	df = df.set_index('Country')
	print(df.iloc[0])


# Remove the rubish column and display the first five rows.
def question_3(df):
	# Drop 'Rubish' column
	df = df.drop(['Rubish'], axis=1)
	print_dataframe(df.head(5))


# Remove the rows with NaN fields and display the last ten rows.
def question_4(df):
	# Drop any row that contains NaN
	df = df.dropna(how='any')
	print_dataframe(df.tail(10))


# Calculate and display which country has won the most gold medals in summer games? 
def question_5(df):
	# Remove the last 'total' line
	df = df.drop(df.index[len(df)-1])
	# Change the data type to float
	df['Gold_summer'] = df['Gold_summer'].str.replace(',','').astype(float)
	# Find the max gold medal country index
	index = df['Gold_summer'].idxmax()
	df = df.iloc[[index]]
	print_dataframe(df)


# Calculate and display which country had the biggest difference between their summer and winter gold medal? 
def question_6(df):
	# Remove the last 'total' line
	df = df.drop(df.index[len(df)-1])
	# Change the data type to float
	df['Gold_summer'] = df['Gold_summer'].str.replace(',','').astype(float)
	df['Gold_winter'] = df['Gold_winter'].str.replace(',','').astype(float)
	# Calculate the difference
	df['diff'] = (df['Gold_summer'] - df['Gold_winter']).abs()
	index = df['diff'].idxmax()
	df = df.iloc[[index]]
	print_dataframe(df)


# Sort the countries in descending order, according to the number of total of medals earned throughout the history and display the first and last 5 rows. 
def question_7(df):
	# Remove the last 'total' line
	df = df.drop(df.index[len(df)-1])
	# Change the data type to float
	df['Total_total'] = df['Total_total'].str.replace(',','').astype(float)
	# Sort
	df = df.sort_values('Total_total', ascending=False)
	print_dataframe(df.head(5))
	print_dataframe(df.tail(5), print_column=False)
	return df


# Plot a bar chart of the top 10 countries (according to the sorting in Question 7). For each country use a stacked bar chart showing for each county the total medals for winter and summer games. 
def question_8(df):
	# Remove the characters after country name
	df['Country'] = df['Country'].str.replace(r'\((.)+$', '')
	# Change the data type to float
	df['Total_summer'] = df['Total_summer'].str.replace(',','').astype(float)
	df['Total_winter'] = df['Total_winter'].str.replace(',','').astype(float)
	countries = df['Country'].head(10)
	summer = df['Total_summer'].head(10)
	winter = df['Total_winter'].head(10)
	ind = [x for x, _ in enumerate(countries)]

	plt.barh(ind, winter, label='Winter games')
	plt.barh(ind, summer, label='Summer games', left=winter)

	plt.yticks(ind, countries)
	plt.ylabel('Country')
	plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)
	plt.title('Medals for Winter and Summer Games')
	plt.show()


# Plot a bar chart of the countries (United States, Australia, Great Britain, Japan, New Zealand). For each county you need to show the gold, silver and bronze medals for winter games
def question_9(df):
	# Remove the characters after country name
	df['Country'] = df['Country'].str.replace(r'\((.)+$', '')
	# Get these countries based on index
	df = df.iloc[[143,6,52,70,97]]
	# Get these columns
	df = df[['Gold_winter', 'Silver_winter', 'Bronze_winter']]
	# Change the data type to float
	gold = df['Gold_winter'].str.replace(',','').astype(float)
	silver = df['Silver_winter'].str.replace(',','').astype(float)
	bronze = df['Bronze_winter'].str.replace(',','').astype(float)
	countries = ['United States','Australia','Great Britain','Japan','New Zealand']
	ind = np.arange(5)
	bar_width = 0.1

	plt.bar(ind, gold, width=bar_width, label='Gold')
	plt.bar(ind+bar_width, silver, width=bar_width, label='Silver')
	plt.bar(ind+bar_width+bar_width , bronze, width=bar_width, label='Bronze')

	plt.xticks(ind + bar_width/2, countries)
	plt.title('Winter Games')
	plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
	plt.show()


if __name__ == "__main__": 
	s = "********************"
	print(s + " question_1 " + s)
	q1 = question_1()
	print()
	print(s + " question_2 " + s)
	question_2(q1)
	print()
	print(s + " question_3 " + s)
	question_3(q1)
	print()
	print(s + " question_4 " + s)
	question_4(q1)
	print()
	print(s + " question_5 " + s)
	question_5(q1)
	print()
	print(s + " question_6 " + s)
	question_6(q1)
	print()
	print(s + " question_7 " + s)
	q7 = question_7(q1)
	question_8(q7)
	question_9(q1)
