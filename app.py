from flask import Flask, redirect, url_for, render_template

path = r'D:\UPD\cs173\Test_Flask'

app = Flask(__name__, static_folder = path)


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()