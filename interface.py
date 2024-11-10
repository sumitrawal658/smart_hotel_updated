import gradio as gr
import requests
import json
import openai  # Add this import

# Azure OpenAI settings
azure_endpoint = "https://gpt-candidate-test.openai.azure.com/"
api_key = "4jcVWz6srd4Y7INprd7cpXGvodoPprnYd3cO3vC920sRWrXSCbvKJQQJ99AKACYeBjFXJ3w3AAABACOGBqy1"
assistant_id = "asst_7y4JlZnzk3Agv6zvFTCEhj1Q"


# Configure OpenAI for Azure
openai.api_type = "azure"
openai.api_base = azure_endpoint
openai.api_key = api_key
openai.api_version = "2023-05-15" 
# Headers for Azure OpenAI API
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Function to connect with Azure OpenAI's GPT model
def get_gpt_response(user_input):
    try:
        # Call the Azure OpenAI API endpoint
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )

        # Convert response to JSON format if needed
        response_json = response  # Azure OpenAI API might directly return JSON

        # Check if 'choices' is in the response
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["message"]["content"]
        else:
            # If 'choices' is missing or empty, return an error message
            return "Error: Unexpected API response structure - 'choices' not found"
    
    except Exception as e:
        # Catch any other exceptions and return a user-friendly error message
        print(f"An error occurred: {e}")  # For debugging purposes
        return f"Error: {str(e)}"


# Function to handle IoT interactions based on user input
def interact_with_iot(user_input):
    gpt_response = get_gpt_response(user_input)
    
    # Basic logic for controlling IoT devices based on user input
    if "turn on" in user_input.lower():
        # Placeholder: Replace with real IoT control logic
        return f"{gpt_response} - Command received: Turning on the device."
    elif "temperature" in user_input.lower():
        # Retrieve IoT sensor data
        # Placeholder: Replace with real data retrieval code
        return f"{gpt_response} - Room temperature is set to 22°C."
    else:
        return f"{gpt_response} - Sorry, I did not understand the command."

# Define Gradio interface
def gradio_interface(user_input):
    return interact_with_iot(user_input)

iface = gr.Interface(fn=gradio_interface, inputs="text", outputs="text", title="Smart Hotel Assistant")
