# most of the functions which involve visualising data is covered here
# requirements : matplotlib

import matplotlib.pyplot as plt
import numpy as np
import random

def create_colours(n):
	to_return = []
	for _ in range(0, n):
		to_return.append(list(np.random.choice(range(256), size=3)))
	return to_return

# sample data, using spending and category type as examples
labels = 'Eating Out', 'Bills', 'Groceries', 'Electronics'
amount = [100, 500, 200, 300]
colours = create_colours(n=len(amount))
title = 'placeholder'

def pie_plot(labels, amount, title):
	plt.title(title)
	plt.pie(amount, labels=labels, autopct='%1.1f%%')
	plt.axis('equal')
	plt.show()

pie_plot(labels, amount, title)

# sample data for the total amount of spending every day
dates = ["11/12/18", "12/12/18", "13/12/18", "14/12/18"]
amount_spent = [300, 200, 51, 65]
title_2 = "Total spending from {} to {}".format(dates[0], dates[len(dates)-1])

def line_plot(x_axis, y_axis, x_label, y_label, title):
	plt.title(title)
	plt.plot(x_axis, y_axis)
	plt.xlabel(x_label)
	plt.ylabel(y_label)

	plt.show()

line_plot(dates, amount_spent, 'Dates', 'Spending', title_2)