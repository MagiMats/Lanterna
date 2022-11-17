import unittest
from main import ReCardParser, Card, SQLAlchemyDatabase

def init_basic_card(self):
    self.parser = ReCardParser()

    self.title = 'template_card'
    self.content = ''' 
    [[Hello_World-123]]

    [[World-Hello_321]]

    Q1{{Hello123@\-/<>,.&[{}()]=*+#[[Hello_jezus]]}}

    Q2{{   What is the size of pain?}}
    $1 + 1 = 2$


    how are u doing today mister swap bro
    #biology
    '''
    self.card = Card(self.title, self.content)
    self.card.set_parsed_content(self.parser.parse_card(self.card))

class ReCardParserTester(unittest.TestCase):
    def setUp(self):
        init_basic_card(self)

    def test_letter_title(self):
        title = 'helloworld'
        self.assertEqual(self.parser.validate_title(title), True)

    def test_capital_title(self):
        title = 'HELLOWORLD'
        self.assertEqual(self.parser.validate_title(title), True)
    
    def test_number_title(self):
        title = '123456'
        self.assertEqual(self.parser.validate_title(title), True)

    def test_dash_title(self):
        title = 'hello-world'
        self.assertEqual(self.parser.validate_title(title), True)

    def test_total_title(self):
        title = 'Hello_World-123'
        self.assertEqual(self.parser.validate_title(title), True)

    def test_space_title(self):
        title = 'hello world'
        try:
            self.parser.validate_title(title)

            self.assertEqual(True, False)
        except ValueError:
            self.assertEqual(True, True)

    def test_links(self):
        card = self.parser.parse_card(self.card)
        self.assertEqual(card['links'][0], 'Hello_World-123')
        self.assertEqual(card['links'][1], 'World-Hello_321')
        self.assertEqual(card['links'][2], 'Hello_jezus')

    def test_questions(self):
        card = self.parser.parse_card(self.card)
        self.assertEqual(card['questions'][0], 'Q1{{Hello123@\-/<>,.&[{}()]=*+#[[Hello_jezus]]}}')
        self.assertEqual(card['questions'][1], 'Q2{{   What is the size of pain?}}')

    def test_tags(self):
        card = self.parser.parse_card(self.card)
        self.assertEqual(card['tags'][0], '#biology')

    def test_latex(self):
        card = self.parser.parse_card(self.card)
        self.assertEqual(card['latex'][0], '$1 + 1 = 2$')

class SQLAlchemyDatabaseTester(unittest.TestCase):
    def setUp(self):
        init_basic_card(self)
        self.database = SQLAlchemyDatabase()
        self.database.init_db()

    def test_store_card(self):
        self.database.store_card(self.card)

    def test_return_all_cards(self):
        self.database.get_all_cards()

    def test_single_card(self):
        self.database.get_card(1)

    

if __name__=='__main__':
    unittest.main()