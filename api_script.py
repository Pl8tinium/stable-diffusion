from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def hello_world():
    subprocess.Popen(["sh","./test.sh"])
    return "Done"

if __name__ == "__main__":
    app.run()