import unittest
import app
import main
import tweepy

class TestApp (unittest.TestCase):

    def test_samples_are_acquired(self):
        """Test that main.get_samples() returns samples that aren't empty strings"""