
from termcolor import colored

def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    formatted_messages = []
    for message in messages:
        if message["role"] == "system":
            formatted_messages.append(f"system: {message['content']}\n")
        elif message["role"] == "user":
            formatted_messages.append(f"user: {message['content']}\n")
        elif message["role"] == "assistant" and message.get("function_call"):
            formatted_messages.append(f"assistant: {message['function_call']}\n")
        elif message["role"] == "assistant" and not message.get("function_call"):
            formatted_messages.append(f"assistant: {message['content']}\n")
        elif message["role"] == "function":
            formatted_messages.append(f"function ({message['name']}): {message['content']}\n")
    for formatted_message in formatted_messages:
        print(
            colored(
                formatted_message,
                role_to_color[messages[formatted_messages.index(formatted_message)]["role"]],
            )
        )
        

def pretty_print_message(message):
    role_to_color = {
        "system": "red",
        "human": "green",
        "ai": "blue",
        "function": "magenta",
    }

    # Define a default formatted message
    formatted_message = f"{message['role']}: {message['content']}\n"

    # Adjust the formatted message based on role
    if message["role"] == "system":
        formatted_message = f"system: {message['content']}\n"
    elif message["role"] == "human":
        formatted_message = f"human: {message['content']}\n"
    elif message["role"] == "ai":
        formatted_message = f"{message['name']}: {message['content']}\n"
    elif message["role"] == "function":
        formatted_message = f"function ({message['name']}): {message['content']}\n"

    # Print the formatted message with the appropriate color
    print(colored(formatted_message, role_to_color[message["role"]]))
    

def pretty_print_message_by_name(message):
    name_to_color = {
        "story": "yellow",
        "environment": "green",
        "character": "blue",
        "style": "magenta",
        "plot": "cyan",
        "programmer": "cyan",
        "critic": "red",
        "keyword": "magenta",
        "summarizer": "green",
        "grammar": "yellow",
    }

    # Find the appropriate color based on the names in the name_to_color dictionary
    color = "white"  # Default color
    for keyword, keyword_color in name_to_color.items():
        if keyword in message['name'].lower():
            color = keyword_color
            break

    # Format and print the message
    formatted_message = f"{message['name']}: {message['content']}\n"
    print(colored(formatted_message, color))
