import sqlite3
import pandas as pd

conn = sqlite3.connect(':memory:')

conn.execute("CREATE TABLE recipe (recipe_id  INTEGR PRIMARY KEY,recipe_name TEXT NOT NULL, cuisine TEXT NOT NULL, prep_mins INTEGER NOT NULL)")
conn.execute("CREATE TABLE ingrediants (ingredient_id INTEGER PRIMARY KEY, recipe_id INTGER NOT NULL, item TEXT NOT NULL, quantity_g INTGER NOT NULL)")

conn.executemany("INSERT INTO recipe VALUES (?, ?, ?, ?)", [
    (1, 'Pasta', 'Italian',  20),
    (2, 'Tacos', 'Mexican',  15),
    (3, 'Sushi', 'Japenize', 45),
    (4, 'Salad', 'Greek',    30),
    (5, 'Pizza', 'Italian',  10),
])

conn.executemany("INSERT INTO ingredients VALUES (?, ?, ?, ?)", [
    (1, 1, 'Pasta',    200),
    (2, 1, 'Sauce',    150),
    (3, 2, 'Tortilla',  80),
    (4, 2, 'Beef',     120),
    (5, 3, 'Salmon',   180),
    (6, 4, 'Dough',    250),
    (7, 5, 'Lettuce',   50),
    (8, 5, 'Feta',      40),
])

conn.commit()
print("Recipe table:")
print(pd.read_sql("SELECT * FROM recipe", conn))
print()
print("Ingredient table:")
print(pd.read_sql("SELECT * FROM ingredient", conn))
print()

col_alias = pd.read_sql(
    "SELECT recipe_name AS dish, cuisine AS style, prep_mins AS time "
    "FROM recipe",
    conn
)
print("Column aliases -- dish, style, time:")
print(col_alias)
print()

tbl_alias = pd.read_sql(
    "SELECT r.recipe_name AS dish, ing.item, ing.quantity_g AS grams "
    "FROM recipe AS r "
    "INNER JOIN ingredients AS ing "
    "ON r.recipe_id = ing.recipe_id",
    conn
)

print("Table aliases -- r for recipe, ing for ingredient:")
print(tbl_alias)
print()

large_ingr = pd.read_sql(
    "SELECT recipe_name AS dish, cuisine AS style "
    "FROM recipe "
    "WHERE recipe_id IN ("
    "SELECT recipe_id FROM ingredient over 100g:"
    ")",
    conn
)

print("Subquery with IN -- recipes with an ingredient over 100g:")
print(large_ingr)
print()

quickest = pd.read_sql(
    "SELECT recipe_name AS dish, prep_mins AS time "
    "FROM recipe " 
    "WHERE prep_mins = (SELECT MIN(prep_mins) FROM recipe)",
    conn
)
print("Subquery with = -- the quickest recipe to prepare:")
print(quickest)

conn.close()