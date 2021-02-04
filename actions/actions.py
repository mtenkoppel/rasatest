# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset, FollowupAction, Form, ActiveLoop
from rasa_sdk.events import SlotSet
from datetime import datetime
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ActionReset(Action):

    def name(self) -> Text:
        return "action_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        AllSlotsReset()
        dispatcher.utter_message(text="[Resetted all slots]")
        return [AllSlotsReset()]


class CalcPrice:
    @staticmethod
    def total_price(num_nights, num_guests, breakfast=False):
        price_per_night_per_guest = 75
        price_for_breakfast = 9
        price = price_per_night_per_guest * num_nights * num_guests
        if breakfast:
            price = price + (price_for_breakfast * num_nights * num_guests)
        return price



class ResetFormValues(Action):

    def name(self) -> Text:
        return "reset_form_values"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="[debug: all values resetted (user may reinitiate a booking)")

        return [AllSlotsReset()]


class ValidateRestaurantForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_book_form"

    @staticmethod
    def hotels_db() -> List[Text]:
        """Database of supported hotels"""

        return ["amsterdam", "berlin", "hamburg", "paris", "madrid"]

    def validate_aacity(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate hotel value."""
        if slot_value.lower() in self.hotels_db():
            # city uttered is within primitive database
            return {"aacity": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text=f"Unfortuately, there is not hotel in {slot_value}.")
            return {"aacity": None}

    def validate_num_nights(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """output rich data after num nights have been inputted hotel value."""

        # variables for part 1
        city = tracker.get_slot("aacity")
        date = tracker.get_slot("arrival_date")
        num_nights = slot_value
        num_guests = tracker.get_slot("num_guests")

        # code to write date back to something more readble to user
        date = date[0:date.find("T")]
        date_time_obj = datetime.strptime(date, '%Y-%m-%d')
        human_readable_date = date_time_obj.strftime('%d %B %Y')

        price = CalcPrice.total_price(num_nights, num_guests, False)
        msg = f"A room in our hotel in {city} arriving at {human_readable_date} for {num_nights} nights and {num_guests} guests costs {price} Euro. Here are some images of the room:"

        city_fn = city.lower()

        test_carousel = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "Hotel",
                    "subtitle": f"The hotel is located right in the centre of {city_fn}. It has a great connection to public transport and a large parking area. The hotel is open 24/7 and you can check-in at any time after 10:00.",
                    "image_url": f"static/images/{city_fn}.png",
                    "buttons": []
                },
                    {
                        "title": "Room",
                        "subtitle": f"The room has a double sized bed and is equiped with all the comfort you need to relax for a great night sleep",
                        "image_url": f"static/images/hotel1.png",
                        "buttons": []
                    },
                    {
                        "title": "Great view",
                        "subtitle": f"Most rooms come with a great view over the city.",
                        "image_url": f"static/images/hotel2.png",
                        "buttons": []
                    },
                    {
                        "title": "Bathroom",
                        "subtitle": f"A luxury bathroom where you can spend hours. Our towels service delivers you new towels every day.",
                        "image_url": f"static/images/hotel3.png",
                        "buttons": []
                    },
                    {
                        "title": "Small details",
                        "subtitle": f"Many details make you feel right at home: all our bathrooms come with 4 kinds of shampoo and soap.",
                        "image_url": f"static/images/hotel4.png",
                        "buttons": []
                    }
                ]
            }
        }

        dispatcher.utter_message(text=msg)
        channel = tracker.get_latest_input_channel()
        print(channel)
        if channel != "cmdline":
            dispatcher.utter_message(attachment=test_carousel)
        return {"num_nights": slot_value}

    def validate_person_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        # variables for part 1
        city = tracker.get_slot("aacity")
        date = tracker.get_slot("arrival_date")
        num_nights = tracker.get_slot("num_nights")
        num_guests = tracker.get_slot("num_guests")

        # code to write date back to something more readble to user
        date = date[0:date.find("T")]
        date_time_obj = datetime.strptime(date, '%Y-%m-%d')
        human_readable_date = date_time_obj.strftime('%d %B %Y')

        # variables for part 2
        person_name = slot_value
        breakfast = tracker.get_slot("breakfast")
        payment_method = tracker.get_slot("payment_method")
        email = tracker.get_slot("email")

        breakfast_msg = "" if breakfast else "not"
        payment_method_msg = "on location" if payment_method else "online"

        price = CalcPrice.total_price(num_nights, num_guests, breakfast)

        msg = f"Summary: Reservation for {person_name} in hotel " \
              f"{city} from {human_readable_date} for {num_nights} " \
              f"with {num_guests} guests. Breakfast is {breakfast_msg} included. " \
              f"Payment is done {payment_method_msg}. Full price is {price} Euro."

        dispatcher.utter_message(text=msg)


        return{"person_name": slot_value}

