from flask import Flask
from flask import request
import subprocess

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = request.get_json(force=True)
    print()
    print(data['prompt'] if 'arst' in data else 'No prompt')
    return "Done"

if __name__ == "__main__":
    app.run()