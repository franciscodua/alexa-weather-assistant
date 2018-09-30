from datetime import datetime
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
            day = datetime.strptime(parameters["day"]["value"], "%Y-%m-%d").date()
        else:
            # this is using the timestamp that comes from the request itself.
            day = datetime.strptime(request["timestamp"] ,"%Y-%m-%dT%H:%M:%SZ").date()
    
        try:
            weather_assistant = weather_information.WeatherAssistant()
            rains, precipitationProb = weather_assistant.rains_on_day(day)
            if rains:
                text = "No. There's a " + str(precipitationProb) + \
                    "% probablity of raining. "
                clear_day = weather_assistant.get_next_clear_day(day)
                if clear_day is not None:
                    # card_content needs to be a different from text because of SSML
                    card_content = text + "Try again on " + str(clear_day)
                    text = text +\
                    "Try again on <say-as interpret-as=\"date\">" +\
                    clear_day.strftime("????%m%d") +\
                    "</say-as>."
                else:
                    text = text + "Try again another time."
                    card_content = text
            else:
                text = "Yeah. It probably won't rain. There is " + \
                    str(precipitationProb) + "% probability of raining."
                card_content = text
        except weather_information.DayNotFoundException as e:
            text = str(e)

        return AlexaResponse().\
            set_output_text(text).\
            set_card_title("Can I hang my clothes").\
            set_card_content(card_content).\
            set_end_session(True).\
            response()

class AnswerError(ErrorHandler):
    def handle(self, request, exception):
        error_message = str(exception)
        print("Error handler: Error handling request: " + error_message)
        return AlexaResponse().\
            set_output_text(error_message).\
            set_card_title("Weather assistant error").\
            set_card_content(error_message).\
            set_end_session(True).\
            response()
