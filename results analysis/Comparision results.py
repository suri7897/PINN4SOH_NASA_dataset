'''
Parse the results of the comparative experiment
'''

import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.abspath('../'))
from utils.util import eval_metrix
import matplotlib.pyplot as plt
import scienceplots
plt.style.use('science')
from result_class_for_comparision import Results_NASA, Results_XJTU
import argparse

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument('--dataset', type=str, required=True, choices=['NASA', 'XJTU', 'NASA_dqdv'],
                   help='Choose dataset')
    p.add_argument('--model', type=str, default = 'MLP', choices=['CNN', 'MLP'],
                   help='Choose model to evaluate')
    return p.parse_args()


if __name__ == '__main__':

    args = get_args()

    if args.dataset == 'NASA':
        root = f'../results of reviewer/{args.model}/NASA results/' # "NASA-CNN results" or "NASA-MLP results"
        writer = pd.ExcelWriter(f'../results of reviewer/{args.model}-NASA-results.xlsx')
        batch = 0
        results = Results_NASA(root, gap=0.07)
        for batch in range(1,10):
            if batch == 4 or batch == 6:
                continue
            df_battery_mean = results.get_battery_average(train_batch=batch,test_batch=batch)
            df_experiment_mean = results.get_experiments_mean(test_batch=batch,train_batch=batch)
            df_battery_mean.to_excel(writer,sheet_name='battery_mean_{}'.format(batch),index=False)
            df_experiment_mean.to_excel(writer,sheet_name='experiment_mean_{}'.format(batch),index=False)
        writer.close()
        print(df_experiment_mean.mean(numeric_only=True))

    if args.dataset == 'NASA_dqdv':
        root = f'../results of reviewer/{args.model}/NASA_dqdv results/' # "NASA-CNN results" or "NASA-MLP results"
        writer = pd.ExcelWriter(f'../results of reviewer/{args.model}-NASA_dqdv-results.xlsx')
        batch = 0
        results = Results_NASA(root, gap=0.07)
        for batch in range(1,10):
            if batch == 4 or batch == 6:
                continue
            df_battery_mean = results.get_battery_average(train_batch=batch,test_batch=batch)
            df_experiment_mean = results.get_experiments_mean(test_batch=batch,train_batch=batch)
            df_battery_mean.to_excel(writer,sheet_name='battery_mean_{}'.format(batch),index=False)
            df_experiment_mean.to_excel(writer,sheet_name='experiment_mean_{}'.format(batch),index=False)
        writer.close()
        print(df_experiment_mean.mean(numeric_only=True))

    if args.dataset == 'XJTU':
        root = f'../results of reviewer/{args.model}/XJTU results/' # "XJTU-CNN results" or "XJTU-MLP results"
        writer = pd.ExcelWriter(f'../results of reviewer/{args.model}-XJTU-results.xlsx')
        xjtu_gap = 0.05
        tju_gap = 0.07
        results = Results_XJTU(root,gap=xjtu_gap)

        for batch in range(6):
            df_battery_mean = results.get_battery_average(train_batch=batch,test_batch=batch)
            df_battery_mean.to_excel(writer, f'battery_mean_{batch}', index=False)
            df_experiment_mean = results.get_experiments_mean(train_batch=batch,test_batch=batch)
            df_experiment_mean.to_excel(writer,f'experiment_mean_{batch}',index=False)
        writer.close()


