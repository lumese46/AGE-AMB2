import json
import helperMethods

def add_model_name(model_name):
    name_model = {}
    name_model["name_model"]= model_name
    return name_model
# takes a list called model_input_parameters
def add_input_parameters(model_input_parameters):
    input_parameters = {}
    input_parameters["input_parameters"] = model_input_parameters
    return input_parameters



################# tests cases for all helper methods #####################


modelName = add_model_name("karabo")
helperMethods.add_to_json(modelName, "modelTest2")

modelInputParam = add_input_parameters([
            {
                "name": "seed",
                "dataType": "int"
            },
            {
                "name": "sheep_gain",
                "dataType": "int"
            },
            {
                "name": "sheep_reproduce",
                "dataType": "int"
            }
        ])
helperMethods.add_to_json(modelInputParam, "modelTest2")