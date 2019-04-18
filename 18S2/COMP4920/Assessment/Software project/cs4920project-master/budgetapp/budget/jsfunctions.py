import re, random, math, secrets

# Takes daily and monthly spend and returns javascript
# code which can be inserted into html
def overview_odometer(daily, monthly, m_income):
	js_func = "setTimeout(function(){\
    				daily_spend.innerHTML =" + str(daily) + ";\
    				monthly_spend.innerHTML = " + str(monthly) + ";\
    				monthly_income.innerHTML = " + str(m_income) + ";\
				}, 1000);"
	return js_func


# Takes labels and data to create a graph with given variables.
# Easier to do this than pass variables to front-end.
# types, expenses and colours should be lists, where
# len(types) == len(expenses) == len(colours)
def donut_graph_no_label(name, types, expenses, colours):
	js_func = "var expend = new Chart(" + str(name) + ", { type: 'doughnut', \
										data: { labels:" + str(types) + ", \
						 				datasets: [{ label: '# of Votes', data:" + str(expenses) + ", \
										backgroundColor:" + str(colours) + "}] }, \
										options: {legend: { display: false } } });"
	return js_func

# Creates a bar graph using set arguments
# name is the variable name and should be unique
# len(labels) == len(data)
def bar_graph_monthly(name, title, labels, data):
	js_func = "var " + str(name) + " = new Chart(typ, { type: 'line',data: { \
						labels:" + str(labels) + ", \
						datasets: [{ data: " + str(data) + ", \
						fill: false, \
						borderColor: '#000000', \
						backgroundColor: [ \
							'rgba(140, 140, 140, 1)', \
							'rgba(40, 40, 40, 1)', \
							'rgba(40, 40, 40, 1)', \
							'rgba(75, 192, 192, 1)', \
							'rgba(153, 102, 255, 1)', \
							'rgba(255, 159, 64, 1)' \
						]}]}, \
						options: {\
						scales: {\
							yAxes: [{\
								ticks: {\
									beginAtZero:true\
								}\
							}]\
						},\
						legend: {\
        					display: false\
    					}} });"
	return js_func