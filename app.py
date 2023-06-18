
from flask import Flask,render_template,url_for,request,redirect, make_response
import json
import os
import time
import random
import datetime
import warnings
import numpy as np
import pandas as pd
import gspread as gs
import threading as th
warnings.filterwarnings("ignore")

_update = False
nf_spot,bnf_spot = [0.0,0.0]
nf_strike,bnf_strike = [0.0,0.0]
_nifty = "https://www.moneycontrol.com/india/indexfutures/nifty/9/"
_banknifty = "https://www.moneycontrol.com/india/indexfutures/banknifty/23/"

def next_exp():   # Expiry date selection for correct url
  today = datetime.date.today()
  dayn = today.isoweekday()
  if dayn<=4:
    delt = (4-dayn)
    coming_thursday = today + datetime.timedelta(delt)
  else:
    dayn = (dayn-4)
    delt = (7-dayn)
    coming_thursday = today + datetime.timedelta(delt)    
  return coming_thursday

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]
    Temperature = (pd.Timestamp('now') + pd.Timedelta('05:30:00'))
    Humidity = random() * 55  
    # Temperature = random() * 100
    # Humidity = random() * 55
    data = [time() * 1000, Temperature, Humidity]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/nf')
def nf():
    n_url = _nifty + str(next_exp()) 
    Raw_Table_Nf = pd.read_html(n_url)
    spot_price_Nf = float(Raw_Table_Nf[0].iloc[4][1])
    t_time = (pd.Timestamp('now') + pd.Timedelta('05:30:00'))
    return str(t_time) + ' nifty:' + str(spot_price_Nf)

@app.route('/bnf')
def bnf():
    bnf_url = _banknifty + str(next_exp())
    Raw_Table_Bn = pd.read_html(bnf_url) #reading datatables
    spot_price_Bn = float(Raw_Table_Bn[0].iloc[4][1])
    OI_Table = Raw_Table_Bn[4]
    OI_Table_dict = OI_Table.to_dict()
    return OI_Table_dict
