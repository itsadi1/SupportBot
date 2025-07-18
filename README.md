# Customer Support Chatbot

This project provides a customer support chatbot with both a command-line interface (CLI) and a graphical user interface (GUI). The bot is designed to handle various customer inquiries, including managing service plans, reporting issues, filing complaints, providing feedback, and answering frequently asked questions.

### Features

* **Natural Language Processing (NLP)**: Utilizes NLTK for tokenization and part-of-speech tagging to understand user queries.
* **Conversation Management**: Manages conversation flow, identifying user intent based on keywords.
* **Database Integration**: Interacts with a MySQL database to store and retrieve customer information, service requests, complaints, and feedback.
* **Service Request Handling**: Allows users to:
    * Upgrade or downgrade their service plans.
    * Cancel subscriptions.
    * Report various types of issues (billing, technical, delivery).
    * Cancel existing complaints.
* **Complaint and Feedback System**:
    * Users can file formal complaints, which are assigned ticket numbers.
    * Users can provide feedback, potentially closing active complaints.
    * Users can track the status of their reported issues or complaints.
* **FAQ Integration**: Provides predefined answers for common queries like contact information and working hours.
* **User Interface Options**:
    * **CLI**: A text-based interface for interacting with the bot.
    * **GUI**: A modern, interactive graphical interface built with Tkinter, featuring chat bubbles for a user-friendly experience.
* **Concurrency**: The GUI version uses threading to run the bot logic in a separate thread, ensuring the UI remains responsive.
* **Logging**: All significant interactions and database operations are logged to a file for auditing and debugging.

### Components

The project is structured into the following Python files:

* `supportbotgui.py`: Implements the graphical user interface using `tkinter`. It manages the display of chat messages, user input, and communicates with the bot's core logic via queues.
* `supportbot.py`: Contains the core NLP and conversational logic. It processes user input, identifies intents using keywords, and orchestrates interactions with the database. It also defines responses and manages the state of the conversation.
* `supportbotdb.py`: Handles all database operations, connecting to MySQL, managing customer data, service plans, issues, complaints, and feedback. It includes functions for logging database interactions.
* `logindb.py`:  This file handles user authentication and initial login procedures for the bot.
