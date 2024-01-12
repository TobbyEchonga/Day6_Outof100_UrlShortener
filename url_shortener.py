from flask import Flask, request, jsonify
import string
import random

app = Flask(__name__)

# Dictionary to store URL mappings (short_key: original_url)
url_mapping = {}

def generate_short_key():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    if 'url' in data:
        original_url = data['url']
        short_key = generate_short_key()

        url_mapping[short_key] = original_url

        short_url = f"http://www.youtube.com/{short_key}"  

        return jsonify({"short_url": short_url}), 201
    else:
        return jsonify({"error": "Missing 'url' parameter"}), 400

@app.route('/<short_key>', methods=['GET'])
def redirect_to_original_url(short_key):
    if short_key in url_mapping:
        original_url = url_mapping[short_key]
        return jsonify({"original_url": original_url}), 200
    else:
        return jsonify({"error": "Short URL not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
