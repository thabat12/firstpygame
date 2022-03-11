import pandas as pd
import random

def to_tsv(arr, file_path):
    with open(file_path, 'w', encoding='UTF8', newline='') as file:
        for a in arr:
            for i in a[:-1]:
                file.write(str(i) + '\t')
            file.write(str(a[-1])+'\n')

def from_tsv(file_path):
    df = pd.read_csv(file_path, sep='\t', header=None)
    pd.set_option('display.max_rows', None)
    print(df.to_string())



sample_arr = [[random.randint(0,1) for _ in range(10)] for _ in range(10)]
to_tsv(sample_arr, 'sample.tsv')
