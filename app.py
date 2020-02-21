#!/usr/bin/env python3
"""
app.py

Copyright (C) 2020 classabbyamp
Released under the MIT License
"""


import atexit
import os
import re
import time
from datetime import timedelta

from flask import abort, Flask, jsonify, request, render_template, send_from_directory
import jinja2
from jinja2 import Template
import requests
from timeloop import Timeloop


tl = Timeloop()


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
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def gen_card():
    form = request.form

    latex_vars = {
        # Demographic
        "callsigns": list(filter(None, form.getlist("callsign[]")[0:2])),
        "name": form.get("name", ""),
        # Address
        "address": list(filter(None, form.get("address", "").split("\n")[0:4])),
        "country": form.get("country", ""),
        # Ham Info
        "cq": list(filter(None, form.getlist("cq[]")[0:3])),
        "itu": list(filter(None, form.getlist("itu[]")[0:3])),
        "county": list(filter(None, form.getlist("county[]")[0:3])),
        "qth": list(filter(None, form.getlist("qth[]")[0:3])),
        "clubs": list(filter(None, form.get("clubs", "").split("\n")[0:3])),
        "notes": list(filter(None, form.get("notes", "").split("\n")[0:3])),
        # Options
        "qso_lines": form.get("qsolines", 1),
        "call_cbox": True if "callcbox" in form else False,
        "cq_cbox": True if "cqcbox" in form else False,
        "cq_rule": True if "cqrule" in form else False,
        "itu_cbox": True if "itucbox" in form else False,
        "itu_rule": True if "iturule" in form else False,
        "county_hide": False if "countyhide" in form else True,
        "county_cbox": True if "countycbox" in form else False,
        "county_rule": True if "countyrule" in form else False,
        "qth_cbox": True if "qthcbox" in form else False,
        "qth_rule": True if "qthrule" in form else False,
    }

    for field, val in latex_vars.items():
        if isinstance(val, str):
            val = tex_escape(val)
        elif isinstance(val, list):
            for i, item in enumerate(val):
                if isinstance(item, str):
                    val[i] = tex_escape(item)
        latex_vars[field] = val


    try:
        template = latex_jinja_env.get_template('templates/qsl-card.tex')
        latex = template.render(latex_vars)
    except Exception as err:
        return jsonify({"success": False, "error": str(err)})

    # write latex and outputs to files with a hash of the form data as a filename
    latex_fn = str(hash(form))
    if not os.path.isfile("files/" + latex_fn + ".tex"):
        try:
            with open("files/" + latex_fn + ".tex", "w") as latex_file:
                latex_file.write(latex)
        except Exception as err:
            return jsonify({"success": False, "error": str(err)})

    if not os.path.isfile("files/" + latex_fn + ".png"):
        try:
            png_url = render_latex('png', latex)
            png_resp = requests.get(png_url)
            with open("files/" + latex_fn + ".png", "wb") as png_file:
                png_file.write(png_resp.content)
        except Exception as err:
            return jsonify({"success": False, "error": str(err)})

    if not os.path.isfile("files/" + latex_fn + ".pdf"):
        try:
            pdf_url = render_latex('pdf', latex)
            pdf_resp = requests.get(pdf_url)
            with open("files/" + latex_fn + ".pdf", "wb") as pdf_file:
                pdf_file.write(pdf_resp.content)
        except Exception as err:
            return jsonify({"success": False, "error": str(err)})

    return jsonify({"success": True, "file": latex_fn})

def render_latex(fmt: str, latex: str):
    payload = {'code': latex, 'format': fmt}
    response = requests.post(LATEX_URL, data=payload)
    response.raise_for_status()
    resp_data = response.json()
    if resp_data['status'] != 'success':
        raise Exception('Failed to render LaTeX: ' + resp_data["description"])
    return LATEX_URL + '/' + resp_data['filename']

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

@app.route("/file/<string:ft>/<string:fn>")
def get_file(ft: str, fn: str):
    ft = ft.lower()
    fn = fn.lower()

    if ft in ["pdf", "png"]:
        try:
            return send_from_directory("files", fn + "." + ft)
        except FileNotFoundError:
            abort(404)
    elif ft == "tex":
        try:
            return send_from_directory("files", fn + ".tex", as_attachment=True)
        except FileNotFoundError:
            abort(404)
    else:
        abort(404)

@tl.job(interval=timedelta(minutes=15))
def cleanup():
    print("[II] Cleaning up old files...")
    os.system("find files -not -name '.keep' -mtime +1 -exec rm '{}' \;")


tl.start()


def end_tl():
    tl.stop()


atexit.register(end_tl)
