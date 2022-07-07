from flask import Flask

app = Flask(__name__)


def error_handler(error):
    return "You shall not pass"


error_code = 403
app.register_error_handler(error_code, error_handler)
