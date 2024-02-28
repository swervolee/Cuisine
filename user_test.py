#!/usr/bin/python3

from models.user import User
from models import storage

data = {"first_name": "william",
        "last_name": "kubai",
        "email": "williamkubai101@gmail.com",
        "password": 25443533,
        "bio": "i am a software engineer"
        }

new = User(**data)

print(new)


storage.new(new)
storage.save()

key = new.__class__.__name__ + "." + new.id

print(key)
a = storage.all()
print(a.get(key))

