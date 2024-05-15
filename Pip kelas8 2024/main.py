from flask import Flask, request, jsonify, render_template
import time
from pymongo import MongoClient
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# Replace with your MongoDB connection details
uri = "mongodb+srv://Samuel:ndDpaXnzUCx2GQ7@testcluster.r67ayxa.mongodb.net/?retryWrites=true&w=majority&appName=TestCluster"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Tugas2"]
collection = db["pipkls82024"]

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    #sorted_cursor = cursor.sort("tugasapa", pymongo.ASCENDING)  # Sort in ascending order
    #for document in sorted_cursor:
        #tugasapa = document.get("tugasapa")
        #deadline = document.get("deadline")
        #data_list.append({"tugasapa": tugasapa, "deadline": deadline})

    # Combine data into a single variable (consider structure and use case)
    cursor = collection.find()
    data_list = []
    a = 1
    documents = list(collection.find())
    documents1 =str(documents)
    # Process the documents (same as loop approach)
    #for document in cursor:
        #TugasID = document.get('_id')
        #target_id = a
        
        #exists = collection.find_one({target_id:True})
        #if exists:
            #data_list.append(a + ":")
            #data_list.append(str(TugasID))
        #else:
            #print("ID does not exist in the database.")
        #data_list.append({"tugasapa": tugasapa, "deadline": deadline})
        #data_list.append(str(a) + ":")
        #data_list.append("{Tugas:"+ str(tugasapa))
        #data_list.append("Kumpul:"+ str(deadline) + "}")
        #a += 1
    return render_template('mainht.html', documents1=documents1)
b = 1

@app.route("/submit", methods=["POST"])
def submit_data():
    if request.method == "POST":
        try:
            tugasapa = request.form.get("tugasapa")  # Access form data
            deadline = request.form.get("deadline")
            #Create the JSON data
            current_time_perf_counter = time.perf_counter()
            current_time_milliseconds = current_time_perf_counter * 1000
            current_time_milliseconds=str(current_time_milliseconds)
            user_data = {
                current_time_milliseconds:{
                    "tugasapa": tugasapa,
                    "deadline": deadline
                }
            }
                    
            result = collection.insert_one(user_data)

            b=+1
            render_template('mainht.html')
            return jsonify({"message": "Data inserted successfully!", "inserted_id": str(result.inserted_id)}), 201
            
        except (Exception) as e:
            return jsonify({"message": f"Error processing data: {str(e)}"}), 400
            
    else:
        return jsonify({"message": "Invalid request method"}), 405
    
@app.route("/read", methods=["GET"])
def readdata():
    if request.method == "GET":
        cursor = collection.find()
        data_list = []
        debug_list = []
        for document in cursor:
            tugasapa = document.get('tugasapa')
            deadline = document.get('deadline')
            data_list.append({"tugas": tugasapa, "deadline": deadline})
            #debug_list.append(document)

        # Return data after processing all documents
        if data_list:
            return jsonify(data_list), 200  # Success code for data retrieval
        else:
            return jsonify({"message": "No data found in the collection."}), 404  # Not found code for empty data
    else:
        return jsonify({"message": "you tried to do anything other than get :laugh:"}), 405

#BUGGGY AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
@app.route("/remove", methods=["DELETE"])
def remove_data():
    """Removes a document from the collection based on a valid ID provided in the request body (JSON).

    Returns:
        - JSON response with a success message (200) or an error message (400 or 404).
    """

    try:
        # Expect JSON data containing the ID in the request body
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Missing data in request body"}), 400

        remove_id = data.get("_id")
        if remove_id is None:
            return jsonify({"message": "Missing '_id' field in request body"}), 400

        # Validate ID format (optional, consider if you have a specific format)

        # Perform the deletion using the validated ID
        delete_result = collection.delete_one({"_id": remove_id})

        if delete_result.deleted_count == 1:
            return jsonify({"message": "Successfully removed data"}), 200
        else:
            return jsonify({"message": "No document found with the provided ID"}), 404

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred during deletion: {e}")
        return jsonify({"message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)