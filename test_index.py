import os

import pytest
import requests
import responses
from mock import MagicMock, patch, Mock

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


def test_fetch_blank_url():
    tc = test_client()
    response = tc.post('/fetch')
    assert 'This field is required.' in response.data

def test_fetch_non_http():
    tc = test_client()
    response = tc.post('/fetch', data=dict(url='ftp://example.com'))
    print response.data
    assert 'Only HTTP- or HTTPS-based URLs allowed!' in response.data

@patch('index.requests.get')
def test_fetch_non_html(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200 
    mock_response.headers = {'content-type': 'application/json'}
    mock_get.return_value = mock_response
    tc = test_client()
    r = tc.post('/fetch', data=dict(url='http://example.com'))
    assert 'The server returned something other than HTML!' in r.data

@patch('index.requests.get')
def test_fetch_404(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    tc = test_client()
    r = tc.post('/fetch', data=dict(url='http://example.com'))
    assert 'Got an error from the remote server!' in r.data

def test_fetch_localhost():
    tc = test_client()
    response = tc.post('/fetch', data=dict(url='http://127.0.0.1'))
    assert 'Requests to that IP address are not allowed!' in response.data

@patch('index.requests.get')
def test_fetch_valid_html(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {'content-type': 'text/html'}
    mock_response.text = html_data()
    mock_get.return_value = mock_response
    tc = test_client()
    r = tc.post('/fetch', data=dict(url='http://example.com'))
    assert r.status_code == 200

@patch('index.requests.get')
def test_fetch_json(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {'content-type': 'text/html'}
    mock_response.text = json_data()
    mock_get.return_value = mock_response
    tc = test_client()
    r = tc.post('/fetch', data=dict(url='http://json.com'))
    print r.data
    assert 'No tags found!' in r.data
