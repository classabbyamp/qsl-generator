#!/usr/bin/env python3
"""
app.py

Copyright (C) 2020 classabbyamp
Released under the MIT License
"""

import requests
import shutil
import os

from flask import Flask, request, render_template
import jinja2
from jinja2 import Template


app = Flask(__name__)


latex_jinja_env = jinja2.Environment(block_start_string='\BLOCK{',
                                     block_end_string='}',
                                     variable_start_string='\VAR{',
                                     variable_end_string='}',
                                     comment_start_string='\#{',
                                     comment_end_string='}',
                                     line_statement_prefix='%%',
                                     line_comment_prefix='%#',
                                     trim_blocks=True,
                                     autoescape=False,
                                     loader=jinja2.FileSystemLoader(os.path.abspath('.')))


LATEX_URL = 'http://rtex.probablyaweb.site/api/v2'


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def gen_cart():
    """
    latex_vars = ""
    if 'callsign[]' in request.form:
        latex_vars +="\def \myCallsign {"
        for call in request.form.getlist('callsign[]'):
            latex_vars += latex_cbox + call + " \, "
        latex_vars += "}\n"
    if 'name' in request.form:
        latex_vars += f"\def \myName {{{request.form['name']}}}\n"
    if 'cq[]' in request.form:
        latex_vars +="\def \myCQZone {"
        for z in request.form.getlist('cq[]'):
            latex_vars += "\= " + latex_cbox + z + "\,"
        latex_vars += "}\n"
    if 'itu[]' in request.form:
        latex_vars +="\def \myITUZone {"
        for z in request.form.getlist('itu[]'):
            latex_vars += "\> " + latex_cbox + z + "\,"
        latex_vars += "}\n"
    if 'county[]' in request.form:
        latex_vars += "\def \myCounty {"
        for cty in request.form.getlist('county[]'):
            latex_vars += "\> " + latex_cbox + cty + "\\\\"
        latex_vars += "}\n"
    latex_vars += f"\def \myMailingAddr {{{request.form['address1']}\\\\ {request.form['address2']}\\\\ {request.form['address3']} \\\\ {request.form['address4']} \\\\ {request.form['country']}}}\n"
    latex_vars += f"\def \myQTH {{{request.form['qth']}}}\n"
    latex_vars += f"\def \myClubs {{CLUBS LINE 1 \\\\ CLUBS LINE 2}}\n"
    latex_vars += f"\def \myNotes {{NOTES}}\n"
    """
    latex_vars = {
                "call_cbox": True,
                "callsigns": ["***REMOVED***", "***REMOVED***"],
                "name": "A. V. G.",
                "address": "ln1 \\\\ ln2 \\\\ ln3 \\\\ ln4 \\\\ country", # maybe make this into 5 vars
                "cq_cbox": True,
                "cq": [1],
                "itu_cbox": False,
                "itu": [56, 17],
                "county_cbox": True,
                "county": ["Alameda"],
                "clubs1": "HRCC YLRL",
                "clubs2": "idk lol",
                "qth": "Troy, NY FN32er",
                "notes": "NOTES GO HERE",
            }
    template = latex_jinja_env.get_template('qsl-card.tex')
    latex = template.render(latex_vars)

    latex_img = render_latex('pdf', latex)
    return render_template('generate.html', data=request.form, latex=latex_img)

def render_latex(fmt: str, latex: str):
    payload = {'code': latex, 'format': fmt}
    response = requests.post(LATEX_URL, data=payload)
    response.raise_for_status()
    resp_data = response.json()
    if resp_data['status'] != 'success':
        raise Exception('Failed to render LaTeX')
    return LATEX_URL + '/' + resp_data['filename']
