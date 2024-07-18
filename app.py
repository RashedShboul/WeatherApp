from flask import Flask, render_template
from dotenv import load_dotenv
from weather_routes import weather
import os

load_dotenv('.env/config.env')

app = Flask(__name__)

sec_key = os.getenv('SEC_KEY')

app.secret_key = sec_key

# register the weather blueprint
app.register_blueprint(weather)

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)