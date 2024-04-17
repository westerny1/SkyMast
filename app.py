from flask import Flask, redirect, url_for, render_template, request
import requests

#change based on saved directory
path = r'D:\Local_UPD\CS 173\SkyMast'

app = Flask(__name__, static_folder = path)


@app.route("/", methods=['POST', 'GET', 'DELETE'])
def home():
    if request.method == 'POST':
        post_text = request.form['post-text']

        try:
            url = 'https://mastodon.social/api/v1/statuses'
            auth = {'Authorization': 'Bearer zfBQR1uwx1iQndjCuZ5H-JPCCZpklrHLp1br6FfeKS4'}
            params = {'status': post_text}
            response = requests.post(url, data=params, headers=auth)
            print(response, "Gumana siya")
            return redirect('/')

        except:
            return 'There was an issue adding your task'
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()

