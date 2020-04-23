"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash 
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

db.create_all()

# ******************************************************
# *  User Routes
# ******************************************************
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def root():
  """Redirect to List Uses page."""
 
  posts = Post.query.order_by(Post.createdAt.desc()).limit(5).all()
  tags = Tag.query.all()
  return render_template('index.html', posts=posts, tags=tags)
  
@app.route('/users')
def list_users():
  """List all users."""
  users = User.query.order_by(User.last_name, User.first_name).all()
  return render_template("users/list.html", users=users)

@app.route('/users/new')
def show_new_user_form():
  """Display new user form to add user."""
  return render_template("users/add_user.html")

@app.route('/users/new', methods=["POST"])
def add_new_user():
  """Add new user to the users database"""
  first_name = request.form['firstName'].strip().capitalize()
  last_name = request.form['lastName'].strip().capitalize()
  profile_image = request.form['profileImage'].strip().capitalize()
  # profile_image = if profile_image else None
  # if no profile pict provided set to none so that DB default can be used
  if profile_image:
    profile_image = profile_image
  else:
    profile_image = None

  user = User(first_name = first_name, last_name = last_name, image_url = profile_image)
  db.session.add(user)
  db.session.commit()

  flash(f"User: '{user.get_full_name}' successfully added.", 'success')

  return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
  """ Display user details page """
  user = User.query.get_or_404(user_id)
  user_posts = Post.query.filter(Post.user_id == user.id).all()
  return render_template("users/user_detail.html", user = user, user_posts=user_posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_detail(user_id):
  """ Display populated edit_user form """
  user = User.query.get_or_404(user_id)
  return render_template("users/edit_user.html", user = user)

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
  """Delete a user"""
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()

  flash(f"User: '{user.get_full_name}' successfully deleted.", 'success')

  return redirect('/users')

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
  """ Update DB to include user edits"""
  user = User.query.get_or_404(user_id)
  user.first_name = request.form['firstName'].strip().capitalize()
  user.last_name = request.form['lastName'].strip().capitalize()
  user.profile_image = request.form['profileImage'].strip().capitalize()

  # if no profile pict provided set to none so that DB default can be used
  if user.profile_image:
    user.profile_image = user.profile_image
  else:
    user.profile_image = None

  db.session.add(user)
  db.session.commit()

  flash(f"User: '{user.get_full_name}' successfully edited.", 'success')

  return redirect("/users")

# ******************************************************
# *  Post Routes
# ******************************************************

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
  """Show add new post form"""
  user = User.query.get_or_404(user_id)
  tags = Tag.query.all()
  return render_template("posts/add_new_post.html", user=user, tags = tags) 

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
  """Ad newly created Post to posts DB """
  user = User.query.get_or_404(user_id)
  post_title = request.form['postTitle'].strip().capitalize()
  post_content = request.form['postContent'].strip().capitalize()

  # Use comprehension to Create a list of tag_id's that were checked on UI's form
  tag_ids = [int(num) for num in request.form.getlist("tags")]

  # Retrieve all tag records with matching tag_ids so we can update them
  tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
  new_post = Post(title = post_title, content = post_content, user= user, tags=tags)
  db.session.add(new_post)
  db.session.commit()
  flash(f"'{post_title}' post successfully added.", 'success')
  return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
  """Display a single post"""
  post = Post.query.get_or_404(post_id)
  user = User.query.get_or_404(post.user_id)
  return render_template('posts/show_post.html', user=user, post=post)

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
  """ Delete a post """
  post = Post.query.get_or_404(post_id)
  user = User.query.get_or_404(post.user_id)
  db.session.delete(post)
  db.session.commit()
  flash(f" '{post.title}' post successfully deleted.", 'success')
  return redirect('/users')

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
  post = Post.query.get_or_404(post_id)
  tags = Tag.query.all()
  return render_template('posts/edit_post.html', post=post, tags = tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def save_post_edits(post_id):
  post = Post.query.get_or_404(post_id)
  post.title = request.form['postTitle'].strip().capitalize()
  post.content = request.form['postContent'].strip().capitalize()
  
  # Create a list of tag_id's that were checked on UI's form
  tag_ids = [int(num) for num in request.form.getlist("tags")]

  post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
  
  db.session.add(post)
  db.session.commit()
 
  flash(f"'{post.title}' post successfully edited.", 'success')

  return redirect(f"/users/{post.user_id}" )

  # ******************************************************
  # *  Tag Routes
  # ******************************************************

@app.route('/tags/new')
def show_add_new_tag_form():
  """Display form to create new tag."""
  posts = Post.query.all()
  return render_template("tags/create_tag.html", posts = posts)

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
  """Add new tag to DB and redirect to list of tags"""
  name = request.form['tagName'].strip().capitalize()
  post_ids = [int(num) for num in request.form.getlist("posts")]
  posts = Post.query.filter(Post.id.in_(post_ids)).all()

  # ??? Don't unsderstand how it is possible to pass in an extra param(i.e., posts)
  # into Tag Class and how passing that parameter SPECIFICALLY causes the posts.tags table
  # to be populated. 
  new_tag = Tag(name = name, posts = posts)

  db.session.add(new_tag)
  db.session.commit()
  tags = Tag.query.all()

  flash(f"'{new_tag.name}' tag was successfully created.", 'success')
  return redirect('/tags')

@app.route('/tags')
def show_all_tags():
  "Display all tags"
  tags = Tag.query.all()
  return render_template('tags/list_tags.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
  """ Display tag name and all post tagged with this tag """
  tag = Tag.query.get_or_404(tag_id)
  return render_template('tags/show_tag.html', tag = tag)

@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_form(tag_id):
  tag = Tag.query.get_or_404(tag_id)
  posts = Post.query.all()
  # import pdb; pdb.set_trace()
  return render_template('tags/edit_tag.html', tag=tag, posts = posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def save_edited_tag(tag_id):
  """ Saves edited tag to the database """
  tag = Tag.query.get_or_404(tag_id)
  tag.name = request.form['tagName'].strip().capitalize()

  post_ids = [int(num) for num in request.form.getlist("posts")]
  import pdb; pdb.set_trace()
  tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

  db.session.add(tag)
  db.session.commit()
  flash(f"'{tag.name}' tag was successfully edited.", 'success')
  return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
  """ Deletes a tag from DB """
  tag = Tag.query.get_or_404(tag_id)
  db.session.delete(tag)
  db.session.commit()
  flash(f"'{tag.name}' tag was successfully deleted.", 'success')
  return redirect('/tags')