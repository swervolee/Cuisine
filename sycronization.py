#!/usr/bin/python3

import models
import json

if models.storage_type == db:
    filename = "test.json"

    objs = ["Recipe", "User", "Tag", "Comment"]

    for cls in objs:
        fetch = models.storage.all(cls).values()

        for obj in fetch:
            data = obj.to_dict()
            with open(filename, "a") as f:
                json.dump(data, f)
