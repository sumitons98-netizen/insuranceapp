import json
import os
import threading

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
_lock = threading.Lock()

FIELDS = ["insured_name", "country", "premium", "limit", "insured_address"]

DEFAULT_RECORD = {
    "insured_name": "",
    "country": "",
    "premium": "",
    "limit": "",
    "insured_address": "",
}


def load_record():
    if not os.path.exists(DATA_FILE):
        return dict(DEFAULT_RECORD)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_RECORD)
    record = dict(DEFAULT_RECORD)
    record.update({k: data.get(k, "") for k in FIELDS})
    return record


def save_record(record):
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)


@app.route("/")
def index():
    return render_template("index.html", record=load_record())


@app.route("/api/record", methods=["GET"])
def get_record():
    return jsonify(load_record())


@app.route("/api/record", methods=["PUT", "POST"])
def update_record():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "JSON object body required"}), 400

    unknown = [k for k in payload if k not in FIELDS]
    if unknown:
        return jsonify({"error": f"unknown field(s): {', '.join(unknown)}"}), 400

    with _lock:
        record = load_record()
        for key in FIELDS:
            if key in payload:
                value = payload[key]
                record[key] = "" if value is None else str(value)
        save_record(record)

    return jsonify(record)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
