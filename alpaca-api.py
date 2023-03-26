from peft import PeftModel
from transformers import LLaMATokenizer, LLaMAForCausalLM, GenerationConfig
import textwrap
import re
import flask
from IPython import get_ipython
import json
from flask import Flask, jsonify, request
app = Flask(__name__)

tokenizer = LLaMATokenizer.from_pretrained("decapoda-research/llama-7b-hf")

model = LLaMAForCausalLM.from_pretrained(
    "decapoda-research/llama-7b-hf",
    load_in_8bit=True,
    device_map="auto",
)
model = PeftModel.from_pretrained(model, "samwit/alpaca7B-lora")

def alpaca_talk(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
    )
    input_ids = inputs["input_ids"].cuda()

    generation_config = GenerationConfig(
        temperature=0.6,
        top_p=0.95,
        repetition_penalty=1.2,
    )
    print("Generating...")
    generation_output = model.generate(
        input_ids=input_ids,
        generation_config=generation_config,
        return_dict_in_generate=True,
        output_scores=True,
        max_new_tokens=256,
    )
    response = []
    for s in generation_output.sequences:
        print(tokenizer.decode(s))
        response.append(tokenizer.decode(s))
    r = ''.join(response)
    #return r[r.index('Response:\n')+10:]
    return clean_output(r, text)

def clean_output(r, text):
	rclean = re.sub('\n### Response:\n', '', r)
	rclean = rclean.strip()
	rclean = rclean.removeprefix(text.strip())
	# print('prefix: ', text, ' response: ', rclean)

	return rclean

@app.route('/')
def index():
	return jsonify({'App':'OK'})

@app.route('/ask', methods=['POST'])
def ask():
    base_input = """You are an AI assistant named AlpacaAI.
AlpacaAI is honest, kind, helpful, friendly and never fails to answer requests immediately and with details and precision.

Your job is to reply to the following question:
"""

    input_text = json.loads(request.data)
    if (input_text['input']):
        res = alpaca_talk(base_input + input_text['input'])
        
        return jsonify(prompt=input_text['input'], result=res)
        #return jsonify(prompt=res.split('\n')[1], result=res.split('\n')[2])
    else:
        return jsonify(error="No input field was specified.")

if __name__ == '__main__':
	app.run()
