from flask import Flask, request, redirect, render_template
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import simplejson as json
import requests
import datetime
import time
from dateutil.relativedelta import relativedelta
import pandas as pd

app = Flask(__name__)

@app.route('/')
def input():
  return render_template('index.html')

@app.route('/output', methods=['getlist', 'post'])
def output():

  # Receive inputs
  start_date = request.form['start_date']
  end_date = request.form['end_date']
  ticker = request.form['ticker']
  features = request.form.getlist('features')

  # Fetch stock data
  api_url = "https://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=AbHy5cdz65R3V9XKLexS&start_date=%s&end_date=%s" % (ticker, start_date, end_date)

  s = requests.Session()
  s.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
  r = s.get(api_url)


  # Store data
  data = json.loads(r.text)
  df = pd.DataFrame(data=data['dataset']['data'], columns=data['dataset']['column_names'])


  # Build plot
  p = figure(title="%s: %s - %s" % (ticker, time.strftime('%B %e, %Y', time.strptime(start_date, '%Y-%m-%d')), time.strftime('%B %e, %Y', time.strptime(end_date, '%Y-%m-%d'))), x_axis_type='datetime')
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Stock Price (USD)'
  palette = ['red', 'blue', 'green', 'orange']
  for i in range(len(features)):
   p.line(pd.to_datetime(df['Date']), y=df[features[i]], line_width=2, line_dash=[2, 4, 2], line_dash_offset=8*i, line_color=palette[i], legend='%s' %features[i])
  
  script, div = components(p)
  
  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
