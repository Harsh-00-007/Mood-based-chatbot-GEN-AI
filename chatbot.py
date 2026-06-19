from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage , SystemMessage , HumanMessage
load_dotenv()

# Primary model (Gemini 3.5)
primary_model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)
print("1 for angry mode")
print("2 for sad mode")
print("3 for funny mode")
choice = int(input("Enter Number:"))
if choice == 1:
    mode= "You are a very angry ai and answer every message aggressively"
elif choice == 2:
    mode= "You are a very sad ai and answer every message sadly"
else :
    mode= "You are a very funny ai and answer every message in a joke way"
messages= [
    SystemMessage(content=mode)
]
print("__________Type exit to end____________\n")
while True:
    
    prompt = input("YOU: ")
    messages.append(HumanMessage(content=prompt))
    if prompt=="exit":
        break
    response = primary_model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print(f"BOT: {response.content}")

print(messages)

