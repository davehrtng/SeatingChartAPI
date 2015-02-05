from flask import Flask
app = Flask(__name__)

@app.route("/") #@ is a decorator
def go_away():
    return "Go away!"
	
@app.route("/hello")
def hello():
	return "Hello World!"

if __name__ == "__main__":
    app.run()