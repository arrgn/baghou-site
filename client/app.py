from flask import render_template, make_response, redirect

from client import app, store
from client.forms.login_form import LoginForm
from client.forms.reg_form import RegForm


@app.get("/")
def home():
    return render_template("home.html")


@app.get("/auth/reg")
def reg_get():
    form = RegForm()
    return render_template("reg.html", form=form)


@app.post("/auth/reg")
def reg_post():
    form = RegForm()
    if form.validate_on_submit():
        res = store.registration(form.username.data, form.email.data, form.password.data)
        return res
    return render_template("reg.html", form=form)


@app.get("/auth/login")
def login_get():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.post("/auth/login")
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        res = store.login(form.email.data, form.password.data)
        return res
    return render_template("login.html", form=form)


@app.errorhandler(Exception)
def http_error_handler(e):
    print(e)
    return {}