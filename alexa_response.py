class AlexaResponse:
    def __init__(self, output_text="", card_title="", card_content=""):
        self.output_text = output_text
        self.card_title = card_title
        self.card_content = card_content
        self.end_session = True
    
    def set_output_text(self, output_text):
        self.output_text = output_text
        return self
    
    def set_card_title(self, card_title):
        self.card_title = card_title
        return self
    
    def set_card_content(self, card_content):
        self.card_content = card_content
        return self
    
    def set_end_session(self, end_session):
        self.end_session = end_session
        return self

    def response(self):
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": "<speak>" + self.output_text + "</speak>",
                },
            "card": {
                "type": "Simple",
                "title": self.card_title,
                "content": self.card_content,
            },
            "shouldEndSession": self.end_session
            }
        }