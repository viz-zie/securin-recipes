from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import json

app = Flask(__name__)
CORS(app)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="recipes_db"
    )

@app.route("/api/recipes", methods=["GET"])
def get_recipes():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM recipes")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT * FROM recipes ORDER BY rating DESC LIMIT %s OFFSET %s", (limit, offset))
    data = cursor.fetchall()
    for r in data:
        r["nutrients"] = json.loads(r["nutrients"])

    db.close()
    return jsonify({"page": page, "limit": limit, "total": total, "data": data})

@app.route("/api/recipes/search", methods=["GET"])
def search():
    title = request.args.get("title")
    rating = request.args.get("rating")
    cuisine = request.args.get("cuisine")
    total_time = request.args.get("total_time")
    calories = request.args.get("calories")

    filters = []
    values = []

    if title:
        filters.append("title LIKE %s")
        values.append(f"%{title}%")
    if rating:
        filters.append("rating >= %s")
        values.append(float(rating))
    if cuisine:
        filters.append("cuisine = %s")
        values.append(cuisine)
    if total_time:
        filters.append("total_time <= %s")
        values.append(int(total_time))
    if calories:
        filters.append("JSON_EXTRACT(nutrients, '$.calories') <= %s")
        values.append(calories)

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""
    query = f"SELECT * FROM recipes {where_clause}"

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, values)
    results = cursor.fetchall()
    for r in results:
        r["nutrients"] = json.loads(r["nutrients"])
    db.close()

    return jsonify({"data": results})

if __name__ == "__main__":
    app.run(debug=True)
