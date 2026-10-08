from personal_knowledge_base.mail_utils import save_attachments

def run():
    print("running through run()")
    save_attachments("rami.mayer@yahoo.com", "aviation/Simulator_2015_eng")

    # bot = ChatBot("You are a friendly Python tutor.", max_tokens=2000)
    # print("Type 'quit' to exit.\n")
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower().strip() == "quit":
    #         break
    #     try:
    #         print(f"Bot: {bot.chat(user_input)}\n")
    #     except BudgetExceededError as exc:
    #         print(f"\nBudget reached -- ending the chat. Details: {exc}")
    #         break


if __name__ == "__main__":
    run()