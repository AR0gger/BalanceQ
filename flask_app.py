
from flask import Flask, request, render_template, jsonify
from Balance import Balanced
import re


app = Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = True


@app.route("/", methods=["GET", "POST"])
def site():
  return render_template('start.html')


@app.route("/process", methods=["POST"])
def process():
    reacts = request.form["reacts"]
    prods = request.form["prods"]
    s = '(?:(?<=")|(?<=\s))\(?[A-Z][\w+\-()]*?(?:(?=")|(?=\s))'
    re_format = re.findall(s, reacts)
    pr_format = re.findall(s, prods)
    for r in re_format:
        if re_format.count(r) > 1:
            re_format.remove(r)
    for p in pr_format:
        if pr_format.count(p) > 1:
            pr_format.remove(p)
    b = Balanced(re_format, pr_format)
    return jsonify({"reaction_info" : b.reaction_printer()})
    # return jsonify({"reaction_info" : ("reacts:", reacts, re_format, "prods:", prods, pr_format)})


