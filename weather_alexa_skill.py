from alexa_response import AlexaResponse
from alexa import Alexa
import weather_assistant_handlers as handlers

def handle_request(event, context):
    request = event["request"]
    alexa = Alexa().\
        add_handler(handlers.LaunchRequest()).\
        add_handler(handlers.CanHangClothes()).\
        add_error_handler(handlers.AnswerError())
    return alexa.handle_request(request)
