from flask import Flask
from ctrip import Ctrip
from ch import Ch
from csair import Csair

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ctrip/<d_code>/<d_city>/<a_code>/<a_city>/<date>')
def ctrip(a_code, a_city, d_code, d_city, date):
    return Ctrip.get_ctrip(a_code, a_city, d_code, d_city, date)


@app.route('/ch/<d_city>/<a_city>/<date>')
def ch(a_city, d_city, date):
    return Ch.get_ch(a_city, d_city, date)


@app.route('/csair/<d_code>/<a_code>/<date>')
def csair(a_code, d_code, date):
    return Csair.get_csair(a_code, d_code, date)


if __name__ == '__main__':
    app.run()
