from flask import jsonify

class Response:

    def __init__ ():
        self.message = "empty message"
        self.cards = []
        self.hint = ""
        self.intent = ""
        self.entities = []
        pass
    
    def generate ():
        return jsonify (intent = intent, entities = entities, message = message, cards = cards, hint = hint)
