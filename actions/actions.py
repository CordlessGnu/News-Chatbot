# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from newsapi import NewsApiClient
import os

# Initialising news api object with API key in env
newsapi = NewsApiClient(api_key = os.environ.get("NEWS_API_KEY")
)

class ActionGetNews(Action):

    def name(self) -> Text:
        return "action_get_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event = tracker.get_slot("event")

        if event:
            data = newsapi.get_top_headlines(q=event, language='en')
        else:
            data = newsapi.get_top_headlines(sources='bbc-news', language='en')

        articles = data.get('articles')    

        if articles:
            # Take the top 3 headlines to keep the chat clean
            message = f"Here are the latest updates on {event if event else 'the news'}:\n\n"
            for art in articles[:3]:
                message += f"{art['title']}\n"
            
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text=f"I couldn't find any recent news about '{event}'.")
            
        newsapi.get_top_headlines(sources='bbc-news')
        dispatcher.utter_message()


        return [SlotSet("event", None)]
