import json
import mysql.connector
import math

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",  # change this
    database="recipes_db"
)
cursor = db.cursor()

# Load JSON file
with open("US_recipes_null.json") as file:
    data = json.load(file)

for key, recipe in data.items():
    rating = recipe.get("rating")
    prep_time = recipe.get("prep_time")
    cook_time = recipe.get("cook_time")
    total_time = recipe.get("total_time")

    # Handle NaN or non-numeric
    def parse_num(val):
        return None if val in ['NaN', None] or (isinstance(val, float) and math.isnan(val)) else val

    cursor.execute("""
        INSERT INTO recipes (cuisine, title, rating, prep_time, cook_time, total_time,
                             description, nutrients, serves)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        recipe.get("cuisine"),
        recipe.get("title"),
        parse_num(rating),
        parse_num(prep_time),
        parse_num(cook_time),
        parse_num(total_time),
        recipe.get("description"),
        json.dumps(recipe.get("nutrients")),
        recipe.get("serves")
    ))

db.commit()
cursor.close()
db.close()
