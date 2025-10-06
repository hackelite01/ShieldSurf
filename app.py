from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.parse import urljoin
import controller
import json
import html
import os

# Get the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))

@app.route('/',  methods=['GET','POST'])
def home():
    try:
        if request.method == 'POST':
            url = request.form.get('url', '').strip()
            if not url:
                output = {
                    'status': 'ERROR',
                    'url': '',
                    'msg': 'Please provide a URL to check.'
                }
            else:
                result = controller.main(url)
                output = result
        else:
            output = 'NA'
    except Exception as e:
        print(f"Error in home route: {e}")
        output = {
            'status': 'ERROR',
            'url': request.form.get('url', 'Unknown'),
            'msg': f'An unexpected error occurred: {str(e)}'
        }

    return render_template('index.html', output=output)


# Old /preview 
# @app.route('/preview/<path:url>')
# def preview(url):
#     try:
#         # url = urllib.parse.unquote(url, encoding='ISO-8859-1')
#         url = 'https://' + url
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # inject external resources into HTML
#         for link in soup.find_all('link'):
#             if link.get('href'):
#                 link['href'] = urljoin(url, link['href'])
#         # for script in soup.find_all('script'):
#         #     if script.get('src'):
#         #         script['src'] = urljoin(url, script['src'])
#         for img in soup.find_all('img'):
#             if img.get('src'):
#                 img['src'] = urljoin(url, img['src'])

#         return render_template('preview.html', content=soup.prettify())
#     except Exception as e:
#         return  f"Error: {e}"

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
        
        # Uncomment this if you want to enable script
        # for script in soup.find_all('script'):
        #     if script.get('src'):
        #         script['src'] = urljoin(url, script['src'])

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


if __name__ == '__main__':
    app.run(debug=True)