import json
import random
import difflib
import openai
import os
import re

# Get the OpenAI API key from the environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Set up the OpenAI API client with the API key
openai.api_key = OPENAI_API_KEY

# Load the chatbot's memory from a JSON file.
def load_memory():
    try:
        with open('memory.json', 'r') as f:
            memory = json.load(f)
    except FileNotFoundError:
        memory = {}
    return memory

# Save the chatbot's memory to a JSON file.
def save_memory(memory):
    with open('memory.json', 'w') as f:
        json.dump(memory, f, indent=4)

# Find the closest match to the user input in memory.
def find_closest_match(user_input, memory):
    if not memory:
        return None
    closest_match = difflib.get_close_matches(user_input, memory.keys(), n=1, cutoff=0.5)
    return closest_match[0] if closest_match else None

# Use the OpenAI GPT model to generate a response.
def generate_response_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()



# Helper function to trim incomplete sentence from GPT response
def trim_incomplete_sentence(response):
    # Check if the response ends with final punctuation or a comma
    if response[-1] in ".?!,":
        return response
    # Split the response into sentences
    sentences = re.split(r'(?<=[.?!]) +', response)
    # If there is only one sentence, return it as is
    if len(sentences) == 1:
        return response
    # Otherwise, return all sentences except the last one
    return ' '.join(sentences[:-1])

# Process user input and generate a response based on the chatbot's memory or GPT
def respond(user_input, memory):
    closest_match = find_closest_match(user_input, memory)
    if closest_match:
        responses = memory[closest_match]
        # If there are multiple responses, choose one at random
        return random.choice(responses) if isinstance(responses, list) else responses
    else:
        # If no close match is found, use GPT to generate a response
        gpt_response = generate_response_gpt(user_input)
        # Trim incomplete sentence from GPT response
        gpt_response = trim_incomplete_sentence(gpt_response)
        # Store the GPT-generated response in memory as a list
        memory[user_input] = [gpt_response]
        save_memory(memory)
        return gpt_response


# Update the chatbot's memory with alternate responses from GPT.
def update_memory_with_gpt(memory):
    user_inputs = list(memory.keys())
    random.shuffle(user_inputs)
    # Select 1-10 user inputs at random.
    user_inputs = user_inputs[:random.randint(1, 10)]
    for user_input in user_inputs:
        # Get the GPT response for each user input.
        gpt_response = generate_response_gpt(user_input)
        # Store the GPT response as an alternate response in memory.
        if gpt_response not in memory[user_input]:
            memory[user_input].append(gpt_response)
            print(f"User Input: {user_input}\nGPT Response: {gpt_response}\n")
    save_memory(memory)



# Define a list of possible prompts
prompts = [
    "Give me any short question to test a simple chatbot with.",
    "Can you think of a random question for a chatbot?",
    "What's an interesting question to ask a chatbot?",
    "Please provide a question that a chatbot might be asked.",
    "Imagine you're talking to a chatbot. What question would you ask it first?",
    "What's a thought-provoking question someone might have for an AI chatbot?",
    "If you could ask a chatbot anything, what would your question be?",
    "What kind of question would you expect a curious person to ask a chatbot?",
    "Suggest a question that would be interesting to discuss with a chatbot.",
    "What's a common question that people often ask virtual assistants or chatbots?",
    "If you wanted to test a chatbot's intelligence, what question would you ask?",
    "What's a fun or humorous question someone might ask a chatbot?",
    "Think of a question that would be a good conversation starter with a chatbot.",
    "What's a question that could lead to an engaging conversation with a chatbot?",
    "Imagine you're chatting with a friend over coffee. What question might you ask to start a conversation?",
    "What's a question someone might ask when they want to learn more about another person's day or experiences?",
    "Think of a question that someone might ask to get advice or an opinion on a personal matter.",
    "What's a question people often ask when they're making plans for the weekend or for a social event?",
    "Suggest a question that someone might ask to check in on a friend's well-being or mood.",
    "What kind of question might someone ask when they're curious about a friend's hobbies or interests?",
    "Imagine you're catching up with an old friend. What question would you ask to learn about what's new in their life?",
    "What's a question someone might ask to start a discussion about a recent movie, TV show, or book?",
    "Think of a question that someone might ask to seek recommendations for a restaurant, travel destination, or activity.",
    "What's a question people often ask when they want to share or hear about funny or interesting anecdotes?"
]

def main():
    memory = load_memory()
    asked_questions = set()  # Keep track of all previously asked questions

    # Ask the user whether they want to interact or train the bot
    mode = input("Choose mode (interact/train): ").lower()

    if mode == "train":
        # Ask the user for the number of training rounds
        num_rounds = int(input("Enter the number of training rounds: "))
        for i in range(num_rounds):
            # Choose a random prompt from the list of possible prompts
            gpt_prompt = random.choice(prompts)
            user_input = generate_response_gpt(gpt_prompt)
            # Check if the question has been asked before
            while user_input in asked_questions:
                # Regenerate the question with an additional instruction
                gpt_prompt += f" Please don't use this question: '{user_input}'"
                user_input = generate_response_gpt(gpt_prompt)
            print("Generated Question:", user_input)
            # Add the question to the set of asked questions
            asked_questions.add(user_input)
            response = respond(user_input, memory)
            print("Bot:", response)
        # Update memory with alternate responses from GPT after training
        update_memory_with_gpt(memory)
    else:
        # Interactive mode
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                # Update memory with alternate responses from GPT before exiting
                update_memory_with_gpt(memory)
                # Exit the loop and end the program
                return
            # Add the question to the set of asked questions
            asked_questions.add(user_input)
            response = respond(user_input, memory)
            print("Bot:", response)

if __name__ == "__main__":
    main()



