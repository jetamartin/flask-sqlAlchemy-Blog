from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

#########################################################
# Test cases to add:
# None at this time
#########################################################


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        db.drop_all()
        db.create_all()

        User.query.delete()
        user = User(first_name="Joe", last_name="Blow", image_url="http://www.profile.com")
        user1 = User(first_name="Franklin", last_name="Jones", image_url="http://www.profile.com")
        db.session.add(user1)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
        # Create two posts and associate them with user 1
        post = Post(title = "Post 1",
                     content = "This is the content for Post 1",
                     user_id = self.user_id)
        # post2 = Post(title = "Post 2",
        #             content = "This is the content for Post 2",
        #             user_id = self.user_id)  

        tag1 = Tag(name = 'Awesome')
        tag2 = Tag(name = 'Wow!')
 
        post.tags.append(tag1)
        post.tags.append(tag2)
 
        db.session.add(post)
        db.session.commit()

        # import pdb; pdb.set_trace()
        self.post_id = post.id
        self.tag_id = tag1.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_custom_404_page(self):
        """ Test custom 404 page displayed on bad route"""
        with app.test_client() as client:
            resp = client.get("/xyz")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)
            self.assertIn('What you were looking for is just not there!', html)        


    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            import pdb; pdb.set_trace()
            self.assertEqual(resp.status_code, 200)
            # Note..the following also test for alphabetical sorting of users
            self.assertIn('<li><a href="/users/2">Joe Blow</li></a>\n    </ul>\n    \n    <ul>\n      <li><a href="/users/1">Franklin Jones</li></a>', html)
            # self.assertIn('Franklin Jones</li>', html)

    def test_show_new_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Name', html)

    def test_show_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit', html)

    def test_edit_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Edit User</h2>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('All Users',html)
            self.assertNotIn('Joe Blow</li>', html)

#########################################################
## PostViewsTestCase
#########################################################


class PostViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add test User and associated Post ."""

        db.drop_all()
        db.create_all()

        # User.query.delete()
        Post.query.delete()
        Tag.query.delete()

        #  Create User
        user = User(first_name="Joe", last_name="Blow", image_url="http://www.profile.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        # Create two posts and associate them with user 1
        post = Post(title = "Post 1",
                     content = "This is the content for Post 1",
                     user_id = self.user_id)

        # post2 = Post(title = "Post 2",
        #             content = "This is the content for Post 2",
        #             user_id = self.user_id)  

        tag1 = Tag(name = 'Awesome')
        tag2 = Tag(name = 'Wow!')
 
        post.tags.append(tag1)
        post.tags.append(tag2)
 
        db.session.add(post)
        db.session.commit()

        # import pdb; pdb.set_trace()
        self.post_id = post.id
        self.tag_id = tag1.id

        # db.session.add(post)
        # # db.session.add(post2)
        # db.session.commit()

        # self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()  


    def test_root_page(self):
        """ Test root page that list last 5 posts """
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            # import pdb; pdb.set_trace()
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)
            self.assertIn('Awesome', html)
            self.assertIn('Wow!', html)


    def test_show_new_post_form(self):
        """Test that new Post form is displayed properly """
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)
            # import pdb; pdb.set_trace()
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post for', html)
            self.assertIn('Awesome', html)
            self.assertIn('Wow!', html)



    def test_add_new_post(self):
        """ Test that new Post are added to the DB """ 
        with app.test_client() as client:
            data = {'postTitle' :'Post2', 'postContent':"This is content for Post2"}
            resp = client.post(f'/users/{self.user_id}/posts/new', data = data, follow_redirects=True )       
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post2', html)

    def test_show_post(self):
        """Test that details of Post are displayed properly"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('This is the content for Post 1',html)
            self.assertIn('Awesome', html)
            self.assertIn('Wow!', html)


    def test_delete_post(self):
        """ Test that deleted Post is removed"""

        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('This is the content for Post 1',html)



    def test_show_post_edit_form(self):
        """ Test that Edit Post View is displayed """
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Post', html)
            self.assertIn('Awesome', html)
            self.assertIn('Wow!', html)
            self.assertIn('checked', html)
        

    def test_save_post_edits(self):
        """Test that edited post is saved """
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new', data={'postTitle':'Post2.2', 'postContent':'This is the content for Post2.2'}, follow_redirects=True )       
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post2.2', html)



# #########################################################
# ## TagViews Test Cases
# #########################################################

class TagViewsTestCase(TestCase):
    """Tests for views for Tags."""

    def setUp(self):
        """Add test User and associated Post ."""
        db.drop_all()
        db.create_all()
        
        User.query.delete()
        Post.query.delete()
        Tag.query.delete()
        PostTag.query.delete()

        #  Create User
        user = User(first_name="Joe", last_name="Blow", image_url="http://www.profile.com")
# +++++++++++++++++++++++++++++++++++++++++++
        db.session.add(user)
        db.session.commit()
# +++++++++++++++++++++++++++++++++++++++++++
        self.user_id = user.id

        # Create two posts and associate them with user 1
        post = Post(title = "Post 1",
                     content = "This is the content for Post 1",
                     user_id = self.user_id)

        # post1 = Post(title = "Post 2",
        #             content = "This is the content for Post 2",
        #             user_id = self.user_id)  

        db.session.add(post)
        db.session.commit()
        # db.session.add(post1)
        # db.session.commit()

        # self.post_id = post.id

        tag1 = Tag(name = 'Awesome')
        tag2 = Tag(name = 'Wow!')
        tag3 = Tag(name = 'Ok')
        tag4 = Tag(name = 'Noyce!')


        post.tags.append(tag1)
        post.tags.append(tag2)
        post.tags.append(tag3)
        post.tags.append(tag4)

        db.session.add(post)
        db.session.commit()

        # import pdb; pdb.set_trace()
        self.post_id = post.id
        self.tag_id = tag1.id



    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()  



    def test_show_add_new_tag_form(self):
        """ Test that Add new Tag form is displayed """
        with app.test_client() as client:
            resp = client.get('/tags/new')
            html = resp.get_data(as_text=True)
            # import pdb; pdb.set_trace()
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create Tag', html)
            self.assertIn('Post 1', html)
     
 
  

    def test_add_new_tag(self): 
        """ Test that new Tag is added to database """
        with app.test_client() as client:
            resp = client.post(f'/tags/new', data={'tagName':'Yolo'}, follow_redirects=True )       

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Yolo', html)


    def test_show_all_tags(self):
        """ Test that all Tags in DB are displayed """
        with app.test_client() as client:
            resp = client.post(f'/tags/new', data={'tagName':'Yolo'}, follow_redirects=True )       

            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Tags</h2>', html)
            self.assertIn('Yolo', html)
            self.assertIn('Awesome', html)

    def test_show_tag_detail(self):
        """  Test that a tag's details page is displayed """
        with app.test_client() as client:
            resp = client.post(f'/tags/new', data={'tagName':'Yolo'}, follow_redirects=True )       

            resp = client.get(f'/tags/{self.tag_id}')
            html = resp.get_data(as_text=True)

            # import pdb; pdb.set_trace()

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Awesome</h2>', html)
            self.assertIn('Post 1', html)


    def test_show_tag_edit_form(self):
        """ Test that tag edit form is displayed """
        with app.test_client() as client:
            resp = client.get(f'/tags/{self.tag_id}/edit')
            html = resp.get_data(as_text=True)
            # import pdb; pdb.set_trace()
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Edit Tag</h2>', html)
            self.assertIn('Post 1', html)
            self.assertIn('checked', html)


    def test_save_edited_tag(self):
        """ Test that edited Tag is saved to database """
        with app.test_client() as client:
            resp = client.post(f'/tags/new', data={'tagName':'Yolo'}, follow_redirects=True )       
            html = resp.get_data(as_text=True)
            # import pdb; pdb.set_trace()

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Tags</h2>', html)
            self.assertIn('Yolo', html)
            self.assertIn('Awesome', html)      

    def test_delete_tag(self):
        """ Test that Tag is deleted from database """
        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag_id}/delete', follow_redirects=True )       
            html = resp.get_data(as_text=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Tags</h2>', html)
            self.assertNotIn('Awesome</li></a>', html)      
    
