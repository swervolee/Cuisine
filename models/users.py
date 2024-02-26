from models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.password = ""
        self.bio = ""
        self.favorites = []
        self.recipes = []
        self.comments = []

    @property
    def Favorites(self):
        return self.favorites

    @Favorites.setter
    def Favorites(self, value):
        if isinstance(value, str):
            self.favorites.append(value)

    def remove_favorite(self, value):
        if value in self.favorites:
            self.favorites.remove(value)

    @property
    def recipes(self):
        return self.recipes

    @recipes.setter
    def recipes(self, value):
        if isinstance(value, str):
            self.recipes.append(value)

    @property
    def comments(self):
        return self.comments

