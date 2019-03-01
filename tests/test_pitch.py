import unittest
from app.models import Pitch

class PitchModelTest(unittest.TestCase):

    def setUp(self):
        self.new_pitch = Pitch(id = 1, title = 'Python', pitch_content = 'Programming language that helps to build application', category = 'courses pitches', like = 3, dislike = 0)


    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

if __name__ == '__main__':
    unittest.main()