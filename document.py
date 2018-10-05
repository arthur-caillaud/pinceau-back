class Document:
    content = ''
    
    @staticmethod
    def add_content(content):
        Document.content += content

    @staticmethod
    def get_content():
        return Document.content
