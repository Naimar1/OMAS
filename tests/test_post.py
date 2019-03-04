import unittest
from app.models import Post


class PostTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Post class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_post = Post(1, 'Python Must Be Crazy','A thrilling new Python Series', 2018)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Post))
