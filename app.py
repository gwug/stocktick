from flask import Flask, render_template, request, redirect
import Quandl as quandl
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.embed import components 

import numpy as np
from math import pi

app = Flask(__name__)

@app.route('/')
def fcn():
	
	return render_template('index.html')

@app.route('/index', methods=['GET','POST'])
def index():
	
	# Make api call
	stock=request.form['tsym']
	
	# Make api call
	quandl_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?column_index=4&exclude_column_names=true&start_date=2016-11-01&end_date=2016-11-30&order=asc&collapse=daily&api_key=EsXwBsciiHTkCJ4869dB' %stock
	quandl_response = requests.get(quandl_url)

	# pandas and format
	quandl_df=pd.read_json(quandl_response.text)	
	stock_data=quandl_df['dataset_data']['data']
	stock_date, stock_price=zip(*stock_data)
	dates=np.array(stock_date, dtype=np.datetime64)	
	prices=np.array(stock_price, dtype=np.float)
	
	# output to static HTML file
	#output_file("templates/graph.html")

	# make a bokeh figure
	p = figure(plot_width=400, plot_height=400)
	# add a circle renderer with a size, color, and alpha
	#p.circle(dates, prices, size=20, color="navy", alpha=0.5)
	p.line(dates, prices)
	
	p.xaxis.formatter=DatetimeTickFormatter(
		hours=["%d %B %Y"],
		days=["%d %B %Y"],
		months=["%d %B %Y"],
		years=["%d %B %Y"],
	)
	
	p.xaxis.major_label_orientation = pi/4
	
	script, div = components(p)
	
	# show the results
	#show(p)
	
	#return render_template('graph1.html', s=s)
	#return render_template('graph.html')
	return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
	app.run(port=33507, debug=True)