from agent import get_action

while True:
    user = input("You: ")
    print(get_action(user))