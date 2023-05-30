from flask import Flask, request,jsonify,render_template_string,session, redirect, url_for
from flask_session import Session
import redis
import bot  # assuming bot.py is in the same directory
from bot import handle_bot 
from datetime import timedelta

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')


@app.route('/bot', methods=['POST'])
def handle_request():
    data = request.json
    response = handle_bot(data)
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    