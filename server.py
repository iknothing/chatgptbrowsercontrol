from wsgiref.validate import validator
from flask import Flask, request, jsonify
app = Flask(__name__)

# Server configuration
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
OPENAI_MODEL = "text-davinci-002"  # Update with your desired GPT-3 model

def checkifpromptsecure(data):
    # Check if prompt is secure
    # Return True if prompt is secure
    # Return False if prompt is not secure
    #url has to be of type https:// etc
    if not data['url'].startswith('https://'):  
        #append or  change http to https
        data['url'] = 'https://' + data['url']
        #check if url is valid
        if not validator.url(data['url']):
            return False
    #check if browser content is valid
    # if not data['browser_content'].startswith('<html>'):
        # return False
    #check if command is valid
    if not data['command'].startswith("You are an agent controlling a browser. You are given:(1) an objective that you are trying to achieve(2) the URL of your current web page(3) a simplified text description of what's visible in the browser window (more on that below)"):
        return False
    else:
        return True

@app.route("/process_request", methods=["POST"])
def process_request():
    data = request.json

    if not checkifpromptsecure(data):
        return jsonify({"suggested_command": "Error: Invalid prompt"})
    # Construct the prompt using data received from the client
    prompt = f"Command: {data['command']}\n"

    # Send the prompt to OpenAI API
    import openai
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        model=OPENAI_MODEL,
        prompt=prompt,
        temperature=0.5,
        best_of=10,
        max_tokens=50,
        n=3,
    )

    # Extract the suggested command from OpenAI response
    suggested_command = response.choices[0].text.strip()

    return jsonify({"suggested_command": suggested_command})

if __name__ == "__main__":
    app.run(debug=True)
