import datetime
from alexa import RequestHandler, ErrorHandler
from alexa_response import AlexaResponse
import weather_information

class LaunchRequest(RequestHandler):
    def can_handle(self, request):
        return request["type"] == "LaunchRequest"
    
    def handle(self, request):
        help_text = "You can ask if you can hang your clothes for a given day"
        return AlexaResponse().\
            set_output_text(help_text).\
            set_card_title("Weather assistant help").\
            set_card_content(help_text).\
            set_end_session(False).\
            response()

class CanHangClothes(RequestHandler):
    def can_handle(self, request):
        return request["type"] == "IntentRequest" and \
            request["intent"]["name"] == "CanHangClothes"
    
    def handle(self, request):
        parameters = request["intent"]["slots"]
        if "value" in parameters["day"]:
            day = datetime.datetime.strptime(parameters["day"]["value"], "%Y-%m-%d").date()
        else:
            day = datetime.date.today()
    
        try:
            rains, precipitationProb = weather_information.rains_on_day(day)
            if rains:
                text = ''.join(["No. There's a ", str(precipitationProb), \
                    "% probablity of raining. Try again another time."])
            else:
                text = "Yeah. It probably won't rain."
        except weather_information.DayNotFoundException as e:
            text = str(e)

        return AlexaResponse().\
            set_output_text(text).\
            set_card_title("Can I hang my clothes").\
            set_card_content(text).\
            set_end_session(True).\
            response()

class AnswerError(ErrorHandler):
    def handle(self, request, exception):
        error_message = str(exception)
        print("Error handling request: " + error_message)
        return AlexaResponse().\
            set_output_text(error_message).\
            set_card_title("Weather assistant error").\
            set_card_content(error_message).\
            set_end_session(True)
