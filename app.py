# coding: utf-8
from flask import Flask, request, render_template, Markup
import os
import openai
import markdown

#model_name = "gpt-4"
#model_name="gpt-3.5-turbo"

openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__, static_folder='./static', static_url_path='')

@app.route('/demo')
def hello_world():
    return "<p>Hello World!</p>"

@app.route('/')
def index():
    #return app.send_static_file('index.html')
    #return render_template('index.html',model=model_name)
    return render_template('index.html')

@app.route('/answer', methods=['post'])
def answer():

    """
    # Using text-davinci-003
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
        res=response.choices[0].text
        return render_template('answer.html',res=res)
    # -- end of text-davinci-003 -- #
    """
    # Using gpt
    content = request.form.get('prompt')
    model_name = request.form.get('model')
    try:
        response = openai.ChatCompletion.create(
          model=model_name,
          messages=[
            {"role": "system", "content": content}
          ]
        )
        configs = {
            'codehilite':{
                'noclasses': True
            }
        }

        res=response.choices[0].message.content
        html = Markup(markdown.markdown(res, extensions=['fenced_code','codehilite'], extension_configs=configs))
        return render_template('answer.html',res=html)
    # -- end of gpt -- #

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
    except openai.error.InvalidRequestError as e:
      print(f"OpenAI API InvalidRequestError: {e}")
      res=f"OpenAI API InvalidRequestError: {e}"
      return render_template('error.html',res=res)
      pass
    except openai.error.RateLimitError as e:
      #Handle rate limit error (we recommend using exponential backoff)
      print(f"OpenAI API request exceeded rate limit: {e}")
      res=f"OpenAI API request exceeded rate limit: {e}"
      return render_template('error.html',res=res)
      pass

app.run(host='0.0.0.0', port=8000, debug=True)
