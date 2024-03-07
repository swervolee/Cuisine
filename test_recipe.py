#!/usr/bin/python3
from models.user import User
from models.recipe import Recipe
from models.tag import Tag

new_user = User(email="test_email", password="Test_password")
new_recipe = Recipe(user_id=new_user.id, title="chicken_masala",
                    introduction="empty",
                    ingredients="empty",
                    instructions="empty")

new_tag = Tag(name="mid-night_meal")

new_recipe.tags = new_tag

print(new_recipe.tags)

new_recipe.untag(new_tag)

print(new_recipe.tag)