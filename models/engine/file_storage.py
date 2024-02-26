#!/usr/bin/python3
import json
"""
 A STORAGE FOR OBJECTS
"""


class FileStorage():
    """
    A CLASS TO CREATE A FILE STORAGE FOR OUR OBJECTS
    """

    __file_path = "storage.json"
    __objects = {}


    def all(self, cls=None):
        """RETURNS A DICTIONARY WITH ALL CREATED OBJECTS"""

        if cls:
            result = {}
            for k, v in self.__objects.items():
                if cls == v.__class__ or cls == v.__class__.__name__:
                    result[k] = v
            return result
        return self.__objects

    def new(self, obj):
        """CREATES A NEW OBJECT IN __objects"""

        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj


    def save(self):
        """WRITES __objects TO A FILE"""
        data = {}

        for key in self.__objects:
            data[key] = self.__objects[key].to_dict()

        with open(self.__file_path, 'w') as f:
            json.dump(data, f)


    def reload(self):
        """DESERIALIZES OBJECTS FROM THE JSON FILE"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f).items()):
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except Exception:
            pass # if the file does not exist do nothing

    def delete(self, obj=None):
        """DELTE AN OBJECT FROM self.__objects"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]


    def close(self):
        """CALLS RELOAD TO DESERIALIZE THE OBJECTS"""
        self.reload()

    def get(self, cls, id):
        """
        RETURNS AN OBJECT BASED ON THE CLASS NAME AND THE ID
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        COUNT THE NUMBER OF OBJECTS IN STORAGE
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
