
# Software structure imports
from abc import ABC,abstractmethod

# Flask Imports
from flask import Flask, jsonify, request
from flask_cors import CORS

#
import pymongo

# General Imports
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





class RevCalcInteractor(ABC):
    @abstractmethod
    def calculate_next_review():
        pass





class AlgorithmCalculator(RevCalcInteractor):
    def calculate_next_review():
        pass





class DatabaseInteractor(ABC):
    @abstractmethod
    def get_all_cards(self):
        return NotImplementedError

    @abstractmethod
    def get_card(self, card_id):
        return NotImplementedError

    @abstractmethod
    def store_card(self, card: Card):
        return NotImplementedError

    @abstractmethod
    def update_card(self, card_id, new_card: Card):
        return NotImplementedError

    @abstractmethod
    def remove_card(self, card_id):
        return NotImplementedError





class MongoDBDatabase(DatabaseInteractor):
    def __init__(self):
        self.dbname = self.get_database()

        self.collection_name = self.dbname["mats_cards"]

    def get_database(self):
        client = pymongo.MongoClient("mongodb+srv://Mats:<password>@cluster0.vzinlcn.mongodb.net/?retryWrites=true&w=majority")
        
        return client['card_list']

    def get_all_cards(self):
        pass

    def get_card(self, card_id):
        pass
    
    def store_card(self, card):
        card_dict = self.serialize_card_to_dict(card)

        self.collection_name.insert_one(card_dict)

    def update_card(self, card_id, new_card):
        pass

    def remove_card(self, card_id):
        pass

    def serialize_card_to_dict(self, card):
        card_dict = {}
        card_parsed_content = card.get_parsed_content()

        card_dict['title']       = card.get_title()
        card_dict['content']     = card.get_content()
        card_dict['links']       = card_parsed_content['links']
        card_dict['questions']   = card_parsed_content['questions']
        card_dict['latex']       = card_parsed_content['latex']
        card_dict['tags']        = card_parsed_content['tags']

        return card_dict





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

        return card

    def create_and_store_card(self, title, content):
        card = self.create_card(title, content)

        self.database.store_card(card)

        return card

    def delete_card(self, card_id):
        self.database.remove_card(card_id)

    def update_card(self, card_id, new_card):
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
        CORS(app)

        @app.route('/cards', methods=["GET", "POST"])
        def cards():
            response_object = {'status': 'succes'}

            response_object = post_follow_up(response_object)

            return jsonify(response_object)

        @app.route('/cards/<card_id>/delete', methods=["DELETE"])
        def delete_card(card_id):
            response_object = {'status': 'succes'}

            if request.method == "DELETE":
                response_object = {'message': 'Card got deleted =['}
                self.delete_card(card_id)

            return jsonify(response_object)

        @app.route('/cards/<card_id>/update', methods=["PUT"])
        def update_card(card_id):
            response_object = {'status': 'succes'}
            if request.method == "PUT":
                post_data = request.get_json()

                card = self.create_card(post_data.get('title'), post_data.get('content'))

                self.update_card(card_id, card)

                response_object['message'] =  'Game Updated!'

            return jsonify(response_object)

        def post_follow_up(response_object):
            if request.method == 'POST':
                post_data = request.get_json()

                self.create_and_store_card(
                    post_data.get('title'),
                    post_data.get('content'),
                )

            
            all_cards = self.get_all_cards()
            response_object['cards'] = all_cards

            return response_object

        app.run(debug=True)




if __name__=='__main__':

    card_parser     = ReCardParser()  
    card_rev_calc   = AlgorithmCalculator()
    card_database   = MongoDBDatabase()
    

    interactor = WebInteractor(card_parser, card_rev_calc, card_database)

    interactor.init_router()