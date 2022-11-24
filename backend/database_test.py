import pymongo


class MongoDBDatabase(DatabaseInteractor):
    def __init__(self):
        self.dbname = self.get_database()

        self.collection_name = self.dbname["mats_cards"]

    def get_database(self):
        client = pymongo.MongoClient("mongodb+srv://Mats:107MaTesla2003@cluster0.vzinlcn.mongodb.net/?retryWrites=true&w=majority")
        
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


