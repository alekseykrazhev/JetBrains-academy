from flask import Flask, render_template

app = Flask(__name__)

forbidden = 403
not_found = 404


@app.errorhandler(not_found)
def page_not_found(e):
    if e:
        return
    return render_template('404.html')


@app.errorhandler(forbidden)
def forbidden(e):
    if e:
        return
    return render_template('403.html')
