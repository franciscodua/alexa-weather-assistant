import json
import datetime
import weather_information
from alexa_response import AlexaResponse

def handle_request(event, context):
    try:
        request = event["request"]
        print("request type: " + request["type"])
        if request["type"] == "LaunchRequest":
            return launch_request_response()
        elif request["type"] == "IntentRequest":
            if request["intent"]["name"] == "CanHangClothes":
                return can_hang_clothes_response(request["intent"]["slots"])
        else:
            print("request[type] not expected: " + request["type"])
    except Exception as e:
        error = str(e)
        print("Error handling request: " + error)
        return error_response(error)


def launch_request_response():
    return AlexaResponse().\
        set_output_text("You can ask if you can hang your clothes for a given day").\
        set_card_title("Weather assistant help").\
        set_card_content("You can ask if you can hang your clothes for a given day").\
        set_end_session(False).\
        response()

def error_response(error_message):
    return AlexaResponse().\
        set_output_text(error_message).\
        set_card_title("Weather assistant error").\
        set_card_content(error_message).\
        set_end_session(True)

def can_hang_clothes_response(parameters):
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
