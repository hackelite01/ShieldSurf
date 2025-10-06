from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.parse import urljoin
import json
import html
import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import controller and model from parent directory
import controller
import model

# Initialize Flask app with correct paths
app = Flask(__name__, 
            template_folder=os.path.join(parent_dir, 'templates'),
            static_folder=os.path.join(parent_dir, 'static'))

@app.route('/',  methods=['GET','POST'])
def home():
    try:
        url = request.form['url']
        result = controller.main(url)
        output = result
    except:
        output = 'NA'
    return render_template('index.html', output=output)

@app.route('/preview', methods=['POST'])
def preview():
    try:
        url = request.form.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # inject external resources into HTML
        for link in soup.find_all('link'):
            if link.get('href'):
                link['href'] = urljoin(url, link['href'])
        
        for img in soup.find_all('img'):
            if img.get('src'):
                img['src'] = urljoin(url, img['src'])

        return render_template('preview.html', content=soup.prettify())
    except Exception as e:
        return  f"Error: {e}"

@app.route('/source-code', methods=['GET','POST'])
def view_source_code():
    url = request.form.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    formatted_html = soup.prettify()
    return render_template('source_code.html', formatted_html = formatted_html, url = url)
