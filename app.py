from flask import Flask, redirect, url_for, render_template
import requests

#change based on saved directory
path = r'D:\UPD\cs173\SkyMast'

app = Flask(__name__, static_folder = path)


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

url = 'https://mastodon.social/api/v1/statuses'
auth = {'Authorization': 'Bearer zfBQR1uwx1iQndjCuZ5H-JPCCZpklrHLp1br6FfeKS4'}
params = {'status': 'Test 2: How do i recreate that test 1'}
response = requests.post(url, data=params, headers=auth)
print(response, "Gumana siya")
