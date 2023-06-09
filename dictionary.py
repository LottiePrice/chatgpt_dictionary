from flask import Flask, render_template_string, request, render_template
import openai
import json
import os
from setup import chat_model


openai.api_key = os.environ.get("OPENAI_API_KEY")

models = openai.Model.list()
model_names = [model['id'] for model in models['data']]
print(model_names)

model = chat_model

prompt_part_a = """Here is a word or phrase, contained in angle brackets: <{}>. """
prompt_part_b1 = """Here is an example usage: <{}>. Focus on the definition that best fits this usage and ignore other definitions. """
prompt_part_b2 = """Use the primary definition of the word. """
prompt_part_c = """Return the definition as a python dictionary with this list of keys: ["word or phrase", "etymology", "definition", "examples", "connotation"]. If the value of any field is unknown, return a value of "unknown" for that field.  The "definition" field should be less than 5 sentences long. The "examples" field should be a list of at most 2 strings containing sentences. The "connotation" field should have one of the values from this list: ["positive", "negative", "neutral"].
"""

app = Flask(__name__)

history=[]

def build_query(word, usage):
   prompt = prompt_part_a.format(word)
   if usage is None:
      prompt = prompt + prompt_part_b2
   else:
      prompt = prompt + prompt_part_b1

   prompt = prompt + prompt_part_c
   return prompt
	
@app.route('/',methods=['GET', 'POST'])
def home():

    global history

    if request.method == 'POST':

        word_text = request.form['word']
        context_text = request.form['context']

        query = build_query(word_text, context_text)


        print( "-------------------------")
        print( f"Sending query: ")
        print( "-------------------------")
        print( f"{query}")

        completion =  openai.ChatCompletion.create(
                    model=model,
                    messages = [{ "role": "user", 
                                  "content": query }],
                    max_tokens = 1024,
                    temperature = 0.8)

        generated_text = completion.choices[0].message.content

    else:
    
        form_text=""
        generated_text = """{ "word or phrase" : "",
                              "etymology" : "",
                              "definition" : "",
                              "connotation" : "",
                              "examples" : "" }"""

    try:

        response_as_dict = json.loads(generated_text)


        print( "-------------------------")
        print( "Response")
        print( "-------------------------")
        print(response_as_dict)
        
        """
        history =   history + "\n" \
                  + "JUAN:  " + response_as_dict["declaración"] + "\n" \
                  + "MARIA: " + response_as_dict["respuesta"] + "\n"

        if len(history) > 500:
            history = history[-500:]
        """

        return render_template('dictionary_interface.html', 
            word = response_as_dict["word or phrase"],
            etymology = response_as_dict["etymology"],
            definition = response_as_dict["definition"], 
            connotation = response_as_dict["connotation"], 
            examples = response_as_dict["examples"],text="")

    except:

        print(  '\033[91m' )
        print( "-------------------------")
        print( "Exception on returned text")
        print( "-------------------------")
        print( generated_text)
        print(  '\033[0m' )

        raise Exception("Error thrown during parse of return text from chat-gpt")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
