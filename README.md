# alpaca-api

## What is it
This is a simple API that prompts [Stanford's Alpaca7B](https://github.com/tatsu-lab/stanford_alpaca), a fine-tuned version of [Meta's LLaMa 7B](https://huggingface.co/decapoda-research/llama-7b-hf), and gives back the response.
It's designed to run on Colab.

## How to use it
Open the notebook on Colab.
Execute each cell. The last cell will take a couple of minutes. Once everything is done, copy the ngrok link that has been generated.

To prompt the language model, send a json POST request to the /ask endpoint, including a json structured like this:
```
{"input":"<your prompt>"}
```

A quick command to test it is 
```
curl -H "Content-Type: application/json" -X POST -d "{\"input\":\"What are Large Language Models?\"}" <your_ngrok_link>/ask
```
