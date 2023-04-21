import json
import os
from tqdm import tqdm
from infer_chatgpt import infer_chatgpt

def infer_test_cases_with_chatgpt():
    with open("../data/dataset/HumanEval_for_test_case_generation.jsonl", 'r') as f:
        dataset = [json.loads(line) for line in f.readlines()]

    with open("../data/generated_data/chatgpt_temp0.8_topp0.95_num_100_test_case.jsonl", 'w') as f:
        for i, data in tqdm(enumerate(dataset)):
            prompt = data['prompt']
            answers = infer_chatgpt(prompt, answer_num=100)
            f.write(json.dumps({"prompt": prompt, "samples": answers}) + '\n')

def infer_code_generation_with_chatgpt():
    with open("../data/dataset/HumanEval_for_code_generation.jsonl", 'r') as f:
        dataset = [json.loads(line) for line in f.readlines()]

    with open("../data/generated_data/chatgpt_temp0.8_topp0.95_num_200_code_solution.jsonl", 'w') as f:
        for i, data in tqdm(enumerate(dataset)):
            prompt = data['prompt']
            answers = infer_chatgpt(prompt, answer_num=100)
            answers += infer_chatgpt(prompt, answer_num=100)
            f.write(json.dumps({"prompt": prompt, "samples": answers}) + '\n')
    





if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    infer_test_cases_with_chatgpt()
    infer_code_generation_with_chatgpt()

