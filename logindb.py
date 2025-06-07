import supportbotdb as db
from random  import randint

def respondcli(text):
    print(f"SupportBot: {text}")

def get_inputcli():
    return input("You: ")


def generateid():
    Id = randint(100000, 999999)
    if Id not in db.idlist():
        return Id
    else:
        return generateid()

def generate_ticket():
    ticket = randint(1000,9999)
    if ticket not in db.tklist(Id):
        return ticket
    else:
        return generate_ticket()
    
def shuffleresponse(response):
    return response[randint(0, 2)]
    
def singnup(respond,get_input):
    respond("Please create an account.")
    global username, plan, Id
    respond("Enter your full name:")
    username = get_input().strip()
    respond("Enter current Plan: (Basic, Standard, Premium): ")
    plan = get_input().strip().lower()
    if plan not in ["basic", "standard", "premium"]:
        respond("Invalid plan. Please start again.")
        return False
    else:
        respond(f"Plan {plan.capitalize()} selected.")
        Id = generateid()
        respond(f"Your confidential ID is {Id}.")
        db.newuser(Id, username, plan)
        respond("Account created successfully.")  
        return username, plan, Id
    
def singnin(respond, get_input):
    respond("Please login to your account.")
    respond("Enter your ID: ")
    Id = get_input().strip()
    counter = 0
    while Id not in db.idlist() and counter< 3:
        respond(f"Invalid ID. You have {3-counter} attempts left.")
        respond("Enter your ID: ")
        Id = get_input()
        if Id in db.idlist():
               break  
        # respond("Too many attempts. Please create a new account.") 
        counter += 1
    if counter >= 3:
        return False    
    else:
        username = db.idname(Id)[0]
        plan = db.idname(Id)[1]
        respond(f"Welcome back, user {username}. Your current plan is {plan.capitalize()}.")
        return username, plan, Id
    
       
def login(respond, get_input):
    respond("Do you have an existing account? (yes/no)")
    exists = True if get_input().strip().lower()== "yes" else False
    global username, plan, Id
    if not exists:
        Singnup = singnup(respond, get_input)
        if not Singnup:
            return singnup(respond, get_input)
        else:
            respond("Account logged in successfully.")
            username, plan, Id = Singnup
            return username, plan, Id
    else:
        Singnin = singnin(respond, get_input)
        if not Singnin:
            return singnup(respond, get_input)
        else:
            respond("Login successful.")
            username, plan, Id = Singnin
            return username, plan, Id

def main():
    if login(respondcli, get_inputcli):
        respondcli("Logged in Successful.")
        print(plan)
        return True
    else:
        respondcli("Login failed. Please try again.")
        return False
if __name__ == "__main__":
    main()