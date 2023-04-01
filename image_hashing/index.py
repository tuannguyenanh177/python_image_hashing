import psycopg2
from psycopg2.extras import execute_values
from flask import Flask, jsonify, request
from image_hashing.src.gen_hash import twos_complement

app = Flask(__name__)
conn = psycopg2.connect(database = "postgres", user = "postgres", password = "myhcmuspassword", host = "127.0.0.1")
cursor = conn.cursor()
print("Connection Successful to PostgreSQL")

@app.route('/save', methods=['POST'])
def save():
    jsonList = list(request.get_json())
    response = jsonList[0]["url"]

    values = [(dic["hash"], dic["url"]) for dic in jsonList]

    execute_values(cursor,
    "INSERT INTO hashes(hash, url) VALUES %s",
    values)
    conn.commit()

    return jsonify(response)
