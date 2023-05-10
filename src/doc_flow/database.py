from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from doc_flow.tables import Base
from doc_flow.settings import settings


engine = create_engine(
    settings.database_url,
    connect_args={'check_same_thread': False},
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


if __name__ == '__main__':
    Base.metadata.create_all(engine)

