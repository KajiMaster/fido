from collections import Counter
from urlparse import urlparse

from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
from flask import request as rq
import requests

app = Flask(__name__)
app.debug = True


# first view shows the URL entry box
@app.route('/')
def index():
    return render_template('test.html')

#the form on the index page hits this url
@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    if rq.method == 'POST':
        #error = None
        #url = None
        url = rq.form.get('url')
        # make sure the user actually passed us a URL
        if not url:
            return render_template('index.html', error='No URL specified!')
        # validate the URL
        pr = urlparse(url)
        # this check also catches relative urls
        if pr.scheme not in ('http', 'https'):
            return render_template('index.html', 
                    error='Only HTTP- or HTTPS-based URLs allowed!')
        #if not pr.netloc:
        #    return render_template('index.html', error='Relative URLs not allowed!')
        try:
            r = requests.get(url)
        except Exception as e:
            return render_template('index.html', 
            error='There was a problem with your request. Please doublecheck your URL.')
        # requests automatically follows redirects
        # so the final status code should be a 200
        if r.status_code != requests.codes.ok:
            return render_template('index.html',
                    error='Got an error from the remote server!')
        # we only try to parse HTML
        # i'm not overjoyed with this as the only check to make sure the
        # payload is in fact HTML, but i'm not sure what other options there are
        if r.headers['content-type'] != 'text/html':
            return render_template('index.html',
                    error='The server returned something other than HTML!')
        source_html = r.text
        try:
            soup = BeautifulSoup(source_html)
        except Exception as e:
            return render_template('index.html',
                    error='There was a problem with the target HTML!')
        tags = [tag.name for tag in soup.findAll()]
        tag_dict = dict(Counter(tags))
        return render_template('index.html', 
                error=error, 
                source_html=source_html,
                tag_dict=tag_dict)

    return render_template('index.html')





    
if __name__ == '__main__':
    app.run()
