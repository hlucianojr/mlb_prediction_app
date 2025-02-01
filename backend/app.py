from flask import Flask, jsonify, request
from HTMLGenerator import HTMLGenerator
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    # Future implementation for prediction logic
    generator = HTMLGenerator()
    return generator.generate_html("https://statsapi.mlb.com/api/v1/sports");
    # r eturn jsonify({'message': 'Prediction logic not implemented yet.'})

if __name__ == '__main__':
    app.run()
