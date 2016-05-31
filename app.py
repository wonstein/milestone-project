from flask import Flask, request, redirect, render_template
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
def main():
  api_url = 'https:/www.quandl.com/api/vq/datasets/WIKI/%s.json' % stock
  session = requests.Session()
  session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
  raw_data = session.get(api_url)

  plot = figure(tools=TOOLS,
              title='Data from Quandle WIKI set',
              x_axis_label='date',
              x_axis_type='datetime')

  script, div = components(plot)
  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
