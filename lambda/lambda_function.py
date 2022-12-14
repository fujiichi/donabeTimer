# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import datetime
import pytz
import typing

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.skill_builder import SkillBuilder, CustomSkillBuilder
from ask_sdk_model.services.reminder_management import (
    Trigger, TriggerType, AlertInfo ,SpokenInfo, SpokenText, PushNotification, PushNotificationStatus, ReminderRequest, Recurrence, RecurrenceFreq)


from ask_sdk_model.ui import SimpleCard, AskForPermissionsConsentCard
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from ask_sdk_model.services.service_exception import ServiceException
from ask_sdk_model.interfaces.connections import SendRequestDirective

if typing.TYPE_CHECKING:
    from ask_sdk_core.handler_input import HandlerInput
    from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PERMISSIONS = ["alexa::alerts:reminders:skill:readwrite"]
TIME_ZONE_ID= 'America/Los_Angeles'

WELCOME_MESSAGE = "Welcome to the medicine reminder sample skill. You can say set a reminder to set reminder in next 5 minutes. What do you want to ask?"
WHAT_DO_YOU_WANT = "What do you want to ask?"
NOTIFY_MISSING_PERMISSIONS = "Please enable reminder permissions in the Amazon Alexa app to proceed further."
ERROR = "Uh Oh. Looks like something went wrong."
GOOD_BYE = "Goodbye !!"
HELP_MESSAGE = "To use this skill say set a reminder which will set a reminder for next 5 minutes."

import os 
from ask_sdk_s3.adapter import S3Adapter 
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

#from ask_sdk_core.skill_builder import CustomSkillBuilder
#from ask_sdk_core.dispatch_components import AbstractRequestHandler
#from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
#from ask_sdk_model.interfaces.connections import SendRequestDirective
#from ask_sdk_model.ui import AskForPermissionsConsentCard
#from ask_sdk_model.ui import SimpleCard, AskForPermissionsConsentCard
from ask_sdk_model.services.directive import (
    SendDirectiveRequest, Header, SpeakDirective)

from ask_sdk_model import Response

#NOTIFY_MISSING_PERMISSIONS = ("???????????????????????????????????????????????????")
#PERMISSIONS = ["alexa::alerts:timers:skill:readwrite"]

#logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "????????????????????????????????????"
        
        #?????????????????????????????????
#        user_permissions = handler_input.request_envelope.context.system.user.permissions
#        if not (user_permissions and user_permissions.consent_token):
#            logger.error('???????????????????????????')
#            #handler_input.response_builder.speak(NOTIFY_MISSING_PERMISSIONS)
#            logger.error('1')

#            handler_input.response_builder.addDirective({
#                'type': 'Connections.SendRequest',
#                'name': 'AskFor',
#                        'payload': {
#                            '@type': 'AskForPermissionsConsentRequest',
#                            '@version': '1',
#                            'permissionScope': 'alexa::alerts:timers:skill:readwrite'
#                          },
#                      token: 'verifier'
#                      
#            return handler_input.response_builder.add_directive(
#                SendRequestDirective(
#                    name="AskFor",
#                    payload={
#                        "@type": 'AskForPermissionsConsentRequest',
#                        "@version": '1',
#                        "permissionScope": ['alexa::alerts:timers:skill:readwrite'],
#                    },
#                    token="verifier"
#                )
#            ).response          

#            return handler_input.response_builder.add_directive(
#                SendRequestDirective(
#                    name="Upsell",
#                    payload={
#                        "InSkillProduct": {
#                            "productId": "<product_id>",
#                        },
#                        "upsellMessage": "<???????????????????????????????????????????????????>",
#                    },
#                    token="correlationToken"
#                )
#            ).response          

            #return handler_input.response_builder.speak("?????????????????????????????????????????????").set_card(AskForPermissionsConsentCard(permissions=["alexa::alerts:timers:skill:readwrite"])).response
            #handler_input.response_builder.set_card(
            #    AskForPermissionsConsentCard(permissions=["alexa::alerts:timers:skill:readwrite"]))
            #logger.error('2')
#           # handler_input.response_builder.response
#           # logger.error('3')
            #return (
            #    handler_input.response_builder
            #        .response
            #)
#        else:
#            logger.error('?????????????????????????????????' + user_permissions.consent_token)
#        logger.error('4')

        #extract persistent attributes, if they exist
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_exist = ('RiceAmount' in attr)
        if attributes_exist:
            RiceAmount = attr['RiceAmount']
            speak_output = speak_output + "????????? {RiceAmount}????????????????????????".format(RiceAmount=str(RiceAmount))
        #else:
        #    speak_output = speak_output
        speak_output = speak_output + "????????????????????????"
        
        #speak_output = "Welcome, you can say Hello or Help. Which would you like to try?"
        #speak_output = "????????????????????????????????????????????????????????????"
        reprompt_output = "????????????????????????"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_output)
                .response
        )


class CaptureRiceAmountIntentHandler(AbstractRequestHandler):
    """Handler for Rice Amount Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureRiceAmountIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        RiceAmount = handler_input.request_envelope.request.intent.slots["RiceAmount"].value #handler_input.request_envelope.request.intent.slots["pet"].value
        WaterAmount = float(RiceAmount) * 180 * 1.2
        speak_output = str(RiceAmount) + "????????????????????????" + str(int(round(WaterAmount,-1))) + "??????????????????????????????????????????"
        
        donabeTimer_attributes = {
                'RiceAmount': RiceAmount
                }
        attributes_manager = handler_input.attributes_manager
        attributes_manager.persistent_attributes = donabeTimer_attributes
        attributes_manager.save_persistent_attributes()
#        speak_output = str(RiceAmount) + "???????????????"
#        speak_output =  "???????????????"
        return (
            handler_input.response_builder
                .speak(speak_output)
#                .ask("add a reprompt if you want to keep the session open for the user to respond")
#                .ask(speak_output)
                .response
        )

class StartCookIntentHandler(AbstractRequestHandler):
    """Handler for StartCook Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StartCook")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "?????????????????????????????????"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
#                .ask("add a reprompt if you want to keep the session open for the user to respond")
#                .ask(speak_output)
                .response
        )


class CreateReminderIntentHandler(AbstractRequestHandler):
    """Handler to create reminder"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input) and \
              (is_intent_name("CreateReminderIntent")(handler_input) or
                is_intent_name("AMAZON.YesIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Reminder Intent handler")
        request_envelope = handler_input.request_envelope
        response_builder = handler_input.response_builder
#        reminder_service = handler_input.service_client_factory.get_reminder_management_service()

        if not (request_envelope.context.system.user.permissions and
                request_envelope.context.system.user.permissions.consent_token):
            
            #return response_builder.speak(NOTIFY_MISSING_PERMISSIONS).set_card(AskForPermissionsConsentCard(permissions=PERMISSIONS)).response
            
            return response_builder.add_directive(
                SendRequestDirective(
                    name="AskFor",
                    payload={
                        "@type": "AskForPermissionsConsentRequest",
                        "@version": "1",
                        "permissionScope": "alexa::alerts:reminders:skill:readwrite"
                    },
                    token="correlationToken"
                )
            ).response

        reminder_service = handler_input.service_client_factory.get_reminder_management_service()

        
        now = datetime.datetime.now(pytz.timezone(TIME_ZONE_ID))
        five_mins_from_now = now + datetime.timedelta(minutes=+5)
        notification_time = five_mins_from_now.strftime("%Y-%m-%dT%H:%M:%S")

        # Create an instance of the recurrence object
        

        # Set the missing attributes on the instance's deserialized_types map, 
        # as following :
        recurrence_pattern = [
           "FREQ=DAILY;BYHOUR=6;BYMINUTE=10;BYSECOND=0;INTERVAL=1;",
           "FREQ=DAILY;BYHOUR=17;BYMINUTE=15;BYSECOND=0;INTERVAL=1;",
           "FREQ=DAILY;BYHOUR=19;BYMINUTE=45;BYSECOND=0;INTERVAL=1;"
        ]

        trigger = Trigger(object_type = TriggerType.SCHEDULED_ABSOLUTE , scheduled_time = notification_time ,time_zone_id = TIME_ZONE_ID, recurrence = Recurrence(recurrence_rules=recurrence_pattern))
        text = SpokenText(locale='en-US', ssml = "<speak> Great! I have scheduled reminder for you.</speak>", text= 'This is medicine reminder. Please take your medicine')
        alert_info = AlertInfo(SpokenInfo([text]))
        push_notification = PushNotification(PushNotificationStatus.ENABLED)
        reminder_request = ReminderRequest(notification_time, trigger, alert_info, push_notification)

        try:
            reminder_response = reminder_service.create_reminder(reminder_request)
            logger.info("Reminder Created: {}".format(reminder_response))
        except ServiceException as e:
            logger.info("Exception encountered: {}".format(e.body))
            return response_builder.speak(ERROR).response

        return response_builder.speak("Your medicine reminder created").set_card(SimpleCard("Medicine Reminder" , "Medicine Reminder created")).response



class ConnectionsResponseHandler(AbstractRequestHandler):

    """ Handler for connections response """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((ask_utils.is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "AskFor"))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In Connections Response Handler")

        response_payload = handler_input.request_envelope.request.payload
        if response_payload and 'status' in response_payload:
            response_status = response_payload['status']
        else: 
            response_status =""        

        #logger.info("Status value is --> {}".format(response_status))

        if (response_status == 'NOT_ANSWERED'):
            return handler_input.response_builder.speak(
                "Please provide Timer permission using the card I have sent to your Alexa app.").set_card(AskForPermissionsConsentCard(permissions=PERMISSIONS)).response

        elif (response_status == 'DENIED'):
            return handler_input.response_builder.speak(
                "You can grant permission anytime by going to Alexa app").response

        else:
            return handler_input.response_builder.speak(
                "Do you want to schedule a medicine reminder?").ask("What do you want to do?").response



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        #speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        speak_output = "?????????????????????????????????????????????????????????????????????????????????"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class LoggingRequestInterceptor(AbstractRequestInterceptor):
    """ Log the request envelope. """

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Received : {}".format(handler_input.request_envelope))


class LoggingResponseInterceptor(AbstractResponseInterceptor):
    """ Log the response envelope """

    def process(self, handler_input, response):
        # type: (HandlerInput) -> None
        logger.info("Response generated: {}".format(response))



# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


#sb = SkillBuilder()
#sb = CustomSkillBuilder(persistence_adapter=s3_adapter)
#sb = CustomSkillBuilder(api_client=DefaultApiClient())
sb = CustomSkillBuilder(api_client=DefaultApiClient(),persistence_adapter=s3_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureRiceAmountIntentHandler())
sb.add_request_handler(StartCookIntentHandler())
sb.add_request_handler(CreateReminderIntentHandler())
sb.add_request_handler(ConnectionsResponseHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

# Adding Request and response interceptor
sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_response_interceptor(LoggingResponseInterceptor())


lambda_handler = sb.lambda_handler()