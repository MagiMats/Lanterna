from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:////tmp/cards.db')
db_session = scoped_session(sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine))

Base.query = db_session.query_property()


class DataCard(Base):
        __tablename__ = 'card'

        card_id     = Column(Integer, primary_key = True)
        title       = Column(String)
        content     = Column(String)

        links       = Column(String)
        questions   = Column(String)
        latex       = Column(String)
        tags        = Column(String)

Base.metadata.create_all(bind=engine)

card = DataCard(title = 'bing', content='chilling',links = 'heasu', questions =' qusnaeuh', latex='latehaus', tags = 'ahutnse')
db_session.add(card)

db_session.commit()


print(card.card_id)
