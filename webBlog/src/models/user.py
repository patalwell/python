from flask import session
from src.common.database import Database
import uuid
from src.models.blog import Blog
from datetime import datetime


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls,email):
        data = Database.find_one("users", {"email":email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # User.Login_valid("jose@schoolofcode.com", "1234")
        # check to see if user email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            # check password
            return user.password == password
        return False

    @classmethod
    def register(cls,email,password):
        user = cls.get_by_email(email)
        if user is None:
            # create the user
            new_user = User(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # user exists
            return False

    # dealing with cookies for the user with session from flask
    @staticmethod
    def login(user_email):
        session['email']= user_email

    @staticmethod
    def logout():
        session['email'] = None


    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title =title,
                    desciption=description,
                    author_id = self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.utcnow()):
        # title, content, date=datetime.datetime.utcnow()
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)


    # passwords are not safe to send over a network unless it is encrypted
    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert("users",self.json())
