#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
import uuid
from unittest import mock
import os
BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in ['models/base_model.py',
                     'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""
    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        """
        SET UP CLASS
        """
        self.base_model = BaseModel()

    def test_instance_creation(self):
        """
        TEST IF AN INSTANCE IS BEING CREATED
        """
        self.assertIsInstance(self.base_model, BaseModel)

    def test_id_generation(self):
        """
        TEST IF AN ID IS BEING GENERATED
        """
        self.assertTrue(hasattr(self.base_model, 'id'))
        self.assertIsInstance(self.base_model.id, str)
        self.assertNotEqual(self.base_model.id, '')

    def test_created_at_and_updated_at(self):
        """
        TEST IF UPDATED AT AND CREATED AT IS BEING
        GENERATED CORRECTLY
        """
        self.assertTrue(hasattr(self.base_model, 'created_at'))
        self.assertTrue(hasattr(self.base_model, 'updated_at'))
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)
        self.assertEqual(
            self.base_model.created_at, self.base_model.updated_at)

    def test_str_representation(self):
        """
        TEST IF STR REPRESENTATION IS BEING CORRECTLY
        GENERATED
        """
        string_representation = str(self.base_model)
        self.assertIn('[BaseModel]', string_representation)
        self.assertIn('id', string_representation)
        self.assertIn('created_at', string_representation)
        self.assertIn('updated_at', string_representation)

    @unittest.skipIf(os.getenv("CUISINE_TYPE_STORAGE") == "db", "FILESTORAGE")
    def test_to_dict_method(self):
        """
        TEST IF OBJECT TO DICTIONARY IS WORKING CORRECT
        """
        base_model_dict = self.base_model.to_dict()
        self.assertIsInstance(base_model_dict, dict)
        self.assertIn('__class__', base_model_dict)
        self.assertIn('id', base_model_dict)
        self.assertIn('created_at', base_model_dict)
        self.assertIn('updated_at', base_model_dict)
        self.assertEqual(base_model_dict['__class__'], 'BaseModel')
        self.assertEqual(base_model_dict['id'], self.base_model.id)
        self.assertEqual(base_model_dict[
            'created_at'], self.base_model.created_at.isoformat())
        self.assertEqual(base_model_dict[
            'updated_at'], self.base_model.updated_at.isoformat())

    @unittest.skipIf(os.getenv("CUISINE_TYPE_STORAGE") == "db", "filestorge")
    def test_save_method(self):
        """
        TEST FILE STORAGE SAVING
        """
        initial_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(initial_updated_at, self.base_model.updated_at)

    @unittest.skipIf(os.getenv("CUISINE_TYPE_STORAGE") == "db", "FILESTRAGE")
    def test_delete_method(self):
        """
        TEST DELETION FROM FILE STORAGE
        """
        # Save the object first
        self.base_model.save()
        self.assertTrue(hasattr(self.base_model, 'id'))
        object_key = self.base_model.__class__.__name__
        object_key += "." + self.base_model.id
        all_objects = models.storage.all().values()
        self.assertTrue(self.base_model in all_objects)
        self.base_model.delete()
        all_objects = models.storage.all().values()
        self.assertFalse(self.base_model in all_objects)

    def test_init_method_with_parameters(self):
        """
        TEST INSTANCIATION
        """
        test_id = str(uuid.uuid4())
        test_created_at = datetime.utcnow()
        test_updated_at = datetime.utcnow()
        test_base_model = BaseModel(
            id=test_id, created_at=test_created_at.isoformat(
            ), updated_at=test_updated_at.isoformat())
        self.assertEqual(test_base_model.id, test_id)
        self.assertEqual(test_base_model.created_at, test_created_at)
        self.assertEqual(test_base_model.updated_at, test_updated_at)
