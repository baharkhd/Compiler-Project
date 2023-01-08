

TEST_CASE_NUM = input()
PRED_TABLE_PATH = 'my_results/symbol_table.txt'
TRUE_TABLE_PATH = 'testcases_phase1_v2/T{}/symbol_table.txt'.format(TEST_CASE_NUM)

pred_symbols = []
true_symbols = []

with open(PRED_TABLE_PATH) as file:
    lines = [line.rstrip() for line in file]
    pred_symbols = [line.split('\t')[1] for line in lines]

with open(TRUE_TABLE_PATH) as file:
    lines = [line.rstrip() for line in file]
    true_symbols = [line.split('\t')[1] for line in lines]

pred_symbols = set(pred_symbols)
true_symbols = set(true_symbols)

print(pred_symbols == true_symbols)