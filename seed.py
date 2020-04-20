"""Seed file to make sample data for users db."""
from models import db, User, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

#Add users
jaime = User(first_name='Jaime', last_name='Johnson')
david = User(first_name='David', last_name='Yarro')
nancy = User(first_name='Nancy', last_name='Jenkins')
mary = User(first_name='Mary', last_name='Jones')

#Add posts
post1 = Post(title='Post1', content='This is the content for Post1', user_id = 1)
post2 = Post(title='Post2', content='This is the content for Post2', user_id = 1)
post3 = Post(title='Post3', content='This is the content for Post3', user_id = 1)
post4 = Post(title='Post4', content='This is the content for Post4', user_id = 1)


#Add tags
tag1 = Tag(name = 'Fantastic!')
tag2 = Tag(name = 'Fun!')
tag3 = Tag(name = 'Boomer')
tag4 = Tag(name = 'WTH')

#Populate posts_tags table
post_tag_1 = PostTag(post_id = 1, tag_id = 1)
post_tag_2 = PostTag(post_id = 1, tag_id = 2)
post_tag_3 = PostTag(post_id = 1, tag_id = 3)
post_tag_4 = PostTag(post_id = 1, tag_id = 4)

post_tag_5 = PostTag(post_id = 2, tag_id = 1)
post_tag_6 = PostTag(post_id = 2, tag_id = 2)
post_tag_7 = PostTag(post_id = 2, tag_id = 3)
post_tag_8 = PostTag(post_id = 2, tag_id = 4)

post_tag_9 = PostTag(post_id = 3, tag_id = 1)
post_tag_10 = PostTag(post_id = 3, tag_id = 2)
post_tag_11 = PostTag(post_id = 3, tag_id = 3)
post_tag_12 = PostTag(post_id = 3, tag_id = 4)


# Add new objects to session, so they'll persist
db.session.add(jaime)
db.session.add(david)
db.session.add(nancy)
db.session.add(mary)
# Commit -- otherwise, this ever gets saved to DB!
db.session.commit()

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.commit()

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)
db.session.commit()


db.session.add(post_tag_1)
db.session.add(post_tag_2)
db.session.add(post_tag_3)
db.session.add(post_tag_4)

db.session.add(post_tag_5)
db.session.add(post_tag_6)
db.session.add(post_tag_7)
db.session.add(post_tag_8)

db.session.add(post_tag_9)
db.session.add(post_tag_10)
db.session.add(post_tag_11)
db.session.add(post_tag_12)

db.session.commit()