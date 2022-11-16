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
engine = create_engine('sqlite:////tmp/test.db')
db_session = scoped_session(sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine))

Base.query = db_session.query_property()


class ParsedCard(Base):
    __tablename__= 'parsed_card'
    parsed_card_id = Column(Integer, primary_key=True)
    links = Column(String)
    questions = Column(String)
    latex = Column(String)
    tags = Column(String)

card = ParsedCard(links = 'heasu', questions =' qusnaeuh', latex='latehaus', tags = 'ahutnse')
card2 = ParsedCard(links = 'eouaeua', questions =' eau', latex='euaoe', tags = 'uae')
db_session.add(card)
db_session.add(card2)

db_session.flush()


print(card.parsed_card_id)
print(card2.parsed_card_id)