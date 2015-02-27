from urlparse import urlparse

from flask import Flask, render_template
from flask import request as rq
import requests

app = Flask(__name__)
app.debug = True


# first view shows the URL entry box
@app.route('/')
def index():
    return render_template('index.html')

#the form on the index page hits this url
@app.route('/fetch', methods=['POST'])
def fetch():
    error = None
    url = None
    url = rq.form.get('url')
    # make sure the user actually passed us a URL
    if not url:
        return render_template('index.html', error='No URL specified!')
    # validate the URL
    pr = urlparse(url)
    if pr.scheme not in ('http', 'https'):
        return render_template('index.html', 
                error='Only HTTP- or HTTPS-based URLs allowed!')
    #if not pr.netloc:
    #    return render_template('index.html', error='Relative URLs not allowed!')
    try:
        r = requests.get(url)
    except Exception as e:
        return render_template('index.html', error='There was a problem with \
                your request. Please doublecheck your URL.')
    return render_template('index.html', error=error, url=url)





    
if __name__ == '__main__':
    app.run()
