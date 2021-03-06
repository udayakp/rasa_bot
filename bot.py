from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from policy import RestaurantPolicy
from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)


class RestaurantAPI(object):
    def search(self, info):
        return "papi's pizza place"

class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_search_restaurants'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for restaurants")
        restaurant_api = RestaurantAPI()
        restaurants = restaurant_api.search(tracker.get_slot("cuisine"))
        return [SlotSet("matches", restaurants)]

class Actioncheckstatus(Action):
    def name(self):
        return 'action_check_status'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("checking data...")
        restaurant_api = RestaurantAPI()
        restaurants = restaurant_api.search(tracker.get_slot("cuisine"))
        return [SlotSet("matches", restaurants)]

class ActionSuggest(Action):
    def name(self):
        return 'action_suggest'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("here's what I found:")
        dispatcher.utter_message(tracker.get_slot("matches"))
        dispatcher.utter_message("is it ok for you? "
                                 "hint: I'm not going to "
                                 "find anything else :)")
        return []


def run_rbot_online(input_channel, interpreter,
                          domain_file="resturant_domain.yml",
                          training_data_file='data/stories1.md'):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy()],
                  interpreter=interpreter)

    agent.train_online(training_data_file,
                       input_channel=input_channel,
                       max_history=2,
                       batch_size=50,
                       epochs=200,
                       max_training_samples=300)

    return agent

def train_dialogue(domain_file="mydomain.yml",model_path="models/dialogue",training_data_file="data/mystories.md"):
    agent = Agent(domain_file,policies=[MemoizationPolicy(), RestaurantPolicy()])
    agent.train(training_data_file,max_history=3,epochs=400,batch_size=100,validation_split=0.2)
    agent.persist(model_path)
    # agent.visualize(training_data_file,output_file="graph.png", max_history=2)
    return agent

def train_sdialogue(domain_file="mydomain.yml",model_path="models/dialogue1",training_data_file="data/mystories.md"):
    agent = Agent(domain_file,policies=[MemoizationPolicy(), RestaurantPolicy()])
    agent.train(training_data_file,max_history=3,epochs=400,batch_size=100,validation_split=0.2)
    agent.persist(model_path)
    # agent.visualize(training_data_file,output_file="graph1.png", max_history=2)
    return agent

def train_nlu():
    from rasa_nlu.converters import load_data
    from rasa_nlu.config import RasaNLUConfig
    from rasa_nlu.model import Trainer

    training_data = load_data('data/tst.json')
    trainer = Trainer(RasaNLUConfig("nlu_model_config.json"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/', fixed_model_name="current")

    return model_directory


def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu/default/current")
    agent = Agent.load("models/dialogue", interpreter=interpreter)

    if serve_forever:
        print(">>")
        agent.handle_channel(ConsoleInputChannel())
    return agent

def train():
    train_nlu()
    train_dialogue()
    interpreter = RasaNLUInterpreter("models/nlu/default/current")
    agent = Agent.load("models/dialogue", interpreter=interpreter)
    return agent

def pretrained():
    interpreter = RasaNLUInterpreter("models/nlu/default/current")
    agent = Agent.load("models/dialogue", interpreter=interpreter)
    return agent

def respond(agent,message):
    m = agent.handle_message(message)
    return m
    

if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
            description='starts the bot')

    parser.add_argument(
            'task',
            choices=["train-nlu", "train-dialogue", "run","train-sdialogue","itrain"],
            help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "train-sdialogue":
        train_sdialogue()
    elif task == "itrain":
        utils.configure_colored_logging(loglevel="INFO")
        run_rbot_online(ConsoleInputChannel(), RegexInterpreter())
    elif task == "run":
        run()
    else:
        warnings.warn("Need to pass either 'train-nlu','train-sdialogue','itrain', 'train-dialogue' or "
                      "'run' to use the script.")
        exit(1)
