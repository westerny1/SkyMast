from flask import Flask, redirect, url_for, render_template, request
import requests
from mastodon import Mastodon

#change based on saved directory
path = r'D:\Local_UPD\CS 173\SkyMast'

app = Flask(__name__, static_folder = path)


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        post_text = request.form['post-text']

        try:
            # create an application
            Mastodon.create_app(
                'skymast',
                api_base_url = 'https://mastodon.social',
                to_file = 'pytooter_clientcred.secret'
            )
            print('created application')

            # login
            mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
            mastodon.log_in(
                'skymast001@gmail.com', 
                '@01skymast01@', 
                to_file = 'pytooter_usercred.secret'
            )
            print('logged in')

            mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
            mastodon.toot(post_text)
            print('posted text')
            return redirect('/')

        except:
            return 'There was an issue in posting'
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()

