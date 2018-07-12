import json
import datetime
import weather_information

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
        print("Error handling request: " + str(e))


def launch_request_response():
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
            "type": "PlainText",
            "text": "Plain text string to speak",
            },
            "shouldEndSession": False
        }
    }

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


    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
            "type": "PlainText",
            "text": text,
            },
            "shouldEndSession": True
        }
    }
