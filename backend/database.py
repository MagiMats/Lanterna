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
import json

Base = declarative_base()
engine = create_engine('sqlite:////tmp/cards.db')
session = scoped_session(sessionmaker(bind=engine))

Base.query = session.query_property()

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

def get_all_cards():
    data_cards = session.query(DataCard).all()

    cards = serialize_cards(data_cards)
    return cards

def serialize_cards(data_cards):
    serialized_cards = {}

    for card in data_cards:
        serialized_card = {}
        serialized_card['card_id']      = card.card_id
        serialized_card['title']        = card.title
        serialized_card['content']      = card.content
        serialized_card['links']        = card.links
        serialized_card['questions']    = card.questions
        serialized_card['latex']        = card.latex
        serialized_card['tags']         = card.tags

        serialized_cards[card.card_id] = serialized_card

    return serialized_cards

def get_card(card_id):
    card = session.query(DataCard).get(card_id)

    return card

def store_card( card):
    parsed_card_content = card.get_parsed_content()

    parsed_card_content = jsonify_parsed_content(parsed_card_content)

    unwrapped_parsed_card = unwrap_parsed_card(card, parsed_card_content)

    session.add(unwrapped_parsed_card)
    #only adds the card temporarily till we commit
    session.commit()

#Parse python dictionaries to a json format
def jsonify_parsed_content(parsed_card_content):
    for item in parsed_card_content:
        parsed_card_content[item] = json.dumps(parsed_card_content[item])

    return parsed_card_content

def unwrap_parsed_card(card, parsed_card_content):

    unwrapped_card = DataCard(
        title       = card.get_title(),
        content     = card.get_content(),
        links       = parsed_card_content['links'], 
        questions   = parsed_card_content['questions'], 
        latex       = parsed_card_content['latex'], 
        tags        = parsed_card_content['tags'], 
    )

    return unwrapped_card

def update_card( card_id, new_card):
    pass

def remove_card(card_id):
    session.query(DataCard).filter(DataCard.card_id == card_id).delete()
    session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

def reset_database():
    Base.metadata.drop_all(engine)
