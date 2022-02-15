"""
File: app.py
------------------
This is the file used to create the Flask app and assiociated routings. 
"""

from flask import Flask, render_template, request, redirect, url_for
from converter import runner_two
import copy


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    print(type(uploaded_file))
    # uploaded_file_two = copy.copy(uploaded_file)
    # uploaded_file_two = request.files['file']  
    output_string = runner_two(uploaded_file)
    return output_string 