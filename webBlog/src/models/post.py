# Creating our model for POST method
# class for BlogPost Objects (e.g. Name, Title, Content, Author, Id)
import uuid
from src.common.database import Database
import datetime


class Post(object):

    def __init__(self, blog_id, title, content, author, date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.date = date
        # this creates a random id for creation of a post
        self._id = uuid.uuid4().hex if id is None else id

# function to insert data into MongoDB
    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

# Function to return a JSON Object for MongoDB
    def json(self):
        return {
            'id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'date': self.date,
        }

    @classmethod
    # Post.from_mongo('post_id)
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)
        # the ** post data is a hack for iterations from our object below
        # return cls(blog_id=post_data['blog_id'],
        #            title=post_data['title'],
        #            content=post_data['content'],
        #            author=post_data['author'],
        #            _id=post_data['_id'],
        #            date=post_data['date']
        #            )

    # Post.from_blog('blog_id'): takes a collection of posts and returns a single post, vice the Mongo DB object
    @staticmethod
    def from_blog(blog_id):
        return [post for post in Database.find(collection='posts', query={'blog_id': blog_id})]
