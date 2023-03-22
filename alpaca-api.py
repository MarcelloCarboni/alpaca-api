from peft import PeftModel
from transformers import LLaMATokenizer, LLaMAForCausalLM, GenerationConfig
import textwrap

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
    r = ''.join(response)
    print(r)
    return r[r.index('Response:\n')+10:]

@app.route('/')
def index():
	return jsonify({'App':'OK'})

@app.route('/ask', methods=['POST'])
def ask():
    input_text = json.loads(request.data)
    if (input_text['input']):
        res = alpaca_talk(input_text['input'])
        
    return jsonify(result=res)

if __name__ == '__main__':
	app.run()
