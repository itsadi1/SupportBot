import nltk
from random import randint
import supportbotdb as db
from logindb import login

# Uncomment these lines if running for the first time
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

close = False
# Detailed keyword arrays
KEYWORDS = {
    "issue": [
        "issue", "problem", "not working", "error", "trouble", "fail", "failure", "bug", "glitch", "crash", "stuck"
    ],
    "billing": [
        "bill", "billing", "invoice", "charge", "payment", "overcharged", "refund", "amount", "deducted"
    ],
    "technical": [
        "technical", "network", "connection", "internet", "wifi", "slow", "speed", "signal", "disconnect", "lag"
    ],
    "delivery": [
        "delivery", "shipment", "order", "late", "delay", "not delivered", "missing", "lost", "track order"
    ],
    "dissatisfaction": [
        "not satisfied", "unsatisfactory", "bad service", "poor service", "disappointed", "unhappy", "frustrated", "angry"
    ],
    "complaint": [
        "complaint", "report", "escalate", "raise", "file", "register"
    ],
    "feedback": [
        "feedback", "suggestion", "recommend", "improve", "comment", "opinion"
    ],
    "takeback": [
        "take back", "retract", "withdraw", "drop", "resolved","Abandon", "cancel", "cancel complaint"
    ],
    "status": [
        "status", "track", "update", "progress", "check", "pending", "resolved", "open", "closed"
    ],
    "help": [
        "help", "support", "assist", "assistance", "need", "question", "query", "how to", "what if"
    ],
    "greeting": [
        "hello", "hi", "hey", "greetings", "good morning", "good evening", "good afternoon"
    ],
    "farewell": [
        "bye", "goodbye", "exit", "quit", "see you", "thanks", "thank you"
    ],
    "service_request": [
        "upgrade", "downgrade", "change plan", "plan", "activate", "deactivate", "subscription", "renew"
    ],
    "faq": [
        "working hours", "contact", "address", "location", "phone", "email", "customer care", "service center"
    ]
}

FAQ_ANSWERS = {
    "working hours": "Our customer care is available 24/7.",
    "contact": "You can contact us at 9868594944 or email itsadi1@outlook.com",
    "address": "Our main office is at Galgotias Hostel, Room no. 976.",
    "location":  "Our main office is at Galgotias Hostel, Room no. 976.",
    "phone": "Our customer care number is 9868594944.",
    "email": "You can email us at itsadi1@outlook.com.",
    "service center": "Sorry, we don't have a service center. We provide online support.",
}

def respond(text):
    print(f"SupportBot: {text}")

def get_input():
    return input("You: ")

def generate_ticket():
    ticket = randint(1000,9999)
    if ticket not in db.tklist(Id):
        return ticket
    else:
        return generate_ticket()

def contains_any(phrase, keywords):
    return any(k in phrase for k in keywords)

def process_nltk(data):
    global close
    data_lower = data.lower()
    tokens = nltk.word_tokenize(data_lower)
    # print("tokens: "+str(tokens))

    tagged = nltk.pos_tag(tokens)
    # print("tagged: "+str(tagged))

    # 1. Greetings
    if contains_any(data_lower, KEYWORDS["greeting"]):
        responses = [
            "Hello! How may I assist you today?",
            "Hi there! How can I help?",
            "Hey! What can I do for you?"
        ]
        respond(responses[randint(0, 2)])
        return

    # 2. Farewell
    if contains_any(data_lower, KEYWORDS["farewell"]):
        respond("Thank you for contacting customer care. Have a great day!")
        close = True
        return

    # 3. FAQs
    for faq in FAQ_ANSWERS:
        if faq in data_lower:
            respond(FAQ_ANSWERS[faq])
            return

    # 4. Service Requests
    if contains_any(data_lower, KEYWORDS["service_request"]):
        Plan = db.plan(Id)[0]
        if "upgrade" in data_lower or "change plan" in data_lower:
            if Plan != 'premium':
                respond("Sure, I can help you upgrade your plan. Please specify the plan you'd like to upgrade to.")
                plan = get_input().strip().lower()
                if plan.lower() not in ["basic", "standard", "premium"]:
                    respond("Invalid plan. Request cannot be processed.")
                else:
                    db.upgrade(Id, plan)
            else:
                respond("You are already on the highest plan (Premium).")
        elif "downgrade" in data_lower:
            if Plan != 'basic':
                respond("Sure, I can help you downgrade your plan. Please specify the plan you'd like to downgrade to.")
                plan = get_input().strip().lower()
                if plan not in ["basic", "standard"]:
                        respond("Invalid plan. Request cannot be processed.")
                else:
                    if (Plan == "premium" and plan in ["basic", "standard"]) or (Plan== "standard" and plan in ["basic",]):
                        db.downgrade(Id, plan)
                    else:
                        respond("You must downgrade to a plan lower than your current plan.")
            else:
                respond("You are already on the lowest plan (Basic).")        
        elif "cancel" in data_lower or "deactivate" in data_lower:
            respond("I'm sorry to see you go. Please confirm if you want to cancel your subscription (yes/no).")
            confirm = get_input().lower()
            if "yes" in confirm:
                ticket = generate_ticket()
                db.terminate(Id, ticket)
                respond(f"Your cancellation request has been submitted. Your ticket number is {ticket}.If you change your mind, let us know!")
            else:
                respond("Cancellation aborted. Let us know if you need anything else.")
        return
    
    # 5. Issue Reporting (with type detection)
    if contains_any(data_lower, KEYWORDS["issue"] + KEYWORDS["billing"] + KEYWORDS["technical"] + KEYWORDS["delivery"]):
        issue_type = "General"
        if contains_any(data_lower, KEYWORDS["billing"]):
            issue_type = "Billing"
        elif contains_any(data_lower, KEYWORDS["technical"]):
            issue_type = "Technical"
        elif contains_any(data_lower, KEYWORDS["delivery"]):
            issue_type = "Delivery"

        respond(f"It seems you have a {issue_type.lower()} issue. Could you please describe your issue in detail?")
        issue = get_input()
        ticket = generate_ticket()
        db.request(Id, issue_type, issue, ticket)
        respond(f"Thank you. Your {issue_type.lower()} issue has been logged. Your ticket number is {ticket}. Our team will get back to you soon.")
        return
    # 5.2. Request Cancellation
    if contains_any(data_lower, KEYWORDS["takeback"]):
        respond("Do you want to cancel your Complaint ? (yes/no)")
        confirm = True if get_input().strip().lower() == "yes" else False
        if confirm:
            respond("Please provide your ticket number.")
            ticket = get_input().strip()
            found = True if ticket in db.tklist(Id) else False
            if found:
                db.request_cancel(Id,ticket)
                respond("Your request has been cancelled.")
            else:
                respond("Sorry, I couldn't find a complaint with that ticket number.")
        else:
            respond("Cancellation aborted. Let us know if you need anything else.")
        return
    # 6. Service Dissatisfaction / Escalation
    if contains_any(data_lower, KEYWORDS["dissatisfaction"]):
        respond("I'm sorry to hear that our service did not meet your expectations. Would you like to escalate this as a formal complaint or provide feedback?")
        followup = get_input().lower()
        if contains_any(followup, KEYWORDS["complaint"]):
            respond("Please describe your complaint.")
            complaint = get_input()
            ticket = generate_ticket()
            db.request(Id, "Complaint", complaint, ticket)
            respond(f"Your complaint has been registered. Your ticket number is {ticket}.")
        elif contains_any(followup, KEYWORDS["feedback"]):
            respond("Please share your feedback.")
            feedback = get_input()
            db.feedback(Id, feedback)
            respond("Thank you for your valuable feedback. We appreciate your input and will work to improve our service.")
        else:
            respond("Thank you for letting us know. If you'd like to provide more details, please let me know.")
        return

    # 7. Complaint/Issue Status Tracking
    if contains_any(data_lower, KEYWORDS["status"]):
        respond("Please provide your ticket number.")
        ticket = get_input().strip()
        found = True if ticket in db.tklist(Id) else False
        if found:
            status = db.status(ticket)
            if status == "open":
                respond(f"Your ticket number {ticket} is currently open. Our team is working on it.")
            elif status == "closed":
                respond(f"Your ticket number {ticket} has been resolved. Thank you for your patience.")
        else:
            respond("Sorry, I couldn't find a complaint with that ticket number.")
        return

    # 8. Feedback & Suggestions
    if contains_any(data_lower, KEYWORDS["feedback"]):
        respond("We value your feedback. Please share your thoughts.")
        feedback = get_input()
        db.feedback(Id, feedback)
        respond("Thank you for your feedback. We appreciate your input!")
        return

    # 9. General Help/Support
    if contains_any(data_lower, KEYWORDS["help"]):
        respond(
            "I'm here to assist you! You can:\n"
            "- Report an issue (billing, technical, delivery, etc.)\n"
            "- File a complaint or escalate a problem\n"
            "- Request a service change (upgrade, cancel, etc.)\n"
            "- Track a complaint\n"
            "- Provide feedback\n"
            "- Ask about our working hours, contact info, and more\n"
            "How can I help you today?"
        )
        return

    # 10. Fallback
    respond("I'm sorry, I didn't quite understand. Could you please rephrase or specify if you need help, want to report an issue, request a service, or give feedback?")

def main():
    global username, plan, Id
    username, plan, Id = login()
    respond("Welcome to Customer Care! How may I assist you today?")
    while not close:
        data = get_input()
        process_nltk(data)

if __name__ == "__main__":
    main()
