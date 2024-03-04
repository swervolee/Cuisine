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
from models import storage


classes = {"BaseModel":BaseModel,
           "Recipe": Recipe,
           "User": User,
           "Commmet": Comment,
           "Tag": Tag
           }

dots = ["all", "count", "show", "destroy", "update"]


class CuisineConsole(cmd.Cmd):
    """CONSOLE FOR CUISINE"""
    prompt = "(cuisine$) "
    verbose = True

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

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

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

    def do_update(self, cmd=None):
        """
        Updates a class with new attributes
        or new values
        command syntax: update <clsname> <id> <attrName> <attrValue>
        """
        cls_name, id, attr_name, attr_val = None, None, None, None
        all_objects = storage.all()

        arg_tuple = cmd.partition(" ")  # Extract the clsName
        if arg_tuple[0]:
            cls_name = arg_tuple[0]
        else:
            print("** class name missing **")
            return

        if cls_name not in classes:
            print("** class doesn't exist **")
            return

        arg_tuple = arg_tuple[2].partition(" ")  # Skip clsName and " "
        if arg_tuple[0]:
            id = arg_tuple[0]  # (<id>, " ", <arguments>)
        else:
            print("** instance id missing **")
            return

        key = f"{cls_name}.{id}"  # Key of storage.all() <clsname.id>

        if key not in storage.all():
            print("** no instance found **")
            return
        item_dict = all_objects[key]  # Key the object

        if '{' in arg_tuple[2] and '}' in arg_tuple[2] and\
           type(eval(arg_tuple[2])) is dict:
            cmd_list = []  # If args is dict, list it, [key, value]
            for k, v in eval(arg_tuple[2]).items():
                cmd_list.append(k)
                cmd_list.append(v)
        else:
            arg = arg_tuple[2]
            arg = arg.strip()
            if arg and arg.startswith("\""):  # # Else check for <">
                attr_name = arg[1:arg.find("\"", 1)]  # Extract btwn ""
                arg = arg[arg.find("\"", 1) + 1:]  # Move the cursor frwd
            arg = arg.partition(" ")  # Else partition again

            if not attr_name and arg[0] != " ":  # if no quotations
                attr_name = arg[0]
            if arg[2] and arg[2][0] == "\"":
                attr_val = arg[2][1: arg[2].find("\"", 1)]
            if arg[2] and not attr_val:
                attr_val = arg[2].partition(" ")[0]
            cmd_list = [attr_name, attr_val]
        for i in range(len(cmd_list)):
            if i % 2 == 0:  # Parse the commands in two's [Key, Value]
                attr_name, attr_value = cmd_list[i], cmd_list[i + 1]
                if not attr_name:
                    print("** attribute name missing **")
                    return
                if not attr_value:
                    print("** value missing **")
                    return
                if hasattr(eval(cls_name), attr_name):  # If attr exists
                    attr_value = type(getattr(eval(cls_name),  # cast val
                                              attr_name))(attr_value)
                setattr(item_dict, attr_name, attr_value)
                item_dict.save()  # Save the changes to file.json

    def help_update(self):
        """
        UPDATES AN INSTANCE'S ATTRIBUTES
        """
        print("Updates the attribute of an instance")
        print("[usage] update <class name> <class id> <attribute> <value>")

    def do_count(self, arg):
        """
        COUNTS THE NUMBER OF CLASS INSTANCES
        """
        count = 0;
        for item in models.storage.all().values():
            if item.__class__ == arg or item.__class__.__name__ == arg:
                count += 1
        print(count)

    def help_count(self):
        """
        COUNTS INSTANCES
        """
        print("Counts number of instances of a class")
        print ("[usage] count <class name>")

    def default(self, cmd):
        """
        Handles class commands
        Class commands syntax is:
            <ClsName>.<Commmand><(Arguments)>
        if the command syntax is wrong print
        error message
        """
        line = cmd[:]  # copy the command
        if not("." in line and "(" in line and ")" in line):
            print(f"*** Unknown syntax: {cmd}")  # <ClsName>.<Command>(Args)
            return
        cls_name = line[: line.find(".", 1)]  # extract the cls name
        if cls_name not in classes:  # Look it up in the clslist
            print(f"*** Unknown syntax: {line}")
            return
        comd = line[line.find(".", 1) + 1: line.find("(", 1)]  # Eg update, all
        if comd not in dots:
            print(f"*** Unknown syntax: {line}")
            return
        if comd == "all":  # prints all the classes in file.json
            self.do_all(cls_name)
        if comd == "count":  # Count the number of instances of a class
            self.do_count(cls_name)
        if comd == "show":  # prints a string representation of a cls
            id = line[line.find("(", 1) + 1: line.find(")", 1)]
            joined_command = " ".join([cls_name, id])
            self.do_show(joined_command)
        if comd == "destroy":  # Destroys an instance
            id = line[line.find("(", 1) + 1: line.find(")", 1)]
            joined_command = " ".join([cls_name, id])
            self.do_destroy(joined_command)
        if comd == "update":  # Updates an isntance with new attrs/values
            arg = line[line.find("(", 1) + 1: line.find(")", 1)]  # Extract
            arg = arg.partition(", ")  # The args are comma seperated so ..
            id = arg[0]  # Extract the id which is the first args
            cmd2 = arg[2]  # Jump id and " ".Extracts args after id
            cmd2 = cmd2.strip()  # Eliminate trailing whitespaces
            if cmd2 and cmd2[0] == "{" and cmd2[-1] == "}"\
               and type(eval(cmd2)) is dict:
                attrs = cmd2  # If its a dict, take it as it is
            else:
                attrs = cmd2.replace(",", "")  # Else eliminate commas
            joined = " ".join([cls_name, id, attrs])  # Join the commands
            self.do_update(joined)

if __name__ == "__main__":
    CuisineConsole().cmdloop()
