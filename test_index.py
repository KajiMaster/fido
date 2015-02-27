import os

import pytest

import index

@pytest.fixture(scope='module')
def json_data():
    with open('sample.json') as f:
        json_data = f.read()
    return json_data

@pytest.fixture(scope='module')
def xml_data():
    with open('sample.xml') as f:
        xml_data = f.read()
    return xml_data

@pytest.fixture(scope='module')
def html_data():
    with open('sample.html') as f:
        html_data = f.read()
    return html_data

@pytest.fixture(scope='module')
def test_client():
    tc = index.app.test_client()
    return tc

#def test_fetch_get():
#    tc = test_client()
#    raw_html = tc.get('/fetch')
#    assert 'Only POSTs allowed!' in raw_html.data

def test_fetch_blank_url():
    tc = test_client()
    response = tc.post('/fetch')
    assert 'No URL specified!' in response.data

def test_fetch_non_http():
    tc = test_client()
    response = tc.post('/fetch', data=dict(url='ftp://example.com'))
    assert 'Only HTTP- or HTTPS-based URLs allowed!' in response.data



#def test_fetch_relative_url():
#    tc = test_client()
#    response = tc.post('/fetch', data=dict(url='//foo'))
#    assert 'Relative URLs not allowed!' in response.data
#class IndexTestClass:
#    def setUp(self):
#        with open('sample.json') as f:
#            json_data = f.read()
#        with open('sample.xml') as f:
#            xml_data = f.read()
#        with open('sample.html') as f:
#            html_data = f.read()

#    def test_empty_fetch(self):
#        raw_html = self.app.get('/fetch')
#        self.assert 'No URL specified!' in raw_html.data

