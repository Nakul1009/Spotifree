from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# your foo function
def foo(param):
    return 'Nigga'


# Defining the behavior of the endpoint "/api/run_foo"
@app.route("/api/run_foo")
def this_function_name_doesnt_really_matter():
    foo_param = request.args.get("param_to_foo", type=str)

    data = {"result": foo(foo_param)}
    return jsonify("hello")