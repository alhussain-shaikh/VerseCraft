from flask import Flask, render_template, request
import openai
from googletrans import Translator

app = Flask(__name__)

# Initialize the OpenAI API with your key
openai.api_key = 'give api key'  # Please replace with your actual OpenAI API key

def generate_poem(prompt, language):
    # Translate the prompt to the desired language
    translated_prompt = translate_prompt_to_language(prompt, language)

    try:
        # Generate the poem using the GPT-3 API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": translated_prompt}
            ]
        )

        # Extract and return the poem from the response
        return response['choices'][0]['message']['content']

    except openai.error.RateLimitError:
        return " "

def translate_prompt_to_language(prompt, language):
    # Initialize the translator
    translator = Translator()

    # Translate the prompt to the desired language
    translation = translator.translate(prompt, dest=language)

    # Return the translated text
    return translation.text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        language = request.form['language']
        poem = generate_poem(prompt, language)
        return render_template('index.html', poem=poem)
    return render_template('index.html', poem="")

if __name__ == '__main__':
    app.debug = True
    app.run()
