#!/usr/bin/env python3
"""
app.py

Copyright (C) 2020 ClassAbbyAmp
Released under the MIT License
"""

from flask import Flask, request, render_template
import requests
import shutil


app = Flask(__name__)

LATEX_URL = 'http://rtex.probablyaweb.site/api/v2'

latex_cbox = "$\Box$ "


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def gen_cart():
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
        for z in request.form['itu[]']:
            latex_vars += "\> " + latex_cbox + z + "\,"
        latex_vars += "}\n"
    if 'county[]' in request.form:
        latex_vars += "\def \myCounty {"
        for cty in request.form.getlist('county[]'):
            latex_vars += "\> " + latex_cbox + cty + "\\\\"
        latex_vars += "}\n"
    latex_vars += f"\def \myMailingAddr {{{request.form['address1']}\\\\ {request.form['address2']}\\\\ {request.form['address3']} \\\\ {request.form['address4']}}}\n"
    latex_vars += f"\def \myQTH {{QTH CITY, ST, {request.form['grid']}}}\n"
    latex_vars += f"\def \myClubs {{CLUBS LINE 1 \\\\ CLUBS LINE 2}}\n"
    latex_vars += f"\def \myNotes {{NOTES}}\n"

    with open('qsl-card.tex') as f:
        LATEX = f.read()
    latex_img = render_latex('pdf', latex_vars+LATEX)
    return render_template('generate.html', data=request.form, latex=latex_img)

def render_latex(fmt: str, latex: str):
    payload = {'code': latex, 'format': fmt}
    response = requests.post(LATEX_URL, data=payload)
    response.raise_for_status()
    resp_data = response.json()
    if resp_data['status'] != 'success':
        raise Exception('Failed to render LaTeX')
    return LATEX_URL + '/' + resp_data['filename']
