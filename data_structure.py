
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
