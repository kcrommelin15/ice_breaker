from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
load_dotenv()
from ice_breaker import ice_break_with

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary, photo_url = ice_break_with(name = name)
    return jsonify(
        {
            "summary_and_facts":summary.to_dict(),
            "picture_url":photo_url
        }
    )

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=False)