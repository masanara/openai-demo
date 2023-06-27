# coding: utf-8
from flask import Flask, request, render_template
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder='./static', static_url_path='')

@app.route('/demo')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/')
def index():
    return app.send_static_file('index.html')
    #return "hi"

@app.route('/answer', methods=['post'])
def answer():
    prompt = request.form.get('prompt')
    try:
        response = openai.Completion.create(
          model="text-davinci-003",
          #model="gpt-3.5-turbo",
          prompt=prompt,
          temperature=0,
          max_tokens=3000,
          top_p=1,
          frequency_penalty=0.0,
          presence_penalty=0.0,
          #stop=["\n"]
        )
        #print(response.choices[0].text) 
        res=response.choices[0].text
        return render_template('answer.html',res=res)
    except openai.error.APIError as e:
      #Handle API error here, e.g. retry or log
      print(f"OpenAI API returned an API Error: {e}")
      res=f"OpenAI API returned an API Error: {e}"
      return render_template('error.html',res=res)
      pass
    except openai.error.APIConnectionError as e:
      #Handle connection error here
      print(f"Failed to connect to OpenAI API: {e}")
      res=f"Failed to connect to OpenAI API: {e}"
      return render_template('error.html',res=res)
      pass
    except openai.error.RateLimitError as e:
      #Handle rate limit error (we recommend using exponential backoff)
      print(f"OpenAI API request exceeded rate limit: {e}")
      res=f"OpenAI API request exceeded rate limit: {e}"
      return render_template('error.html',res=res)
      pass

app.run(host='0.0.0.0', port=8000, debug=True)
