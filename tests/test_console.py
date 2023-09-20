#!/usr/bin/python3
"""test for the console"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
import console
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):
    """this will test the console"""

    @classmethod
    def setUpClass(cls):
        """setup class"""
        cls.console = HBNBCommand()

    @classmethod
    def teardown(cls):
        """clear at the ends"""
        del cls.console

    @classmethod
    def tearDown(self):
        """clear at the ends of each test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_each_function_is_documented(self):
        """check if each function is documented"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """when the user doesn't enter anything"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("\n")
            self.assertEqual('', output.getvalue())

    def test_console_create_with_missing_class_name(self):
        """test the create console command with missing class name"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create")
            self.assertEqual(
                    "** class name missing **\n",
                    output.getvalue())

    def test_console_create_not_exist_class_name(self):
        """test the create console not exist class name"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create NotClass")
            self.assertEqual(
                    "** class doesn't exist **\n",
                    output.getvalue())

    def test_console_create_without_params(self):
        """test create command without params"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create State")
            self.assertEqual(36, len(output.getvalue().strip()))

    def test_console_create_with_params(self):
        """test create command with params"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297')
            _id = output.getvalue().strip()
            self.assertEqual(36, len(_id))
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd(f"show Place {_id}")
            out = output.getvalue()
            self.assertIn(_id, out)
            self.assertEqual("[Place] ", out[:8])
