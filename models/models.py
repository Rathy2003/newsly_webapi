import datetime
from flask import request
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extentions.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile = db.Column(db.String(255), nullable=True)
    fcm_token = db.Column(db.String(255), nullable=True)
    createdAt: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updatedAt: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        base_url = request.host_url.rstrip('/')
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_image_path": f"{base_url}/files/profiles/{self.profile}" if self.profile else None,
            "createdAt": self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": self.updatedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }

class Category(db.Model):
    __tablename__ = 'categorys'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(200),unique=True,nullable=False,)
    news: Mapped[list["News"]] = relationship("News",back_populates="category", cascade='all, delete-orphan')
    createdAt: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updatedAt: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "createdAt": self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": self.updatedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
class News(db.Model):
    __tablename__ = 'news'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255),unique=True,nullable=False)
    description: Mapped[str] = mapped_column(db.String(500),unique=False,nullable=False)
    thumbnail: Mapped[str] = mapped_column(db.String(255),unique=True,nullable=False)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    category_id: Mapped[int] = mapped_column(db.Integer,ForeignKey('categorys.id',ondelete="SET NULL"),nullable=True)
    category = relationship("Category",back_populates="news")
    createdAt: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updatedAt: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        base_url = request.host_url.rstrip('/')
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "full_image_path": f"{base_url}/files/{self.thumbnail}" if self.thumbnail else None,
            "content": self.content,
            "category_name": self.category.name if self.category else None,
            "category_id": self.category_id,
            "posted_at": self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
        }