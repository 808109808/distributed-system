# Import necessary libraries and modules for XMLRPC server and data manipulation.
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import xml.etree.ElementTree as ET
import datetime
import requests
import threading

# Define a threaded version of the XMLRPC server to handle requests concurrently.
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# Initialize an XML database to store notes.
def init_xml_db():
    root = ET.Element("notes")
    tree = ET.ElementTree(root)
    tree.write("db.xml")

# Fetches summary information from Wikipedia using the OpenSearch protocol.
def fetch_from_wikipedia(topic):
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    
    # Setup parameters for OpenSearch API request.
    search_params = {
        "action": "opensearch",
        "search": topic,
        "limit": "1",
        "namespace": "0",
        "format": "json"
    }
    search_response = session.get(url=url, params=search_params)
    search_data = search_response.json()

    # Check if data is available; if not, return a default message.
    if not search_data or len(search_data) < 3 or not search_data[3]:
        return "No additional information found"
    
    # Extract page title and URL from search data.
    page_title = search_data[1][0] if search_data[1] else ""
    page_url = search_data[3][0] if search_data[3] else ""

    # Setup parameters for detailed page query.
    query_params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
    }
    query_response = session.get(url=url, params=query_params)
    query_data = query_response.json()
    
    # Extract summary information from query response.
    page_id = next(iter(query_data['query']['pages']))
    summary = query_data['query']['pages'][page_id]['extract'] if page_id else "Summary not available."

    return f"Title: {page_title}\nURL: {page_url}\nSummary: {summary}"

# Thread lock for file operations to ensure thread safety.
file_lock = threading.Lock()

# Adds or updates a note with optional Wikipedia content.
def add_or_update_note_with_wiki(topic, text, include_wiki=False):
    with file_lock: 
        try:
            tree = ET.parse('db.xml')
            root = tree.getroot()
        except Exception:
            # Initialize XML database if it does not exist.
            init_xml_db()
            tree = ET.parse('db.xml')
            root = tree.getroot()

        # Append Wikipedia content to note if requested.
        wikipedia_content = ""
        if include_wiki:
            wikipedia_content = fetch_from_wikipedia(topic)
            text += f"\nWikipedia Link: {wikipedia_content}"

        # Add new note or update existing one in the XML structure.
        note_found = False
        for note in root.findall('note'):
            if note.find('topic').text == topic:
                note_found = True
                new_entry = ET.SubElement(note, "entry")
                new_entry.text = text
                new_entry.set('timestamp', str(datetime.datetime.now()))
                break

        if not note_found:
            new_note = ET.SubElement(root, "note")
            new_topic = ET.SubElement(new_note, "topic")
            new_topic.text = topic
            new_entry = ET.SubElement(new_note, "entry")
            new_entry.text = text
            new_entry.set('timestamp', str(datetime.datetime.now()))

        # Write the updated XML data back to the file.
        tree.write('db.xml')
        return "Note added or updated successfully."

# Retrieve notes by topic from the XML database.
def get_notes_by_topic(topic):
    with file_lock: 
        notes_content = []
        try:
            tree = ET.parse('db.xml')
            root = tree.getroot()
            # Iterate through notes and collect entries matching the topic.
            for note in root.findall('note'):
                if note.find('topic').text == topic:
                    entries = note.findall('entry')
                    for entry in entries:
                        notes_content.append((entry.text, entry.get('timestamp')))
        except Exception as e:
            return str(e)
        return notes_content

# Set up and start the XMLRPC server.
server = ThreadedXMLRPCServer(("localhost", 8000), allow_none=True)
print("Listening on port 8000...")

# Register functions to make them callable via XMLRPC.
server.register_function(add_or_update_note_with_wiki, "add_or_update_note_with_wiki")
server.register_function(get_notes_by_topic, "get_notes_by_topic")

# Run the server indefinitely.
server.serve_forever()
