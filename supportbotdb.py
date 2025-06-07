import mysql.connector
from datetime import datetime
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Its@di1",
  port="3306"
)
def newlog(message):
    with open("supportbot.log", "a") as log_file:
        log_file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {message}\n')


def idlist():
  mycursor.execute("SELECT id FROM Customers")
  ids = mycursor.fetchall()
  return [str(Id[0]) for Id in ids]

def issue(ticket):
  mycursor.execute("SELECT issue FROM Customers WHERE ticket = %s", (ticket,))
  issues = mycursor.fetchall()
  return [str(issue[0]) for issue in issues][0]

def plan(Id):
  mycursor.execute("SELECT plan FROM Customers where id = %s", (Id,))
  plans = mycursor.fetchall()
  return [plan for plan in plans][0]

def upgrade(Id, plan):
  mycursor.execute("UPDATE Customers SET plan = %s WHERE id = %s", (plan, Id))
  mydb.commit()
  newlog(f"User {Id} upgraded to {plan} plan.")

def downgrade(Id, plan):
  mycursor.execute("UPDATE Customers SET plan = %s WHERE id = %s", (plan, Id))
  mydb.commit()
  newlog(f"User {Id} downgraded to {plan} plan.")

def terminate(Id,ticket):
  mycursor.execute("UPDATE Customers SET issue='Deactivation',status='open',ticket=%s WHERE id = %s", (ticket,Id))
  mydb.commit()
  newlog(f"User {Id} to be removed from the database.")

def request(Id, issue, complaint, ticket):
  mycursor.execute("SELECT status FROM Customers WHERE id = %s", (Id,))
  status = True if mycursor.fetchone() == ('open',) else False
  if not status:
    mycursor.execute("UPDATE Customers SET issue = %s, complaint = %s,status = 'open',timestamp = CURRENT_TIMESTAMP, ticket = %s WHERE id = %s", (issue, complaint, ticket, Id))  
    mydb.commit()
    newlog(f"User {Id} has registered a {issue} issue with ticket no. {ticket}.")
    return True
  else:
    newlog(f"User {Id} already has an open request.")
    return False

def logout(Id):
  newlog(f"User {Id} has been logged out..")

def feedback(Id, feedback):
  mycursor.execute("UPDATE Customers SET feedback = %s,issue='feedback',status='closed' WHERE id = %s", (feedback, Id))
  mydb.commit()
  newlog(f"User {Id} has provided feedback: {feedback}")

def request_cancel(Id,ticket):
  mycursor.execute("UPDATE Customers SET status = 'closed' WHERE id = %s AND ticket = %s", (Id,ticket))
  mydb.commit()
  newlog(f"User {Id} has closed ticket no. {ticket}.")

def tklist(Id):
  mycursor.execute("SELECT ticket FROM Customers WHERE id = %s", (Id,))
  tickets = mycursor.fetchall()
  return [str(ticket[0]) for ticket in tickets]

def status(ticket):
  mycursor.execute("SELECT status FROM Customers WHERE ticket = %s", (ticket,))
  status = mycursor.fetchall()
  return [str(stat[0]) for stat in status][0]

def idname(ID):
  mycursor.execute("SELECT name,plan FROM Customers where id = %s", (ID,))
  names = mycursor.fetchall()
  return [name for name in names][0]  

def newuser(Id, name, plan):
  mycursor.execute("INSERT INTO Customers (id, name, plan) VALUES (%s, %s, %s)", (Id, name, plan))
  mydb.commit()
  newlog(f"User {name} with ID {Id} and plan {plan} added to the database.") 

def main():
  global mycursor
  mycursor = mydb.cursor()
  mycursor.execute("CREATE DATABASE IF NOT EXISTS supportbotdb")
  mycursor.execute("USE supportbotdb")
  mycursor.execute("SHOW TABLES")

  if ('customers',) not in mycursor.fetchall():
    mycursor.execute("CREATE TABLE Customers(id INT PRIMARY KEY, name VARCHAR(255),plan VARCHAR(255), issue VARCHAR(255),ticket INT, status VARCHAR(255), complaint VARCHAR(255), feedback VARCHAR(255), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

if __name__ == "__main__":
   main() 