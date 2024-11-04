from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    # Connect to MongoDB
    client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.3")

    # Attempt to retrieve server information as a connectivity test
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")

    # Optionally, list all databases as an additional check
    databases = client.list_database_names()
    print("Available databases:", databases)

except ConnectionFailure as e:
    print("Could not connect to MongoDB:", e)

# Create the database and collection if they don't already exist
db = client["practical"]
collection = db["Sample"]

def add_document(data):
    """Add a document to the collection, ensuring no duplicates."""
    try:
        # Check if a document with the same 'name' and 'city' already exists
        existing_document = collection.find_one({"name": data["name"], "city": data["city"]})
        if existing_document:
            print("Duplicate document found. No new document added.")
        else:
            result = collection.insert_one(data)
            print(f"Document added with id: {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred while adding the document: {e}")

def delete_document(query):
    """Delete a document matching the query."""
    try:
        result = collection.delete_one(query)
        if result.deleted_count > 0:
            print("Document deleted.")
        else:
            print("No document found matching the query.")
    except Exception as e:
        print(f"An error occurred while deleting the document: {e}")

def update_document(query, new_values):
    """Update a document matching the query."""
    try:
        result = collection.update_one(query, {"$set": new_values})
        if result.modified_count > 0:
            print("Document updated.")
        else:
            print("No document found matching the query.")
    except Exception as e:
        print(f"An error occurred while updating the document: {e}")

def show_all_documents():
    """Show all documents in the collection."""
    try:
        documents = collection.find()
        for doc in documents:
            print(doc)
    except Exception as e:
        print(f"An error occurred while showing documents: {e}")

# Example usage
if __name__ == "__main__":
    # Adding documents
    add_document({"name": "Alice", "age": 25, "city": "New York"})
    add_document({"name": "ankur", "age": 20, "city": "York"})
    add_document({"name": "sachin", "age": 15, "city": "New"})

    # Attempting to add a duplicate document
    add_document({"name": "Alice", "age": 25, "city": "New York"})

    # Showing all documents
    print("All documents:")
    show_all_documents()

    # Updating a document
    update_document({"name": "Alice"}, {"age": 26})

    # Deleting a document
    delete_document({"name": "Alice"})

    # Showing all documents after deletion
    print("All documents after deletion:")
    show_all_documents()

    # Close the MongoDB connection
    client.close()


# use practical;

# db.createCollection("Sample");
# db.Sample.find();

