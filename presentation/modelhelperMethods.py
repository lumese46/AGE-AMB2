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