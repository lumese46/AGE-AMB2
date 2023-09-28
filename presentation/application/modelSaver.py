import os
from .codeGenerator import codeGenerator
def save_to_model(content, file_name='model.py'):
    
    # Get the current working directory (assuming your application folder is the working directory)
    current_directory = os.getcwd()

    # Define the path to the model file relative to the "data" folder
    model_file_path = os.path.join(current_directory, 'data', file_name)
    try:
        with open(model_file_path, 'w') as file:
            file.write(content)
        print(f'Successfully saved to {model_file_path}')
    except Exception as e:
        print(f'Error: {str(e)}')



# Create an instance of CodeGenerator
#code = codeGenerator()

# Call the method on the instance
#codeString = code.generateComponent()

#print(codeString)  # Save to default file path "model.py"

