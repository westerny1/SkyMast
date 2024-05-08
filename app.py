from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from mastodon import Mastodon
from datetime import datetime
from atproto import Client, models
from werkzeug.utils import secure_filename
import os
import glob

UPLOAD_FOLDER = 'temp_img'

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skymast.db'
db = SQLAlchemy(app)

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_email = db.Column(db.String(200), nullable=False)
    db_password = db.Column(db.String(200), nullable=False)
    db_website = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Account %r>' % self.id

with app.app_context():
    db.create_all()

@app.route("/", methods=['POST', 'GET'])
def home():
    temp_img_to_del = glob.glob(os.getcwd()+"\\temp_img\\*")
    for img in temp_img_to_del:
        os.remove(img)
    account_list = Accounts.query.order_by(Accounts.date_created).all()
    return render_template("index.html", account_list = account_list)
    
@app.route('/cross_post', methods=['POST', 'GET'])
def cross_post():
    if request.method == 'POST':
        post_text = request.form['post-text']
        imglist = request.files.getlist('img')

        if (post_text != "" or imglist != []) and "post-to" in request.form:
            img_bytes_list = []
            if imglist != []:     
                for img in imglist:
                    img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
                    with open(os.getcwd()+'\\temp_img\\'+img.filename, "rb") as f:
                        img_bytes = f.read()
                    img_bytes_list.append(img_bytes)
            for account in Accounts.query.all():
                if account.db_website == 'mastodon':
                    try:
                        # create an application
                        Mastodon.create_app(
                            'skymast',
                            api_base_url = 'https://mastodon.social',
                            to_file = 'pytooter_clientcred.secret'
                        )
                        print('created application in mastodon')

                        # login
                        mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
                        mastodon.log_in(
                            account.db_email, 
                            account.db_password, 
                            to_file = 'pytooter_usercred.secret'
                        )
                        print('logged-in in mastodon')

                        # posting
                        mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
                        
                        if imglist != []:
                            mastodon.status_post(post_text, media_ids=[mastodon.media_post(os.getcwd()+'\\temp_img\\'+img.filename) for img in imglist])
                        elif post_text != "":
                            mastodon.toot(post_text)
                        else:
                            return 'There was an issue in posting in mastodon 1'
                        print('posted text in mastodon')

                    except:
                        return 'There was an issue in posting in mastodon 2'
                elif account.db_website == 'bluesky':
                    try:
                        # creating session
                        client = Client(base_url='https://bsky.social')
                        client.login(account.db_email, account.db_password)
                        print('created session in bluesky')

                        # posting 
                        if imglist != []:
                            embed_images = models.AppBskyEmbedImages.Main(images=[models.AppBskyEmbedImages.Image(alt='', image=client.com.atproto.repo.upload_blob(img).blob) for img in img_bytes_list])
                            client.send_post(text=post_text, embed=embed_images)
                        elif post_text != "":
                            client.send_post(post_text)
                        else:
                            return 'There was an issue in posting in bluesky'
                    except:
                        return 'There was an issue in posting in bluesky'
                else:
                    pass
            print('Done posting in both mastodon and bluesky')
            return redirect('/')
        else:
            return redirect('/')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # add mastodon account  
        if "mastodon_login" in request.form and email != '' and password != '':
            print("mastodon login")
            account = Accounts(db_email = email, db_password = password, db_website = "mastodon")
            db.session.add(account)
            db.session.commit()
            return redirect('/')
        
        # add bluesky account
        elif "bluesky_login" in request.form and email != '' and password != '':
            print("bluesky login")
            account = Accounts(db_email = email, db_password = password, db_website = "bluesky")
            db.session.add(account)
            db.session.commit()
            return redirect('/')
        
        else:
            return redirect('/')

@app.route('/accounts', methods=['POST', 'GET'])
def accounts():
    if request.method == 'POST':
        for account in Accounts.query.all():
            if "del_account{}".format(account.id) in request.form:
                db.session.delete(account)
                db.session.commit()
                return redirect('/')
        else:
            return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

