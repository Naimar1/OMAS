# import unittest
# from app.models import Movie

# class MovieTest(unittest.TestCase):
#     '''
#     Test Class to test the behaviour of the Movie class
#     '''

#     def setUp(self):
#         '''
#         Set up method that will run before every Test
#         '''
#         self.new_movie = Movie(1234,'Python Must Be Crazy','A thrilling new Python Series','/khsjha27hbs',8.5,129993)

#     def test_instance(self):
#         self.assertTrue(isinstance(self.new_movie,Movie))

# if __name__ == '__main__':
#     unittest.main()


import unittest
from app.models import Pitch

class PitchModelTest(unittest.TestCase):

    def setUp(self):
        self.new_pitch = Pitch(id = 1, title = 'What Makes a Song Sad', pitch_content = 'Where does sad music get its sadness from? And whom should you ask—a composer or a cognitive psychologist?', category = 'Pickup Lines', upvote = 10, downvote = 12, author = 'DANIEL WATTENBERG'
)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)