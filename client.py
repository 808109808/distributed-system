# Import the XML-RPC client library and create a server proxy for local communication.
import xmlrpc.client
s = xmlrpc.client.ServerProxy('http://localhost:8000')

# Function to add a new note with optional Wikipedia information.
def add_note():
    topic = input("Enter topic: ")
    text = input("Enter text: ")
    wiki_option = input("Fetch data from Wikipedia? (yes/no): ").lower()
    include_wiki = wiki_option == 'yes'
    print(s.add_or_update_note_with_wiki(topic, text, include_wiki))

# Function to search and display notes based on a topic.
def search_note():
    topic = input("Enter topic to retrieve: ")
    notes = s.get_notes_by_topic(topic)
    if notes:
        for note in notes:
            print(f"Text: {note[0]}, Timestamp: {note[1]}")
    else:
        print("No notes found")

# Main menu function to navigate through the application.
def main_menu():
    while True:
        print("\n1. Add note")
        print("2. Search note")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            add_note()
        elif choice == '2':
            search_note()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid input, please try again.")

# Entry point of the program, invoking the main menu.
if __name__ == "__main__":
    main_menu()
