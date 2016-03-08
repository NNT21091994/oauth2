from flask import Flask, request, redirect, session, url_for, render_template
from requests_oauthlib import OAuth2Session
from flask.json import jsonify
import os
import traceback
import sys
import logging
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

client_id = "475f6645dbeae7705619"
client_secret = "da53ed6a6f596834145d45ca805532b9aeb58519"
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"
redirect_url = "https://immense-ravine-87169.herokuapp.com/myapp/callback"


@app.route("/")
def myapp():
	return render_template('view.js')


@app.route("/view")
def demo():
   try:
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    #return render_template('err.html',err=authorization_url)
    return redirect(authorization_url)
   except Exception as e:
    traceback.print_exc(file=sys.stdout)
    return render_template('err.html', err=str(e))


@app.route("/callback", methods=['GET'])
def callback():
	github = OAuth2Session(client_id, state=session.get('oauth_state'))
	url=request.url.replace("http://","https://")
	#return render_template('err.html',err=url)


	token = github.fetch_token(token_url, username=client_id, password=client_secret, authorization_response=url)
	
	session['oauth_token'] = token
	return jsonify(github.get('https://api.github.com/user').json())
	#return redirect(url_for('.profile'))


@app.route("/myapp/profile", methods=["GET"])
def profile():
	github = OAuth2Session(client_id, token=session["oauth_token"])
	return jsonify(github.get("https://api.github.com/user").json())

if __name__ == "__main__":
	os.environ['DEBUG'] = "1"
	app.run(debug=True)
