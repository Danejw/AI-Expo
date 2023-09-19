import requests
from models.ChatMessage import ChatMessage
from models.ChatHistory import ChatInputModel
from PrettyPrint import pretty_print_message_by_name

# Test the Programmer endpoint
message = ChatMessage(role= "human", name="User", content="Give me a program snippet of your choice?" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/programmer/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the critic endpoint
message = ChatMessage(role= "human", name="User", content="""Luna Nightshade grew up in a small town, constantly fascinated by puzzles and mysteries. Her inquisitive nature led her to become a renowned detective known for solving complex cases. Luna is haunted by a 
personal tragedy in her past, driving her relentless pursuit of justice. She is determined to uncover the truth behind every mystery, no matter how dangerous or convoluted it may be. With her sharp wit and unique intuition, Luna navigates the shadows of the criminal underworld, always managing to stay one step ahead.""" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/critic/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the summarization endpoint
message = ChatMessage(role= "human", name="User", content="""Nebula Oasis is a luminous realm filled with swirling clouds of vibrant colors, reminiscent of vast nebulas in deep space. Tendrils of stardust intertwine with ethereal mists, creating a mystical ambiance. The ground beneath one's feet appears to be made of shimmering stardust, and as visitors walk through the oasis, constellations form overhead, casting a gentle glow. Fountains of liquid starlight spray and cascade, creating a mesmerizing display. Exotic alien flora dot the landscape, their bioluminescent petals radiating a soft glow. It is a place of ethereal beauty and cosmic wonder, an escape from the mundane into a realm of dreams.""" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/summarization/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the keywords endpoint
message = ChatMessage(role= "human", name="User", content="""Nebula Oasis is a luminous realm filled with swirling clouds of vibrant colors, reminiscent of vast nebulas in deep space. Tendrils of stardust intertwine with ethereal mists, creating a mystical ambiance. The ground beneath one's feet appears to be made of shimmering stardust, and as visitors walk through the oasis, constellations form overhead, casting a gentle glow. Fountains of liquid starlight spray and cascade, creating a mesmerizing display. Exotic alien flora dot the landscape, their bioluminescent petals radiating a soft glow. It is a place of ethereal beauty and cosmic wonder, an escape from the mundane into a realm of dreams.""" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/keywords/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the Grammar endpoint
message = ChatMessage(role= "human", name="User", content="What kine you want ah?" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/grammar/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the Story endpoint
message = ChatMessage(role= "human", name="User", content="Give me an idea of a character?" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/story/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the Plot endpoint
message = ChatMessage(role= "human", name="User", content="Give me an idea of a a plotline for a new story?" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/plot/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the Style endpoint
message = ChatMessage(role= "human", name="User", content="Give me an idea of a style?" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/style/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the Environment endpoint
message = ChatMessage(role= "human", name="User", content="Give me an idea of an environment?" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/environment/", json=message_dict)
pretty_print_message_by_name(response.json())


# Test the Character endpoint
message = ChatMessage(role= "human", name="User", content="Give me an idea of a character?" )
message1 = ChatMessage(role= "human", name="User", content="I want to write a book" )
message2 = ChatMessage(role= "system", name="System", content="this is a test of the history" )
chathistory = [message1, message2]
inputModel = ChatInputModel(message=message, chatHistory=chathistory)
message_dict = inputModel.dict()
response = requests.post("http://127.0.0.1:8000/character/", json=message_dict)
pretty_print_message_by_name(response.json())
