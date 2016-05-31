from flask import Flask, Render_Template, request, redirect
import request
app = Flask(__name__)

@app.route('/')
def main():
  return "Hello World! ws"

@app.route('/index')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
