import models
from models.user import User

user = User(**{
    "email": "williamkubai",
    "password": "password",
    "first_name": "William",
    "last_name": "Kubai",
    "bio": "I am a software developer"
})

print(user)