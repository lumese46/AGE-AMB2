import json
import os

def json_load(name_of_jason):
    # Get the current working directory (assuming your application folder is the working directory)
    current_directory = os.getcwd()

    # Define the path to the JSON file relative to the "data" folder
    json_file_path = os.path.join(current_directory, 'data', name_of_jason)

    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data


# for obj in data:
#     name_of_component = obj.get("Name_of_component")
#     component_attributes = obj.get("Component_atributes", [])

#     print("Name_of_component:", name_of_component)
#     print("Component_attributes:")
#     for attribute in component_attributes:
#         print(f"  Name: {attribute['name']}")
#         print(f"  Default Value: {attribute['DefaultValue']}")
#         print(f"  Description: {attribute['Description']}")
#     print()







