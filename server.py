from flask import Flask, request, jsonify
import bot as spotify_bot

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def handle_request():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    response = spotify_bot.handle_bot(data)
    return jsonify(response)

if __name__ == '__main__':
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    app.run(port=5000, debug=debug_mode)

