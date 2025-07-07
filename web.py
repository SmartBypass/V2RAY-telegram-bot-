from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running!"

def start():
    app.run(host='0.0.0.0', port=10000)
