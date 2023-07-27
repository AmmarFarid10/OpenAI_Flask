from flask import Flask, jsonify, request
import openai

class ChatGPTBotAPI:
    def __init__(self, api_key, engine='text-davinci-002', temperature=0.7, max_tokens=150):
        self.api_key = api_key
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompts = []

    def initialize_gpt3(self):
        openai.api_key = self.api_key

    def create_prompt(self, prompt):
        self.prompts.append(prompt)
        return len(self.prompts) - 1

    def get_response(self, prompt_index):
        if prompt_index >= len(self.prompts) or prompt_index < 0:
            return "Invalid prompt index."
        
        prompt = self.prompts[prompt_index]
        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response['choices'][0]['text']

    def update_prompt(self, prompt_index, new_prompt):
        if prompt_index >= len(self.prompts) or prompt_index < 0:
            return "Invalid prompt index."

        self.prompts[prompt_index] = new_prompt
        return "Prompt updated successfully."

    def delete_prompt(self, prompt_index):
        if prompt_index >= len(self.prompts) or prompt_index < 0:
            return "Invalid prompt index."

        del self.prompts[prompt_index]
        return "Prompt deleted successfully."


# Create Flask app and ChatGPT Bot instance
app = Flask(__name__)
chatbot = ChatGPTBotAPI(api_key='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')

# Initialize the ChatGPT Bot with OpenAI API
chatbot.initialize_gpt3()

@app.route('/create_prompt', methods=['POST'])
def create_prompt():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"message": "Prompt is missing."}), 400

    prompt_index = chatbot.create_prompt(prompt)
    return jsonify({"message": "Prompt created successfully.", "prompt_index": prompt_index}), 201

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    prompt_index = data.get('prompt_index')
    if prompt_index is None:
        return jsonify({"message": "Prompt index is missing."}), 400

    response = chatbot.get_response(prompt_index)
    return jsonify({"response": response}), 200

@app.route('/update_prompt', methods=['PUT'])
def update_prompt():
    data = request.get_json()
    prompt_index = data.get('prompt_index')
    new_prompt = data.get('new_prompt')

    if prompt_index is None or new_prompt is None:
        return jsonify({"message": "Prompt index or new prompt is missing."}), 400

    result = chatbot.update_prompt(prompt_index, new_prompt)
    return jsonify({"message": result}), 200

@app.route('/delete_prompt', methods=['DELETE'])
def delete_prompt():
    data = request.get_json()
    prompt_index = data.get('prompt_index')

    if prompt_index is None:
        return jsonify({"message": "Prompt index is missing."}), 400

    result = chatbot.delete_prompt(prompt_index)
    return jsonify({"message": result}), 200

if __name__ == '__main__':
    app.run(debug=True)
