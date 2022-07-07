from flask import Flask, jsonify

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"msg": "Something was not found", "code": 404})
