from flask import Blueprint, render_template, redirect, request, url_for
from src.backend.benchmark import benchmark

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@views.route("/sus", methods=["GET", "POST"])
def sus():
    if request.method == "POST":
        passwords = str(request.form.get("passwords"))
        pass_list = list(passwords.split(", "))

        results = benchmark(pass_list)
        return render_template("result.html", results=results)

    return render_template("sus.html")
