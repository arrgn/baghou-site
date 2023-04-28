from flask import render_template, redirect, abort, request

from client import app, store
from client.forms.login_form import LoginForm
from client.forms.reg_form import RegForm


from client.http.api import Api


@app.get("/")
def home():
    return render_template("home.html", store=store)


@app.get("/auth/reg")
def reg_get():
    if store.is_auth:
        return redirect("/")

    form = RegForm()

    return render_template("reg.html", form=form, store=store)


@app.post("/auth/reg")
def reg_post():
    if store.is_auth:
        return redirect("/")

    form = RegForm()

    if form.validate_on_submit():
        res = store.registration(form.username.data, form.email.data, form.password.data)
        return res
    return render_template("reg.html", form=form, store=store)


@app.get("/auth/login")
def login_get():
    form = LoginForm()
    return render_template("login.html", form=form, store=store)


@app.post("/auth/login")
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        res = store.login(form.email.data, form.password.data)
        return res
    return render_template("login.html", form=form, store=store)


@app.get("/auth/logout")
def logout_get():
    res = store.logout()
    return res


@app.get("/profile/<gtag>")
def profile(gtag):
    res = store.get_user_by_gtag(gtag)
    if "user" not in res:
        return abort(404)
    user = res["user"]
    return render_template("profile.html", store=store, user=user, owner=(user["gtag"] == store.user["gtag"]))


@app.get("/profile/edit")
def profile_edit():
    if "access_token" not in request.cookies:
        return redirect('/')
    return render_template("profile-edit.html", store=store, user=store.user)

@app.get("/social")
def social():
    res = ''
    return render_template("social.html", store=store)


@app.before_request
def check_auth():
    store.check_auth()


@app.errorhandler(Exception)
def http_error_handler(e):
    return render_template("error.html", store=store, error=e)
