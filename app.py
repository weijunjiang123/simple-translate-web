import requests, os, uuid, json
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request, render_template, session

load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    # Get the text to translate from the request
    original_text = request.form['text']
    target_language = request.form['language']

    # Get the environment variables
    key = os.getenv('KEY')
    endpoint = os.getenv('ENDPOINT')
    location = os.getenv('LOCATION')

    # Create the request construct
    path = '/translate?api-version=3.0'
    params = '&to=' + target_language
    constructed_url = endpoint + path + params

    # Create the header
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body
    body = [{"text": original_text}]

    # Send the request
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    translator_response = translator_request.json()
    translated_text = translator_response[0]['translations'][0]['text']
    return render_template(
        'results.html',
        translated_text=translated_text,
        oringinal_text=original_text
    )

