from collections import defaultdict
chat_history = defaultdict(str)

def save_chat_history(user_prompt, gen_response):
    chat_history[user_prompt] = gen_response
    
def retrieve_from_chat_history():
    for prompt, response in chat_history.items():
        return f"user: {prompt}, what gen ai said: {response}"


def delete_history():
    global count
    if count == 5:
        chat_history.clear()
        count = 0
        print("Deleted history")

user_prompt1 = "how to make ice cream"
gen_response1 = "i dont know"

save_chat_history(user_prompt1, gen_response1)

user_prompt2 = "how to make apple pie"
gen_response2 = "i dont know"

save_chat_history(user_prompt2, gen_response2)
# print(chat_history)
# retrieve_from_chat_history()
# delete_history()
print(chat_history)
print()
