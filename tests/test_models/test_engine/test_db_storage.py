#!/usr/bin/python3
"""test for file storage"""
import unittest
import pep8
import json
import os
from os import getenv
import MySQLdb
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
class TestDBStorage(unittest.TestCase):
    '''this will test the DBStorage'''

    @classmethod
    def setUpClass(self):
        """set up for test"""
        self.User = getenv("HBNB_MYSQL_USER")
        self.Passwd = getenv("HBNB_MYSQL_PWD")
        self.Db = getenv("HBNB_MYSQL_DB")
        self.Host = getenv("HBNB_MYSQL_HOST")
        self.db = MySQLdb.connect(host=self.Host, user=self.User,
                                  passwd=self.Passwd, db=self.Db,
                                  charset="utf8")
        self.query = self.db.cursor()
        self.storage = DBStorage()
        self.storage.reload()

    @classmethod
    def teardown(self):
        """at the end of the test this will tear it down"""
        self.query.close()
        self.db.close()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_pep8_DBStorage(self):
        """Test Pep8"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_read_tables(self):
        """existing tables"""
        self.query.execute("SHOW TABLES")
        output = self.query.fetchall()
        self.assertEqual(len(output), 7)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_no_element_user(self):
        """no elem in users"""
        self.query.execute("SELECT * FROM users")
        output = self.query.fetchall()
        self.assertEqual(len(output), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_no_element_cities(self):
        """no elem in cities"""
        self.query.execute("SELECT * FROM cities")
        output = self.query.fetchall()
        self.assertEqual(len(output), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_add(self):
        """Test same size between storage() and existing db"""
        self.query.execute("SELECT * FROM states")
        output = self.query.fetchall()
        self.assertEqual(len(output), 0)
        state = State(name="KAKAMEGA")
        state.save()
        self.db.autocommit(True)
        self.query.execute("SELECT * FROM states")
        output = self.query.fetchall()
        self.assertEqual(len(output), 1)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_get(self):
        """Test the method for obtaining an instance from the database storage"""
        state_data = {"name": "TEXAS"}
        state_instance = State(**state_data)
        storage.new(state_instance)
        storage.save()
        retrieved_instance = storage.get(State, state_instance.id)
        self.assertEqual(retrieved_instance, state_instance, "Instances are not equal")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_count(self):
        """Test the count method of the database storage"""
        state_data = {"name": "VECINDAD"}
        state_instance = State(**state_data)
        storage.new(state_instance)
        city_data = {"name": "MEXICO", "state_id": state_instance.id}
        city_instance = City(**city_data)
        storage.new(city_instance)
        storage.save()
        count_all_instances = storage.count()
        self.assertEqual(count_all_instances, len(storage.all()), "Count mismatch")


if __name__ == "__main__":
    unittest.main()
