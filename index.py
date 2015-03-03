from collections import Counter
from urlparse import urlparse

from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
from flask import request as rq
#from flask_wtf.csrf import CsrfProtect
import requests

import forms

app = Flask(__name__)
app.debug = True

# first view shows the URL entry box
@app.route('/')
def index():
    return render_template('test.html')


#the form on the index page hits this url
@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    tag_dict = None
    form = forms.URLForm(csrf_enabled=False)
    if form.validate_on_submit():
        html_errors = None
        url = form.url.data
        try:
            r = requests.get(url)
        except Exception as e:
            form.url.errors.append('There was a problem with your request. Please doublecheck your URL.')
            return render_template('index.html', 
                    form=form,
                    tag_dict=tag_dict)
        # requests automatically follows redirects
        # so the final status code should be a 200
        if r.status_code != requests.codes.ok:
            form.url.errors.append('Got an error from the remote server!')
            return render_template('index.html', form=form)
        # we only try to parse HTML
        # i'm not overjoyed with this as the only check to make sure the
        # payload is in fact HTML, but i'm not sure what other options there are
        if not r.headers['content-type'].startswith('text/html'):
            form.url.errors.append('The server returned something other than HTML!')
            return render_template('index.html', form=form)
        source_html = r.text
        try:
            soup = BeautifulSoup(source_html, 'html.parser')
        except Exception as e:
            html_errors = ['There was a problem with the target HTML!']
            return render_template('index.html', form=form,
                                    html_errors=html_errors)
        tags = [tag.name for tag in soup.findAll()]
        # just in case something got past that's not actually HTML
        # like, say, JSON
        if not tags:
            html_errors = ['No tags found!']
            source_html = None
            tag_dict = None
        else:
            source_html = soup.prettify()
            tag_dict = dict(Counter(tags))
        return render_template('index.html', 
                html_errors=html_errors, 
                form=form,
                source_html=source_html,
                tag_dict=tag_dict)
    return render_template('index.html', form=form, tag_dict=tag_dict)





    
if __name__ == '__main__':
    app.run()
