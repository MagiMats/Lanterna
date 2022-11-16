from uuid import uuid4
from abc import ABC,abstractmethod
from flask import Flask, jsonify

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

import re, json


class Card():
    def __init__(self, title, content):
        self.set_title(title)
        self.set_content(content)
        self.set_id()

    def set_title(self,title):
        self._title = title

    def get_title(self):
        return self._title

    def set_content(self, content):
        self._content = content

    def get_content(self):
        return self._content

    def get_parsed_content(self):
        return self._parsed_content

    def set_parsed_content(self, parsed_content):
        self._parsed_content = parsed_content

    def set_id(self):
        self._id = uuid4().hex

    def get_id(self):
        return self._id

class CardParserInteractor(ABC):
    @abstractmethod
    def validate_title():
        pass

    def parse_card(self, card):
        content = card.get_content()

        links = self._parse_links(content)
        questions = self._parse_question(content)
        latex = self._parse_latex(content)
        tags = self._parse_tags(content)

        parsed_card = {
            'links': links,
            'questions': questions,
            'latex': latex,
            'tags': tags,
        }

        card.set_parsed_content(parsed_card)

        return parsed_card

    @abstractmethod
    def _parse_links():
        pass

    @abstractmethod
    def _parse_question():
        pass

    @abstractmethod
    def _parse_latex():
        pass


    @abstractmethod
    def _parse_tags():
        pass

class RevCalcInteractor(ABC):
    @abstractmethod
    def calculate_next_review():
        pass

class DatabaseInteractor(ABC):
    @abstractmethod
    def get_all_cards(self):
        return NotImplementedError

    @abstractmethod
    def get_card(self, card_id: uuid4):
        return NotImplementedError

    @abstractmethod
    def store_card(self, card: Card):
        return NotImplementedError

    @abstractmethod
    def update_card(self, card_id:uuid4, new_card: Card):
        return NotImplementedError

    @abstractmethod
    def remove_card(self, card_id: uuid4):
        return NotImplementedError

class CardInteractor():
    def __init__(
        self, 
        card_parser: CardParserInteractor,
        card_rev_calc: RevCalcInteractor,
        card_database: DatabaseInteractor
    ):
        self.parser = card_parser
        self.database = card_database

    def create_card(self, title, content):
        self.card_parser.validate_title()
        
        card = Card(title, content)

        self.card_storage.store_card(card)

        return card

    def delete_card(self, card_id: uuid4):
        self.database.remove_card(card_id)

    def update_card(self, card_id: uuid4, new_card: Card):
        new_card_title = new_card.get_title()
        self.card_parser.validate_title(new_card_title)

        self.database.update_card(card_id, new_card)

    def create_web_interface(self, web_interface):
        self.web_interface = web_interface

    def get_all_cards(self):
        all_cards = self.database.get_all_cards()
        # TODO make a specifier so we can choose 
        # TODO which contents we get for a specific purpose

        return all_cards

    def get_next_card():
        cards = self.database.get_all_cards()
        # TODO We need to pass the id and 
        # TODO the properties for calculating but nothing else

class WebInteractor(CardInteractor):
    def init_router(self):
        self.app = Flask(__name__)
        app = self.app

        @app.route('/')
        def home():
            response_object = {'status': 'succes'}

            all_cards = self.get_all_cards()
            response_object['CARDS'] = all_cards

            return jsonify(response_object)

        app.run(debug=True)

class ReCardParser(CardParserInteractor):
    def validate_title(self, title):
        title_pat = re.compile('[a-zA-Z1-9\-\_]*')
        
        if re.match(title_pat, title)[0] == title:
            return True
        else:
            raise ValueError 

    def _parse_links(self, content):
        # Matches a title surrounded by 2 hooks
        link_pat = re.compile('\[\[[a-zA-Z1-9\-\_]*\]\]')
        return re.findall(link_pat, content)

    def _parse_question(self, content):
        q_pat = re.compile('Q\d*\{\{.*\}\}')

        return re.findall(q_pat, content)

    def _parse_latex(self, content):
        latex_pat = re.compile('\$.*\$')

        return re.findall(latex_pat, content)

    def _parse_tags(self, content):
        tag_pat = re.compile('#\w+')

        return re.findall(tag_pat, content)

class AlgorithmCalculator(RevCalcInteractor):
    def calculate_next_review():
        pass

class SQLAlchemyDatabase(DatabaseInteractor):
    def __init__(self):
        self.base = declarative_base()
        self.engine = create_engine('sqlite:////tmp/test.db')
        self.session = scoped_session(sessionmaker(autocommit=False,
            autoflush=False,
            bind=self.engine))

        self.base.query = self.session.query_property()

    class DataCard(declarative_base()):
        __tablename__ = 'card'

        card_id = Column(Integer, primary_key = True)
        parsed_card_id = Column(Integer, ForeignKey("parsed_card.parsed_card_id"))
        title = Column(String)
        content = Column(String)

    class ParsedCard(declarative_base()):
        __tablename__= 'parsed_card'
        parsed_card_id = Column(Integer, primary_key=True)
        links = Column(String)
        questions = Column(String)
        latex = Column(String)
        tags = Column(String)


    def get_all_cards(self):
        print(self.base.query.all())

    def get_card(self, card_id):
        pass

    def store_card(self, card):
        parsed_card_content = card.get_parsed_content()

        for item in parsed_card_content:

            parsed_card_content[item] = json.dumps(parsed_card_content[item])
    
        unwrapped_card = self.unwrap_card(parsed_card_content)

        self.session.add(unwrapped_card)
        self.session.flush()

    def unwrap_card(self, parsed_card):
        unwrapped_card = self.ParsedCard(
            links = parsed_card['links'], 
            questions = parsed_card['questions'], 
            latex = parsed_card['latex'], 
            tags = parsed_card['tags'], 
        )

        return unwrapped_card



    def update_card(self, card_id, new_card):
        pass

    def remove_card(self, card_id):
        pass
    
    def init_db(self):
        self.base.metadata.create_all(bind=self.engine)

if __name__=='__main__':


    card_parser = ReCardParser()  
    card_rev_calc = AlgorithmCalculator()
    card_database = SQLAlchemyDatabase()
    card_database.init_db()
    interactor = WebInteractor(card_parser, card_rev_calc, card_database)

    interactor.init_router()