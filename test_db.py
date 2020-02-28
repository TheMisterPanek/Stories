import unittest
import db

class TestStoriesDataBase(unittest.TestCase):
  def test_create_story(self):
    db.create_story()