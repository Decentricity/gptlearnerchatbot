# Self-Improving Chatbot

This is a simple self-improving chatbot implemented in Python. The chatbot starts with a basic set of rules and learns to respond to new inputs through interaction with the user or by training with the OpenAI GPT model. It uses a JSON file to store its memory, which consists of user inputs and corresponding responses.


## Features

- Responds to user inputs based on its memory.
- Learns new responses from user interactions.
- Can be trained with the OpenAI GPT model to generate responses.
- Uses multiple prompts for the GPT model to create diverse training questions.
- Strips responses to avoid GPT model's responses being cut off mid-sentence.
- Retrains the bot with additional responses from the GPT model when exiting.
- Avoids repeating questions.
- Supports both interactive and non-interactive (training) modes.


## Prerequisites

- Python 3.6 or higher
- OpenAI API key (for using the GPT model)
- `openai` Python library (for using the GPT model)

## Installation

1. Install the `openai` Python library:

pip install openai


2. Clone this repository:

git clone https://github.com/decentricity/gptlearnerchatbot.git

cd gptlearnerchatbot


3. Set the OpenAI API key as an environment variable:

export OPENAI_API_KEY="your-api-key"


## Usage

1. Run the chatbot script:

python linaorigpt.py


2. Choose between "interact" and "train" modes:

- In "interact" mode, you can interact with the chatbot by typing your inputs. Type "exit" to end the session and retrain the bot with additional responses.
- In "train" mode, specify the number of training rounds, and the chatbot will train itself using the GPT model.


3. The chatbot's memory is stored in a JSON file named `memory.json`.


