# distributed-system
just a student assignment2 for distributed system

 `client.py`:
- Imports and Server Proxy: This script starts by importing the `xmlrpc.client` library and setting up a proxy for communicating with the server located at 'http://localhost:8000'.
  
- add_note Function: This function asks the user for a note's topic, text, and whether they want to fetch related information from Wikipedia. It then sends these details to the server and prints the server's response.

- search_note Function: This function prompts the user to enter a topic to search for within the notes. It requests the data from the server and prints each note found, including its text and timestamp.

- main_menu Function: This provides a text-based menu for the user, allowing them to add a new note, search for existing notes, or exit the program. It navigates according to the user's choice.

- Program Entry Point: The `if __name__ == "__main__":` block starts the application by calling the `main_menu` function.

 `server.py`:
- Imports and Server Setup: This script imports necessary modules for XML-RPC server functionality, XML manipulation, datetime operations, making HTTP requests, and threading. It defines a `ThreadedXMLRPCServer` class that can handle multiple client requests simultaneously by extending `SimpleXMLRPCServer` with threading capabilities.

- init_xml_db Function: Initializes an XML file to serve as a simple database for storing notes if one does not already exist.

- fetch_from_wikipedia Function: Fetches a summary, title, and URL for a given topic from Wikipedia using the OpenSearch protocol. It processes and returns this data, or an error message if the topic is not found or an issue occurs.

- Thread Lock: A thread lock (mutex) is used to prevent simultaneous write operations on the XML database by multiple threads, ensuring data integrity.

- add_or_update_note_with_wiki Function: Adds a new note to the XML database or updates an existing one. If requested, it appends Wikipedia information related to the note's topic. This function handles reading and writing to the XML file with thread safety.

- get_notes_by_topic Function: Searches the XML database for notes matching a specific topic and returns them. It ensures thread safety using the mutex during read operations.

- Server Initialization and Function Registration: Initializes the XML-RPC server to listen on localhost at port 8000 and registers the functions `add_or_update_note_with_wiki` and `get_notes_by_topic` so they can be called remotely.

- Server Loop: Starts the server and keeps it running indefinitely to listen for and respond to client requests.

The entire system allows multiple clients to add, update, and search notes concurrently, with optional integration of Wikipedia information for enhanced note content.
