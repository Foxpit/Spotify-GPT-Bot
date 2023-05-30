from flask import Flask, request, jsonify
import bot as spotify_bot

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def handle_request():
    data = request.json
    response = spotify_bot.handle_bot(data)
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
