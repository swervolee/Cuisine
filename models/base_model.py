#!/usr/bin/python3
"""
A BASEMODEL FOR THE CLASSES
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    A DEFINATION OF THE BASEMODEL CLASS
    -----------------------------------

    * CREATED_AT - THE TIME AT WHICH THE OBJECT WAS CREATED
    * UPDATED_AT -THE TIME AT WHICH AN OBJECT WAS UPDATED
    * ID - A UNIQUE IDENTITY FOR EACH OBJECT
    """
    def __init__(self, *args, **kwargs):
        """
        CLASS SETTING
        """

        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        try:
                            value = datetime.strptime(
                                value, "%Y-%m-%dT%H:%M:%S.%f")
                        except Exception:
                            value = datetime.utcnow()
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """
        RETURNS  A STRING REPRESENTATION OF THE STRING
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        SAVES AN OBJECT TO FILESTORAGE
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        RETURNS A DICTIONARY REPRESENTATION OF A CLASS
        """
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict

    def delete(self):
        """DELETES SELF FROM THE FILESTORAGE"""
        models.storage.delete(self)
