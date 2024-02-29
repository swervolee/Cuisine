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

            if len(arguments) >= 2:
                id = arguments[1]

        if not args or not class_name:
            print("** class name missing **")

        elif class_name not in  classes:
            print("** class doesn't exist **")

        elif not id:
            print("** instance id missing **")

        else:
            obj = models.storage.get(class_name, id)

            if obj:
                print(obj)

            else:
                print("** no instance found **")

    def help_show(self):
        """HELP FOR THE SHOW COMMAND"""

        print("Prints the string representation of an object")
        print("[usage]: show <class_name> <class_id>")

    def do_destroy(self, args=None):
        """DESTROYS AN OBJECT GIVEN ITS CLASS AND ID"""

        class_name = id = None

        if args:
            arguments = args.split(" ")
            if len(arguments) >= 1:
                class_name = arguments[0]

            if len(arguments) >= 2:
                id = arguments[1]

        if not args or not class_name:
            print("** class name missing **")

        elif class_name not in classes:
            print("** class doesn't exist **")

        elif not id:
            print("** instance id missing **")

        else:
            obj = models.storage.get(class_name, id)
            if obj:
                obj.delete()
            else:
                print("** no instance found **")

    def help_destroy(self):
        """
        HELP FOR DESTROY COMMAND
        """
        print("destroy command deletes an object")
        print("[usage] destroy <class name> <id>")

    def do_all(self, args=None):
        """
        Prints a string representation of all classes or
        of the given class
        """
        class_name = None

        if args:
            arguments = args.split(" ")
            class_name = arguments[0]

            if class_name not in classes:
                print("** class doesn't exist **")

            else:
                for obj in models.storage.all(class_name).values():
                    print(obj)

        else:
            for obj in models.storage.all().values():
                print(obj)

    def help_all(self):
        """
        PRINTS A STRING REPRESENTATION OF ALL INSTANCES
        OF THE CLASSES GIVEN.IF NO CLASS GIVEN PRINTS ALL
        INSTANCES
        """
        print("Prints string representation of given class or all")
        print("[Usage] all [class_name]")

    def do_update(self, args):
        """
        UPDATES THE ATTRIBUTES OF AN OBJECT
        """
        class_name = id = attribute = value = None

        if args:
            arguments = args.partition(" ")
            class_name = arguments[0]

            if not class_name:
                print("** class name missing **")
                return

            if class_name not in classes:
                print("** class doesn't exist **")
                return

            arguments = arguments[2].partition(" ")
            id = arguments[0]

            if not id:
                print("** instance id missing **")
                return

            obj = models.storage.get(class_name, id)

            if not obj:
                print("** no instance found **")
                return

            dict_items = []
            if "{" in arguments[2] and "}" in arguments[2]:

                if eval(arguments[2]) == dict:
                    params = eval(arguments[2])

                    for k, v in params.items():
                        dict_items.append(k)
                        dict_items.append(v)
            else:
                arguments = arguments[2].partition(" ")

                if arguments[0].startswith('"') and arguments[0].endswith('"'):
                    attribute = arguments[0][1 : -1]

                else:
                    attribute = arguments[0]

                if not attribute:
                    print("** attribute name missing **")
                    return

                arguments = arguments[2].partition(" ")

                if arguments[0].startswith('"') and arguments[0].endswith('"'):
                    value = arguments[0][1 : -1]
                else:
                    value = arguments[0]

                if  not value:
                    print("** value missing **")
                    return

            if dict_items:
                for i in range(0, len(dict_items)):
                    if i % 2 == 0:
                        setattr(obj, dict_items[i], dict_items[i + 1])

            else:
                setattr(obj, attribute, value)

if __name__ == "__main__":
    CuisineConsole().cmdloop()
