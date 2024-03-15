#!/usr/bin/python3

import requests
from models.recipe import Recipe


api_endpoint = "https://api.edamam.com/search"
app_id = "2168d975"
app_key = "ae2d6ab735750d243e12f84f5778c59b"
query = ["beef", "chicken", "fish"]
cuisine_type = ["American", "Asian", "British", "Eastern Europe", "French", "Indian"]
diet_labels = "balanced"
health_labels = "alcohol-free"
user_id = "750fdb4e-b14a-4d01-9986-72c0df0a5294"


for i in cuisine_type:
    for j in query:
        params = {
            "q": j,
            "cuisineType": i,
            "diet": diet_labels,
            "health": health_labels,
            "app_id": app_id,
            "app_key": app_key
        }


        response = requests.get(api_endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            for recipe in data["hits"]:
                recipe_name = recipe["recipe"]["label"]
                ingredients = recipe["recipe"]["ingredientLines"]
                instructions = recipe["recipe"]["url"]
                recipe_label = recipe["recipe"]["label"]

                print(recipe_name, ingredients, instructions, recipe_label, end="\n")
                print()

            ingredients = "\n".join(ingredients)
            new = Recipe(title=recipe_name, user_id=user_id, introduction=recipe_label, ingredients=ingredients, instructions=instructions)
            new.save()
        else:
            print("Error:", response.status_code)
