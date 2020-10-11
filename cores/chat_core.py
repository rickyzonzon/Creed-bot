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
        self.SPEECH_FILE = "bot_trainer\\data\\speech_data.pth"
        self.EMOTION_FILE = "bot_trainer\\data\\emotion_data.pth"
        self.emotions = Emotion(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        self.sentence = ""
        self.log = open("log.txt", "a")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        with open("bot_trainer\\data\\intents.json", "r") as f:
            self.intents = json.load(f)
        
        with open("bot_trainer\\data\\sentiments.json", "r") as f:
            self.sentiments = json.load(f)

        self.speech_data = torch.load(self.SPEECH_FILE)
        self.speech_input_size = self.speech_data["input_size"]
        self.speech_hidden_size = self.speech_data["hidden_size"]
        self.speech_output_size = self.speech_data["output_size"]
        self.speech_all_words = self.speech_data["all_words"]
        self.speech_tags = self.speech_data["tags"]
        self.speech_model_state = self.speech_data["model_state"]
        self.speech_model = NeuralNet(self.speech_input_size,
                                      self.speech_hidden_size,
                                      self.speech_output_size).to(self.device)

        self.emotion_data = torch.load(self.EMOTION_FILE)
        self.emotion_input_size = self.emotion_data["input_size"]
        self.emotion_hidden_size = self.emotion_data["hidden_size"]
        self.emotion_output_size = self.emotion_data["output_size"]
        self.emotion_all_words = self.emotion_data["all_words"]
        self.emotion_tags = self.emotion_data["tags"]
        self.emotion_model_state = self.emotion_data["model_state"]
        self.emotion_model = NeuralNet(self.emotion_input_size,
                                       self.emotion_hidden_size,
                                       self.emotion_output_size).to(self.device)

        self.initialize()

    # Establish the neural network
    def initialize(self):
        self.log.truncate(0)
        self.speech_model.load_state_dict(self.speech_model_state)
        self.emotion_model.load_state_dict(self.emotion_model_state)
        self.speech_model.eval()
        self.emotion_model.eval()

    # Analyze sentiment of user input based on sentiments.json, update emotion accordingly
    # not yet implemented
    def analyze_sentiment(self, tokenized_sentence):
        X = bag_of_words(tokenized_sentence, self.emotion_all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.emotion_model(X)
        probs = torch.softmax(output, dim=1)

        count = 0
        analysis = []
        while count < len(probs[0]):
            self.emotions.change(self.emotion_tags[count], 0.5 * probs[0][count].item())
            analysis.append([self.emotion_tags[count], 0.5 * probs[0][count].item()])
            count += 1

        return analysis

    # Talk to Creed
    def chat(self, sentence):

        self.log.write(f"You: {sentence}\n")

        tokenized_sentence = tokenize(sentence)
        analysis = self.analyze_sentiment(tokenized_sentence)

        X = bag_of_words(tokenized_sentence, self.speech_all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.speech_model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.speech_tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        self.log.write(f"{tag}: {prob.item()}: {analysis}\n")

        response = ""

        # Threshold can be adjusted as needed when more data is added
        if prob.item() > 0.99:
            for intent in self.intents["intents"]:
                if tag == intent["tag"]:

                    if intent["tag"] == "goodbye":
                        response = response + random.choice(intent["responses"])
                        self.log.write(response + "\n")
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
                        if getPerson(self.speech_all_words, sentence)[0]:
                            response = response\
                                       + random.choice(intent["responses"][0])\
                                       + getPerson(self.speech_all_words, sentence)[1]
                            self.log.write(response + "\n")
                        else:
                            response = response \
                                       + getPerson(self.speech_all_words, sentence)[1]
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
                                   + self.emotions.status()
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
