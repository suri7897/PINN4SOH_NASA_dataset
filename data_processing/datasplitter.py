from scipy.stats import kurtosis, skew, entropy
import numpy as np
import pandas as pd
import re
import os
import glob

def compute_shannon_entropy(signal, bins=100): # Compute Entropy
    hist, _ = np.histogram(signal, bins=bins, density=True)
    hist = hist[hist > 0]  
    return entropy(hist, base=2)  

def extract_file_number(filename):
    return int(re.findall(r'\d+', filename)[0])

def extract_battery_num(battery_id):
    return battery_id[-2:]

print("Data splitting starts...")

# directory setting
data_dir = "NASA_dataset/data"
output_dir = "../NASA data"
metadata = pd.read_csv("NASA_dataset/metadata.csv")
data_type = 'charge' # 'dischrage' or 'charge'

features = [
    'voltage mean', 'voltage std', 'voltage kurtosis', 'voltage skewness',
    'CC Q', 'CC charge time', 'voltage slope', 'voltage entropy',
    'current mean', 'current std', 'current kurtosis', 'current skewness',
    'CV Q', 'CV charge time', 'current slope', 'current entropy',
    'capacity'
]

batches = ['Dataset_05_06_07_18', 'Dataset_25_26_27_28', 'Dataset_29_30_31_32', 'Dataset_33_34_36', 'Dataset_38_39_40', 
           'Dataset_41_42_43_44', 'Dataset_45_46_47_48', 'Dataset_49_50_51_52', 'Dataset_53_54_55_56']

for battery_id in metadata['battery_id'].unique():
    battery_df = metadata[(metadata['battery_id'] == battery_id) & (metadata['type'] == data_type)]

    result = []
    
    batch = None
    
    battery_num = extract_battery_num(battery_id)
    for batch_elem in batches:
        if battery_num in batch_elem:
            batch = batch_elem
            break
    
    if batch == None :
        continue
    
    for _, row in battery_df.iterrows():
        filepath = os.path.join(data_dir, row['filename'])
        charge_num = extract_file_number(row['filename'])

        discharge_rows = metadata[
            (metadata['battery_id'] == battery_id) &
            (metadata['type'] == 'discharge')
        ].copy()

        discharge_rows['file_num'] = discharge_rows['filename'].apply(extract_file_number)
        discharge_rows = discharge_rows.sort_values('file_num')

        valid_future = discharge_rows[
            (discharge_rows['file_num'] > charge_num) &
            (~discharge_rows['Capacity'].isna())
        ]

        if not valid_future.empty:
            capacity = valid_future.iloc[0]['Capacity']
        else:
            capacity = np.nan
        
        try:
            df = pd.read_csv(filepath)
            # Use data of [V_end - 0.2, V_end], where V_end is defined as the 95th percentile of the dataset, since peak values are unstable.
            df = df[(df['Voltage_measured'] > df['Voltage_measured'].quantile(0.95) - 0.2) & (df['Voltage_measured'] < df['Voltage_measured'].quantile(0.95) + 0.2)]
            df[['Voltage_measured', 'Current_measured', 'Time']] = df[
                ['Voltage_measured', 'Current_measured', 'Time']
            ].ffill().bfill()

            if df[['Voltage_measured', 'Current_measured', 'Time']].isnull().any().any():
                print(f"{filepath} skipped: still contains NaN after filling")
                continue

            v = df['Voltage_measured']
            c = df['Current_measured']
            t = df['Time']

            cv_mask = v > v.max() - 0.005
            cc_mask = ~cv_mask

            row_result = {
                'voltage mean': v.mean(),
                'voltage std': v.std(),
                'voltage kurtosis': kurtosis(v),
                'voltage skewness': skew(v),
                'CC Q': np.trapz(c[cc_mask], t[cc_mask]) if cc_mask.any() else np.nan,
                'CC charge time': t[cc_mask].iloc[-1] - t[cc_mask].iloc[0] if cc_mask.sum() > 1 else np.nan,
                'voltage slope': np.gradient(v, t).mean(),
                'voltage entropy': compute_shannon_entropy(v),  
                'current mean': c.mean(),
                'current std': c.std(),
                'current kurtosis': kurtosis(c),
                'current skewness': skew(c),
                'CV Q': np.trapz(c[cv_mask], t[cv_mask]) if cv_mask.any() else np.nan,
                'CV charge time': t[cv_mask].iloc[-1] - t[cv_mask].iloc[0] if cv_mask.sum() > 1 else np.nan,
                'current slope': np.gradient(c, t).mean(),
                'current entropy': compute_shannon_entropy(c),  
                'capacity': capacity
            }

            result.append(row_result)

        except Exception as e:
            print(f"Error in {filepath}: {e}")
            print(df)
    batch_dir = os.path.join(output_dir, batch)
    out_path = os.path.join(batch_dir, f"{battery_id}_{data_type}_summary.csv")
    
    
    if not os.path.exists(batch_dir):
        os.makedirs(batch_dir)
    
    result_df = pd.DataFrame(result[:-1])
    voltage_mean_overall = result_df['voltage mean'].mean()
    result_df = result_df[(result_df['capacity'] != '[]')]
    # result_df = result_df[
    #     (result_df['voltage mean'] >= voltage_mean_overall - 1) &
    #     (result_df['voltage mean'] <= voltage_mean_overall + 1)
    # ]

    result_df.to_csv(out_path, index=False)
    
    print(f"{battery_id}_{data_type}_summary.csv saved in {batch}" )

print("Data split all done.")