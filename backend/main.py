from uuid import uuid4
from abc import ABC,abstractmethod
from flask import Flask, jsonify, request
from flask_cors import CORS

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
        self.parser.validate_title(title)

        card = Card(title, content)
        self.parser.parse_card(card)

        self.database.store_card(card)

        return card

    def delete_card(self, card_id: uuid4):
        self.database.remove_card(card_id)

    def update_card(self, card_id: uuid4, new_card: Card):
        new_card_title = new_card.get_title()
        self.parser.validate_title(new_card_title)

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
        CORS(app, resources={r"/*":{'origins':"*"}})

        @app.route('/cards', methods=["GET", "POST"])
        def cards():
            response_object = {'status': 'succes'}

            if request.method == 'POST':
                post_data = request.get_json()

                self.create_card(
                    post_data.get('title'),
                    post_data.get('content'),
                )

            
            all_cards = self.get_all_cards()
            response_object['cards'] = all_cards

            return jsonify(response_object)

        app.run(debug=True)
        print('error')

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
        links = re.findall(link_pat, content)

        links = self.strip_chars(links, 2, 2)

        return links

    def strip_chars(self, strip_list, begin, end=0):
        for index, item in enumerate(strip_list):
            if end == 0:
                strip_item = item[begin:]
            else:
                strip_item = item[begin: -end]
            
            strip_list[index] = strip_item

        return strip_list

    def _parse_question(self, content):
        q_pat = re.compile('Q\d*\{\{.*\}\}')

        questions = re.findall(q_pat, content)

        #TODO Make it so we can parse more than 9 questions
        questions = self.strip_chars(questions, 4,2)
        return questions

    def _parse_latex(self, content):
        latex_pat = re.compile('\$.*\$')
        latex = re.findall(latex_pat, content)

        latex = self.strip_chars(latex, 1, 1)
        return latex

    def _parse_tags(self, content):
        tag_pat = re.compile('#\w+')

        tags = re.findall(tag_pat, content)

        tags = self.strip_chars(tags, 1)

        return tags

class AlgorithmCalculator(RevCalcInteractor):
    def calculate_next_review():
        pass

class SQLAlchemyDatabase(DatabaseInteractor):
    def __init__(self):
        self.base = declarative_base()
        self.engine = create_engine('sqlite:////tmp/cards.db')
        self.session = scoped_session(sessionmaker(autocommit=False,
            autoflush=False,
            bind=self.engine))

    class DataCard(declarative_base()):
        __tablename__ = 'card'

        card_id     = Column(Integer, primary_key = True)
        title       = Column(String)
        content     = Column(String)

        links       = Column(String)
        questions   = Column(String)
        latex       = Column(String)
        tags        = Column(String)

    def update_database(self):
        self.session.commit()

    def get_all_cards(self):
        cards = self.session.query(self.DataCard).all()
        cards = self.serialize_cards(cards)

        return cards

    def serialize_cards(self, cards):
        serialized_cards = {}
        serialized_card = {}

        for card in cards:
            serialized_card['title']        = card.title
            serialized_card['content']      = card.content
            serialized_card['links']        = card.links
            serialized_card['questions']    = card.questions
            serialized_card['latex']        = card.latex
            serialized_card['tags']         = card.tags

            serialized_cards[card.card_id] = serialized_card

        return serialized_cards

    def get_card(self, card_id):
        card = self.session.query(self.DataCard).get(card_id)

        return card

    def store_card(self, card):
        parsed_card_content = card.get_parsed_content()

        parsed_card_content = self.jsonify_parsed_content(parsed_card_content)
    
        unwrapped_parsed_card = self.unwrap_parsed_card(card, parsed_card_content)

        self.session.add(unwrapped_parsed_card)

        #only adds the card temporarily till we commit
        self.session.commit()

    #Parse python dictionaries to a json format
    def jsonify_parsed_content(self, parsed_card_content):
        for item in parsed_card_content:
            parsed_card_content[item] = json.dumps(parsed_card_content[item])

        return parsed_card_content

    def unwrap_parsed_card(self,card, parsed_card_content):

        unwrapped_card = self.DataCard(
            title       = card.get_title(),
            content     = card.get_content(),
            links       = parsed_card_content['links'], 
            questions   = parsed_card_content['questions'], 
            latex       = parsed_card_content['latex'], 
            tags        = parsed_card_content['tags'], 
        )

        return unwrapped_card

    def update_card(self, card_id, new_card):
        pass

    def remove_card(self, card_id):
        self.session.query(self.DataCard).get(card_id).delete()
    
    def init_db(self):
        self.base.metadata.create_all(bind=self.engine)

    def reset_database(self):
        self.base.metadata.drop_all(self.engine)

if __name__=='__main__':

    card_parser     = ReCardParser()  
    card_rev_calc   = AlgorithmCalculator()
    card_database   = SQLAlchemyDatabase()
    
    card_database.init_db()
    interactor = WebInteractor(card_parser, card_rev_calc, card_database)

    interactor.init_router()