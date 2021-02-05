from flask import Flask
from flask import render_template

# creates a Flask application with name "app"
app = Flask(__name__)

# a route to display our html page called "index.html" gotten from [react-chat-widget](https://github.com/mrbot-ai/rasa-webchat)
@app.route("/")
def index():
    print("lololo")
    return render_template('index.html')

# run the application
if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0")