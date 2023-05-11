import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    is_superuser = sa.Column(sa.BOOLEAN, default=False, nullable=False)
    password_hash = sa.Column(sa.Text, nullable=False)


class Document(Base):
    __tablename__ = 'document'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.TEXT, unique=True, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    admin_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    is_verified = sa.Column(sa.BOOLEAN, default=False, nullable=False)
