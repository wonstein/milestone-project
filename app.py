from flask import Flask#, Render_Template, request, redirect

app = Flask(__name__)

@app.route('/')
def hello_world():
  return "Hello World! ws"

#@app.route('/index')
#def index():
#  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
