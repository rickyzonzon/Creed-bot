# Chatbot core

import random
import json
import torch
from bot_trainer.model import NeuralNet
from bot_trainer.nltk_utils import bag_of_words, tokenize
from cores.emotion_core import Emotion
from cores.va_core import *


# ChatCore class creates an instance
class ChatCore:

    bot_name = "Creed"

    def __init__(self):
        self.FILE = "bot_trainer\\data\\speech_data.pth"
        self.emotions = Emotion(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        self.sentence = ""
        self.log = open("log.txt", "a")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        with open("bot_trainer\\data\\intents.json", "r") as f:
            self.intents = json.load(f)

        self.data = torch.load(self.FILE)
        self.input_size = self.data["input_size"]
        self.hidden_size = self.data["hidden_size"]
        self.output_size = self.data["output_size"]
        self.all_words = self.data["all_words"]
        self.tags = self.data["tags"]
        self.model_state = self.data["model_state"]
        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)

        self.initialize()

    # Establish the neural network
    def initialize(self):
        self.log.truncate(0)
        self.model.load_state_dict(self.model_state)
        self.model.eval()

    # Analyze sentiment of user input based on sentiment.json, update emotion accordingly
    # not yet implemented
    def analyze_sentiment(self, tokenized_sentence):
        pass

    # Talk to Creed
    def chat(self, sentence):

        self.log.write(f"You: {sentence}\n")

        tokenized_sentence = tokenize(sentence)
        analysis = self.analyze_sentiment(tokenized_sentence)

        X = bag_of_words(tokenized_sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        self.log.write(f"{tag}: {prob.item()}: {analysis}\n")

        response = ""

        # Threshold can be adjusted as needed when more data is added
        if prob.item() > 0.97:
            for intent in self.intents["intents"]:
                if tag == intent["tag"]:
                    if intent["tag"] == "goodbye":
                        response = response + random.choice(intent["responses"])
                        self.log.write(response + "\n")
                        self.log.close()
                        return assistantResponse(response)
                    elif intent["tag"] == "date":
                        response = response + random.choice(intent["responses"]) + getDate()
                        self.log.write(response + "\n")
                        return assistantResponse(response)
                    elif intent["tag"] == "time":
                        response = response + random.choice(intent["responses"]) + getTime()
                        self.log.write(response + "\n")
                        return assistantResponse(response)
                    elif intent["tag"] == "person_info":
                        # search memory first, use [1] if found in memory (to be implemented)
                        if getPerson(self.all_words, sentence)[0]:
                            response = response\
                                       + random.choice(intent["responses"][0])\
                                       + getPerson(self.all_words, sentence)[1]
                            self.log.write(response + "\n")
                        else:
                            response = response \
                                       + getPerson(self.all_words, sentence)[1]
                            self.log.write(response + "\n")
                        return assistantResponse(response)
                    elif intent["tag"] == "general_info":
                        # search memory first (to be implemented)
                        getInfo(sentence)
                        response = response\
                                   + random.choice(intent["responses"])\
                                   + f'\"{sentence}\":'
                        self.log.write(response + "\n")
                        return assistantResponse(response)
                    elif intent["tag"] == "how_to":
                        howTo(sentence)
                        response = response + random.choice(intent["responses"])
                        self.log.write(response + "\n")
                        return assistantResponse(response)
                    elif intent["tag"] == "status":
                        response = response \
                                   + f'{random.choice(intent["responses"])} ' \
                                   + random.choice(self.emotions.status())
                        self.log.write(response + "\n")
                        return assistantResponse(response)
                    else:
                        response = response + random.choice(intent["responses"])
                        self.log.write(response + "\n")
                        return assistantResponse(response)
        else:
            response = response + "I can't do that for you right now."
            self.log.write(response + "\n")
            return assistantResponse(response)

creed = ChatCore()
creed.chat("ok")