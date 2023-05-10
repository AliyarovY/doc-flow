import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True)
    username = sa.Column(sa.String, unique=True)
    is_superuser = sa.Column(sa.BOOLEAN, default=False)
    password_hash = sa.Column(sa.Text)


class Document(Base):
    __tablename__ = 'document'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    content = sa.Column(sa.TEXT)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    admin_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    is_verified = sa.Column(sa.BOOLEAN, default=False)
