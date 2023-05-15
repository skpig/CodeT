import json
import ast
import os
import pickle
import random

def convert(data_type):
    with open(f"../data/generated_data/HumanEval_codegen16B_temp0.8_topp0.95_num100_max300_test_case.jsonl", 'r') as f:
        s1 = json.loads(f.readline())
    with open(f"../data/generated_data/HumanEval_codegen16B_temp0.8_topp0.95_num100_max300_code_solution.jsonl", 'r') as f:
        s2 = json.loads(f.readline())
    with open(f"./{data_type}/original_dataset.jsonl", 'r') as f:
        origin_dataset = [json.loads(line) for line in f.readlines()]

    # convert test_case
    with open(f"./{data_type}/test_cases.pkl", "rb") as f:
        tc_dataset = pickle.load(f)
    with open(f"./{data_type}/test_cases_in_codet_format.jsonl",'w') as f:
        for sample in tc_dataset:
            task_id = sample['task_id'].split('/')[-1]
            entry_point = origin_dataset[int(task_id)]['entry_point']
            # determine whether is multi_args
            if data_type == "CodeContests":
                multi_args = False
            else:
                ast_tree = ast.parse(sample["prompt"])
                for body in ast_tree.body:
                    if isinstance(body, ast.FunctionDef) and body.name == entry_point:
                        multi_args = len(body.args.args) > 1
                        break

            test_cases = []
            for i, test_case in enumerate(sample['test_cases']):
                if 'output' not in test_case or 'input' not in test_case:
                    continue
                input_str = test_case['input']
                output_str = test_case['output']
                if type(test_case['input']) == str:
                    input_str = f"'{test_case['input']}'"
                if type(test_case['output']) == str:
                    output_str = f"'{test_case['output']}'"

                if multi_args:
                    assert_str = f'assert {entry_point}(*{input_str}) == {output_str}'
                else:
                    assert_str = f'assert {entry_point}({input_str}) == {output_str}'
                test_cases.append(assert_str)
            f.write(json.dumps({'prompt': sample['prompt'],
                                'samples': test_cases}) + '\n')

    # convert code_solution
    with open(f"./{data_type}/solutions.jsonl", "r") as f:
        cs_dataset = [json.loads(line) for line in f.readlines()]
    with open(f"./{data_type}/code_solution_in_codet_format.jsonl",'w') as f:
        for sample in cs_dataset:
            f.write(json.dumps({'prompt': sample['prompt'],
                                'samples': sample['completions']}) + '\n')


        

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for data_type in ['human_eval', 'CodeContests']:
        convert(data_type)