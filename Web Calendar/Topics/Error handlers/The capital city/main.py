from flask import Flask

app = Flask(__name__)


@app.route("/capital/<country>")
def capital(_country):
    error_404 = 404
    capitals_dictionary = {"Russia": "Moscow", "Ukraine": "Kiev", "USA": "Washington"}

    if _country in capitals_dictionary.keys():
        return capitals_dictionary[_country]

    return abort(error_404, "Resource not found")
