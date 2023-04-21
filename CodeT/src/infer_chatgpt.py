import openai
import os
import json
from tqdm import tqdm
import time
import re

openai.api_type = "azure"
openai.api_base = "https://yaobo.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("")
openai.api_key = "f2b8dd24042242aea57e5c5b194efef0"

def query_openai_api(query, model='text-davinci-003', max_tokens=2048, choice_num=5, verbose=False):
    if verbose:
        print("the prompt to model:")
        print(query)
    if model == 'text-davinci-003' or model == 'text3':
        response = openai.Completion.create(
            engine="text3",
            prompt=query,
            temperature=0,
            max_tokens=1500)
        if verbose:
            print('response:', response)
        return response["choices"][0]["text"]
    elif model == 'chatgpt':
        response = openai.Completion.create(
            engine="gpt-35-turbo",
            prompt=query,
            temperature=0.8,
            max_tokens=max_tokens,
            top_p=0.95,
            n=choice_num,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["<|im_end|>", "¬Human¬"])
        if verbose:
            print('response:', response)
        return [x["text"]  for x in response["choices"] if x['finish_reason'] != 'length']


def infer_chatgpt(instruction, 
                  max_tokens=2048,
                  answer_num=5):
                  
    """
    Args:
        instruction: str
    Returns:
        answers: list of str
    """

    opener_prompt = f"""
<|im_start|>system
You are a helpful AI to complete python codes provided by user. You only reply with the code completion. You won't say anything else.
<|im_end|>
<|im_start|>user
{instruction}
<|im_end|>
<|im_start|>assistant
"""

    retry_times = 0
    while True:
        time.sleep(1)
        try:
            answers = query_openai_api(opener_prompt, model='chatgpt', max_tokens=max_tokens, choice_num=answer_num)
            return answers
        except Exception as e:
            # print(e)
            sleep_time = re.findall(r'Please retry after (\d+) seconds.', e.user_message)
            if not sleep_time:
                time.sleep(10)
            else:
                time.sleep(int(sleep_time[0]))
            retry_times += 1

def infer_chatgpt2(instruction, exemplars, query, answer_num=5):
    """
    Args:
        instruction: str
        exemplars: list of dict {"query": str, "answer": str}
        query: str
    Returns:
        answers: list of str
    """
    messages = [{"role": "system", "content": "You are a helpful AI."},
                {"role": "user", "content": instruction},
                {"role": "assistant", "content": "OK, I'm ready to help."},
        ]
    
    for i, exemplar in enumerate(exemplars):
        messages.append({"role": "user", "content": exemplar['query']})
        messages.append({"role": "assistant", "content": exemplar['answer']})
    
    messages.append({"role": "user", "content": query})
    print(1)

    answers = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        engine="chatgpt",
        messages=messages,
        temperature=0.8,
        max_tokens=2048,
        top_p=0.9,
        n=5,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["<|im_end|>", "¬Human¬"])

    return answers

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))