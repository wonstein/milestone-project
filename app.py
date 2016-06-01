from flask import Flask, request, redirect, render_template
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import simplejson as json
import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

app = Flask(__name__)

# Accept inputs

@app.route('/')
def main():
  # Fetch stock data
  start_date = datetime.date.today() - relativedelta(days=5)
  end_date = datetime.date.today()
  #print start_date
  #print type(datetime.date.today())
  stock = "AAPL"

  api_url = "https://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=AbHy5cdz65R3V9XKLexS&start_date=%s" % (stock, str(start_date))

  s = requests.Session()
  s.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
  r = s.get(api_url)

  # Store data
  data = json.loads(r.text)
  #print json.dumps(data, indent=4)
  #print json.dumps(data['dataset']['column_names'], indent=4)
  #print type(data['dataset']['column_names'])
  df = pd.DataFrame(data=data['dataset']['data'], columns=data['dataset']['column_names'])
  #print df.iloc[0:3,1]

  # Build plot
  output_file("graph2.html")
  #print pd.to_datetime(df['Date'])
  #print type(pd.to_datetime([1, 2]))

  p = figure(title="%s: %s - %s" % (stock, start_date.strftime("%B %d, %Y"), end_date.strftime("%B %d, %Y")), x_axis_type='datetime')
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Stock Price (USD)'
  #p.title_text_font_size = '12pt'
  p.line(pd.to_datetime(df['Date']), y=df['Open'], line_width=2)
  
  script, div = components(p)
  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
