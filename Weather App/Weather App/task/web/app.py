from flask import Flask, render_template
import sys

app = Flask(__name__)


def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return "Hello, world!"


# app.register_error_handler(404, page_not_found)


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
