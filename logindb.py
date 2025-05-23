import supportbotdb as db
from random  import randint
import sys
def generateid():
    Id = randint(100000, 999999)
    if Id not in db.idlist():
        return Id
    else:
        return generateid()

def singnup():
    print("Please create an account.")
    global username, plan, Id
    username = input("Enter your full name: ")
    plan = input("Enter current Plan: (Basic, Standard, Premium): ").strip().lower()
    if plan not in ["basic", "standard", "premium"]:
        print("Invalid plan. Please start again.")
        return False
    else:
        print(f"Plan {plan.capitalize()} selected.")
        Id = generateid()
        print(f"Your confidential ID is {Id}.")
        db.newuser(Id, username, plan)
        print("Account created successfully.")  
        return username, plan, Id
    
def singnin():
    print("Please login to your account.")
    Id = input("Enter your ID: ")
    counter = 0
    while Id not in db.idlist() and counter< 3:
        print(f"Invalid ID. You have {3-counter} attempts left.")
        Id = input("Enter your ID: ")
        if Id in db.idlist():
               break  
        print("Too many attempts. Please create a new account.") 
        counter += 1
    if counter >= 3:
        return False    
    else:
        username = db.idname(Id)[0]
        plan = db.idname(Id)[1]
        print(f"Welcome back, user {username}. Your current plan is {plan.capitalize()}.")
        return username, plan, Id
    
       
def login():
    exists = True if input("Do you have an account? (yes/no): ").strip().lower()== "yes" else False
    global username, plan, Id
    if not exists:
        Singnup = singnup()
        if not Singnup:
            singnup()
        else:
            print("Account logged in successfully.")
            username, plan, Id = Singnup
            return username, plan, Id
    else:
        Singnin = singnin()
        if not Singnin:
            singnup()
        else:
            print("Login successful.")
            username, plan, Id = Singnin
            return username, plan, Id
def main():
    if login():
        print("Logged in Successful.")
        return True
    else:
        print("Login failed. Please try again.")
        return False
if __name__ == "__main__":
    main()