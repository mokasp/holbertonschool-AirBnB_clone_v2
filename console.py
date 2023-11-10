#!/usr/bin/python3
# KASPER edited 10/31 12:56pm
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os
import re
import shlex


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
        }
    environment = os.getenv('HBNB_TYPE_STORAGE')

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    types = {'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float}

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    # Fixed SyntaxWarnings 10/26/23
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) == dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            storage.shutdown()
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            storage.shutdown()
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class """
        if not args:
            # User didn't specify class name
            print("** class name missing **")
            return

        args_list = args.split(" ")
        class_name = args_list[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.classes[class_name]()
        key_values = args_list[1:]  # skip class_name

        for item in key_values:
            param = item.split("=")
            if (param[1][0] == '"'):
                key = param[0]
                value = param[1][1:-1]  # strip quotes off
                new_instance.__dict__[key] = value.replace("_", " ")
            else:
                key = param[0]
                value = param[1]
                new_instance.__dict__[key] = value.replace("_", " ")
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)
        storage.save()

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <Class name> <param 1> <param 2>...\n")

    def do_show(self, args):
        """ Method to show an individual object """
        if len(args) == 0:
            print("** class name missing **")
            return
        line = args.split()
        if line[0] not in self.classes:
            print("** class doesn't exist **")
            return
        elif len(line) < 2:
            print("** instance id missing **")
            return
        key = f"{line[0]}.{line[1]}"
        all_of_them = storage.all()
        try:
            print(all_of_them[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            dictionary = storage.all()
            for x in dictionary:
                if x == key:
                    new_key = x
            storage.delete(dictionary[new_key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        line = args.split()
        dictionary = storage.all()
        instance_list = []

        if len(args) == 0:
            for key in dictionary:
                instance_list.append(dictionary[key])
            if len(instance_list) != 0:
                for item in instance_list:
                    print(item)
                return
        elif line[0] not in self.classes:
            print("** class doesn\'t exist **")
            return
        else:
            for key in dictionary:
                var = key.split(".")
                if var[0] == line[0]:
                    instance_list.append(dictionary[key])
                for item in instance_list:
                    print(item)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, line):
        """
        Enter the command:
        update <class> <id> <new attribute> "<new attribute value>"
        to add a new attribute to an instance of the specific class.
        """
        args = line.split()
        dictionary = storage.all()
        if len(line) == 0:
            print("** class name missing **")
            return
        elif args[0] not in self.classes.keys():
            print("** class doesn't exist **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in dictionary:
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        the_object = dictionary.get(key)
        object_to_dict = the_object.to_dict()
        class_name = object_to_dict.get('__class__')
        object_dict = self.classes[class_name].__dict__
        strings = re.findall('"([^"]*)"', line)
        attribute_key = args[2]
        attribute_value = strings[0]
        if attribute_key in object_dict:
            if isinstance(object_dict.get(attribute_key), str):
                attribute_value = str(attribute_value)
            elif isinstance(object_dict.get(attribute_key), int):
                attribute_value = int(float(attribute_value))
            elif isinstance(object_dict.get(attribute_key), float):
                attribute_value = float(attribute_value)
        setattr(the_object, attribute_key, attribute_value)
        storage.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
