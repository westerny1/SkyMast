from flask import Flask, redirect, url_for, render_template

#change based on saved directory
path = r'D:\UPD\cs173\SkyMast'

app = Flask(__name__, static_folder = path)


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()