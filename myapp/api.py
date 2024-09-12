from flask import Flask


app = Flask(__name__)

@app.route('/api/route')
def getMacros():
    return "Prediction Route Working!" 

def getNutrients(food):
    return 0

