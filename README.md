# chatgpt_dictionary
Ask ChatGPT to give a word's definition &amp; etymology and give examples.
# Directions:
1. Create a virutal environment

     python3 -m venv venv
     source venv/bin/activate

     pip install openai flask

2. Go to this site, request a key

     https://platform.openai.com/account/api-keys 

3. Put the key into an environment variable called "CHAT_API_KEY":

     export CHAT_API_KEY="<your key here>"

4. Run the python code to create a server

     python <this filename>

5. Open a web browser at

     localhost:5001

 
See this tutorial for more

     https://levelup.gitconnected.com/interfacing-chatgpt-with-python-824be63dfa2f

 Cool features of the API
     https://platform.openai.com/docs/api-reference/completions/create?lang=python
