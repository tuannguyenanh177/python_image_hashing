import psycopg2
from psycopg2.extras import execute_values
from flask import Flask, jsonify, request
from image_hashing.src.gen_hash import twos_complement, genHash
from timeit import default_timer as timer

app = Flask(__name__)
conn = psycopg2.connect(database = "postgres", user = "postgres", password = "myhcmuspassword", host = "127.0.0.1")
cursor = conn.cursor()
print("Connection Successful to PostgreSQL")

# @app.route('/save', methods=['POST'])
# def save():
#     jsonList = list(request.get_json())
#     response = jsonList[0]["url"]

#     values = [(dic["hash"], dic["url"]) for dic in jsonList]

#     execute_values(cursor,
#     "INSERT INTO hashes(hash, url) VALUES %s",
#     values)
#     conn.commit()

#     return jsonify(response)

@app.route('/search', methods=['POST'])
def search():
  if request.files['image']:
    start = timer()
    img = request.files['image']
    hashInt = genHash(img)
    gen_hash_time = round(timer() - start, 3)

    start = timer()
    maxDifference = 3
    cursor.execute(f"SELECT hash, url FROM hashes WHERE hash <@ ({hashInt}, {maxDifference})")
    hashRows = cursor.fetchall()
    result = [{"hash": x[0], "url": x[1]} for x in hashRows]
    query_time = round(timer() - start, 3)

    response = {
      "gen_hash_time": gen_hash_time,
      "query_time": query_time,
      "data": result
    }

    return jsonify(response)
  else:
    return "Where is the image?"
