"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

def connect_db(app):
  """Connect to database. """
  db.app = app
  db.init_app(app)

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  first_name = db.Column(db.String(20), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)
  image_url = db.Column(db.String(75), default='https://iupac.org/wp-content/uploads/2018/05/default-avatar.png')

  posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

  def __repr__(self):
    """Show info about User."""
    u = self
    return f"<User {u.first_name} {u.last_name} {u.image_url}>"

  @property
  def get_full_name(self):
    """ Display full name """
    return f"{self.first_name} {self.last_name}" 


class Post(db.Model):
  __tablename__ = "posts"
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  title = db.Column(db.String(20), nullable = False)
  content = db.Column(db.String(200),nullable = False)
  createdAt = db.Column(db.DateTime, nullable = False, default=datetime.datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable = False)
  # tags = db.relationship('Tag', secondary="posts_tags", backref="posts")

  def __repr__(self):
    """Show info about Post."""
    u = self
    return f"<Post {u.title} {u.content}>"

  
  @property
  def simple_post_time(self):
    """Post Friendly Formatted Date"""
    return self.createdAt.strftime("%a %b %d  %Y, %I:%M %p")

  
class Tag(db.Model):
  __tablename__ = 'tags'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  name = db.Column(db.String(15), nullable = False, unique = True)

  posts = db.relationship('Post', secondary="posts_tags", backref="tags")

  def __repr__(self):
    """Show info about Post."""
    u = self
    return f"<Tag {u.name}>"

class PostTag(db.Model):
  __tablename__ = 'posts_tags'
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)
 


# UniqueConstraint("id", "candidate_id")
# tags = db.Table('tags',
#   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key = True),
#   db.Column('post_id', db.Integer, db.ForeignKey('post_id'), primary_key = True)
