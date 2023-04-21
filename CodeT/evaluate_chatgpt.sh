python main.py \
--source_path_for_solution ./data/dataset/HumanEval_for_code_generation.jsonl \
--predict_path_for_solution ./data/generated_data/chatgpt_temp0.8_topp0.95_num_200_code_solution.jsonl \
--source_path_for_test ./data/dataset/HumanEval_for_test_case_generation.jsonl \
--predict_path_for_test ./data/generated_data/chatgpt_temp0.8_topp0.95_num_100_test_case.jsonl \
--cache_dir .runtime \
--timeout 0.1 \
--test_case_limit 5