import unittest
from app.models import Comment,User

class CommentModelTest(unittest.TestCase):

    def setUp(self):
        self.new_comment = Comment(body = 'very nice progress!!')

    def tearDown(self):
        Coment.query.delete()
       

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0

    def test_get_comment_by_id(self):

        self.new_comment.save_comment()
        got_comments = Comment.get_comments()
        self.assertTrue(len(got_comments) == 1)

if __name__ == '__main__':
    unittest.main()
