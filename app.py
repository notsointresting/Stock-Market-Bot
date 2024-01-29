from flask import Flask
from flask import request
from twilio.rest import Client
from market import get_stock_price
import os


app = Flask(__name__)

ACCOUNT_ID = os.environ.get('TWILIO_ACCOUNT')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
client = Client(ACCOUNT_ID, TWILIO_TOKEN)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')


def process_msg(msg, receiver_name):
    response = ""
    if msg.lower() == "hi":
        response = f"Hello {receiver_name}, welcome to the stock market bot! Type sym:<stock_symbol> to get the price of the stock"
    elif "sym:" in msg:
        data = msg.split(":")
        stock_symbol = data[1]
        stock_data = get_stock_price(stock_symbol)
        response = "The stock price of {} is ₹ {}".format(stock_symbol, stock_data['last_price'])
    else:
        response = "Please type hi to get started"
    return response

def send_msg(msg, recipient):
    client.messages.create(
       from_=TWILIO_NUMBER,
       body=msg,
       to=recipient
    )

@app.route('/webhook', methods=['POST'])
def webhook():
    
    f = request.form
    msg = f['Body']
    receiver_name = f['ProfileName']
    sender = f['From']
    response = process_msg(msg, receiver_name)
    send_msg(response, sender)
    return "OK", 200



