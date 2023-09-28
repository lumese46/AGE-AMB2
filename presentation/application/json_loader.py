import json
import os
def json_load(fname):
    result = []
    try:
        with open(f"data/{fname}s.json") as jfile: #read old file if it exists
            result = json.load(jfile)
    except:
        with open(f"data/{fname}s.json", "w") as jfile:    #create new file
            pass
    return result

def on_load(name_of_jason):
    # Get the current working directory (assuming your application folder is the working directory)
    current_directory = os.getcwd()

    # Define the path to the JSON file relative to the "data" folder
    json_file_path = os.path.join(current_directory, 'data', name_of_jason)

    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

#print(json_load("component"))







