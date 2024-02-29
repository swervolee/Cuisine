#!/usr/bin/python3
"""CUISINE CONSOLE"""
import cmd
from datetime import datetime
import models
from models.base_model import BaseModel
from models.recipe import Recipe
from models.user import User
from models.comment import Comment
from models.tag import Tag
import shlex
import sys


classes = {"BaseModel":BaseModel,
           "Recipe": Recipe,
           "User": User,
           "Commnet": Comment,
           "Tag": Tag
           }

class CuisineConsole(cmd.Cmd):
    """CONSOLE FOR CUISINE"""
    prompt = "(cuisine$) "

    def do_EOF(self, args):
        """
        EXIT ON TERMINATE SIGNAL
        """
        print()
        return True

    def emptyline(self):
        """
        DO NOTHING FOR EMPTY LINE
        """
        return False

    def do_quit(self):
        """
        EXITING THE CONSOLE
        """
        return True

    def preloop(self):
        """
        ONLY SHOW PROMPT WHEN IN INTERACTION MODE
        """
        if not sys.__stdin__.isatty():
            print("cuisine$ ")

    def do_create(self, cls):
        """
        CREATES A NEW INSTANCE OF EITHER OF THE CLASSE
        BaseModel, User, Recipe, Tag or Comment
        """
        if not cls:
            print("** class name missing **")
        elif cls not in classes:
            print("** class doesn't exist **")
        else:
            new = classes[cls]()
            new.save()
            print("{}".format(new.id))

    def help_create(self):
        """
        HELP COMMAND USAGE
        """
        print("Creates a new instance\nUsage create")
        print("[BaseModel | User | Recipe | Tag | Comment")

    def do_show(self, args=None):
        """
        PRINTS A STRING REPRESENTATION OF AN INSTANCE
        BASE ON THE CLASS'S NAME AND ID
        """
        class_name = id = None

        if args:
            arguments = args.split(" ")
            if len(arguments) >= 1:
                class_name = arguments[0]
            if len(arguments) >= 0:
                id = arguments[1]

        if not cmd or not class_name:
            print("** class name missing **")
        elif class_name not in  classes:
            print("** class doesn't exist **")
        elif not id:
            print("** instance id missing **")


if __name__ == "__main__":
    CuisineConsole().cmdloop()
