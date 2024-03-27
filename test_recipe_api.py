#!/usr/bin/python3
import requests
import json
from models.recipe import Recipe

recipe = requests.get("http://0.0.0.0:5000/api/v1/recipes/7eebacca-be71-450c-bbde-11f35226843c").json()

print(recipe)
recipe = eval(recipe["__class__"])(**recipe)

r = requests.post("http://0.0.0.0:5000/api/v1/users/98503c43-481b-4b76-92ca-cef42f4bf16f/recipes",
                  data=json.dumps(recipe.to_dict()),
                  headers={"Content-Type": "application/json"})

print(r.text)