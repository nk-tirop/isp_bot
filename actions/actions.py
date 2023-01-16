from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionIamabot(Action):
    def name(self) -> Text:
        return "action_iamabot"
    
    def run(self, dispatcher, tracker, domain):
        message = "I am a bot, powered by Rasa."
        dispatcher.utter_message(text=message)
        return []
        
class NoInternetAction(Action):
    def name(self) -> Text:
        return "action_no_internet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's intent and entities
        intent = tracker.latest_message['intent'].get('name')
        router_entities = tracker.latest_message['entities']

        # Check if the intent is "no internet"
        if intent == "no_internet":
            # Ask the user to check the router
            response = "Please check if your router is connected to a valid power socket and turned on. Are the lights on the router showing that it is turned on?"
            dispatcher.utter_message(response)
            return []
        
        # check for the user's answer
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            response = "Thank you for confirming. Please check your internet connection and let us know if the problem persist."
            dispatcher.utter_message(response)
            return []
        elif last_message.lower() == 'no':
            response = "Please connect it to a valid power source and turn it on. Let us know if the problem persist."
            dispatcher.utter_message(response)
            return []
        
        # check if the user recieved notification on repairs
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            response = "Connection lines are under maintainance please be patient."
            dispatcher.utter_message(response)
            return []
        elif last_message.lower() == 'no':
            # Check if the user has paid for the subscription
            response = "Have you paid for your subscription?"
            dispatcher.utter_message(response)
            return []
        
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            # Request the user's router number
            response = "Please provide your router number."
            dispatcher.utter_message(response)
            return []
        
        # Get the router details from the file
        router_number = last_message
        router_details = get_router_details(router_number)
        under_maintainance = router_details['under_maintainance']
        subscription_status = router_details['subscription_status']
        is_active = router_details['is_active']
        
        # Check the router details
        if under_maintainance:
            response = "Connection lines are under maintainance please be patient."
        elif not subscription_status:
            response = "Your subscription has expired. Please renew it."
        elif not is_active:
            response = "Your account has been deactivated."
        else:
            response = "We are sorry, we could not find the problem. Please contact us for further assistance."
        dispatcher.utter_message(response)
       

class SlowInternetAction(Action):
    def name(self) -> Text:
        return "action_slow_internet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's intent and entities
        intent = tracker.latest_message['intent'].get('name')

        # Check if the intent is "slow internet"
        if intent == "slow_internet":
            # Inform the user of potential network congestion
            response = "The network might be congested, please restrict the number of connections allowed. Has this helped with the slow internet speed?"
            dispatcher.utter_message(response)
            return []
        
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            response = "Glad to hear it! Let us know if you have any other issues."
            dispatcher.utter_message(response)
            return []
        elif last_message.lower() == 'no':
            response = "Is there any large download taking place?"
            dispatcher.utter_message(response)
            return []
        
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            response = "Please be patient or disconnect the device from the network."
            dispatcher.utter_message(response)
            return []
        elif last_message.lower() == 'no':
            # Request the user's router number
            response = "Please provide your router number."
            dispatcher.utter_message(response)
            return []

        # Get the router details from the file
        router_number = last_message
        router_details = get_router_details(router_number)
        subscription_type = router_details['subscription_type']
        
        if subscription_type != 'very_fast':
            response = "Your subscription type is "+subscription_type+". Would you like to upgrade to very fast subscription"
            dispatcher.utter_message(response)
            return []
        else:
            response = "We are sorry, we could not find the problem. Please contact us for further assistance."
            dispatcher.utter_message(response)

from typing import Any, Dict, List, Text

class ChangePasswordAction(Action):
    def name(self) -> Text:
        return "action_change_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's intent
        intent = tracker.latest_message['intent'].get('name')

        # Check if the intent is "change password"
        if intent == "change_password":
            # Ask if the user wants to change their password
            response = "Do you want to change your password?"
            dispatcher.utter_message(response)
            return []
        
        # Get the user's answer
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            # Request the user's router number
            response = "Please provide your router number."
            dispatcher.utter_message(response)
            return []
        
        # Get the router number and confirm if correct
        router_number = last_message
        response = f"Just to confirm, your router number is: {router_number}. Is this correct?"
        dispatcher.utter_message(response)
        return []
        
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            # Request the user's new password
            response = "Please provide your new password."
            dispatcher.utter_message(response)
            return []
        elif last_message.lower() == 'no':
            response = "Please provide the correct router number."
            dispatcher.utter_message(response)
            return []
        
        # Get the new password and confirm
        new_password = last_message
        response = "Please confirm your new password."
        dispatcher.utter_message(response)


class PasswordAction(Action):
    def name(self) -> Text:
        return "action_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's intent
        intent = tracker.latest_message['intent'].get('name')

        # Check if the intent is "password"
        if intent == "password":
            # Request the user's router number
            response = "Please provide your router number."
            dispatcher.utter_message(response)
            return []
        
        # Get the router number
        router_number = tracker.latest_message['text']
        # Get the router details from the file
        router_details = get_router_details(router_number)
        password = router_details['password']
        
        # Provide the password
        response = "Your password is: " + password
        dispatcher.utter_message(response)
        
        # Ask if the password helped
        response = "Has this helped with connecting to the network?"
        dispatcher.utter_message(response)
        return []
        
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            response = "Glad to hear it! Let us know if you have any other issues."
            dispatcher.utter_message(response)
            return []
        elif last_message.lower() == 'no':
            response = "Please resend your router number."
            dispatcher.utter_message(response)
            return []
        
        # Check if the second router number is the same as the first
        router_number_2 = tracker.latest_message['text']
        if router_number == router_number_2:
            response = "Sorry I could not help you. Do you want to connect to customer service?"
            dispatcher.utter_message(response)
            return []
        else:
            # Provide the password
            response

class ReactivateSubscriptionAction(Action):
    def name(self) -> Text:
        return "action_reactivate_subscription"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's intent
        intent = tracker.latest_message['intent'].get('name')

        # Check if the intent is "subscription/account reactivation"
        if intent == "reactivate_subscription":
            # Request the user's router number
            response = "Please provide your router number."
            dispatcher.utter_message(response)
            return []
        
        # Get the router number
        router_number = tracker.latest_message['text']
        # Get the router details from the file
        router_details = get_router_details(router_number)
        
        # Confirm the router number
        response = "Just to confirm, your router number is: " + router_number + ". Is this correct?"
        dispatcher.utter_message(response)
        return []
        
        last_message = tracker.latest_message['text']
        if last_message.lower() == 'yes':
            # Provide payment methods
            response = "We currently accept Visa, Mastercard and PayPal as payment methods. Which method would you like to use?"
            dispatcher.utter_message(response)
            return []
        elif last_message.lower() == 'no':
            response = "Please provide the correct router number."
            dispatcher.utter_message(response)

class UpgradeSubscriptionAction(Action):
    def name(self) -> Text:
        return "action_upgrade_subscription"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if intent == "upgrade_subscription":
            response = "We can upgrade your subscription to a faster plan. Would you like to proceed?"
            dispatcher.utter_message(response)
            return []
        elif intent == "affirm":
            # Get the router number
            router_number = tracker.get_slot("router_number")
            # Get the router details from the file
            router_details = get_router_details(router_number)
            subscription_type = router_details['subscription_type']
            if subscription_type != 'very_fast':
                response = "We have upgraded your subscription. Your new subscription type is very fast"
                dispatcher.utter_message(response)
                return []
            else:
                response = "Your subscription is already very fast"
                dispatcher.utter_message(response)
                return []

