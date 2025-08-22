# Lithium-ion Battery Calendar Ageing Model using Universal Differential Equations

> [!IMPORTANT]
I acknowledge that all ideas and codes presented here are derived from the study titled '**[Physics-informed neural network for lithium-ion battery degradation stable modeling and prognosis](https://www.nature.com/articles/s41467-024-48779-z)**' (2024). This code is created for **learning and practice purposes** only.

---


This repository contains the implementation of Lithium-ion battery SOH prediction using Physics informed neural network. The model is based on the article titled "*Physics-informed neural network for lithium-ion battery degradation stable modeling and prognosis*" by **Fujin Wang**, **Zhi Zhai**, **Zhibin Zhao**, **Yi Di** and **Xuefeng Chen**.


#
This repository replaces the XJTU dataset used in prior work with the **NASA Battery Dataset**.
- Please note that this code might produce inaccurate results or fail to run properly, since it was developed mainly for practice and learning purposes.
- The code was developed with the assistance of generative large language model (LLM).

#

For further details, refer to the repository available at
- Codes : https://github.com/wang-fujin/PINN4SOH.git.

# **Usage Instructions**

To run the model, follow these steps:

- **This code is developed under Python version 3.12, Pytorch 2.4.0.**

## **1. Clone the Repository**
   ```bash
   git clone https://github.com/suri7897/PINN4SOH_NASA_dataset.git
   cd PINN4SOH_NASA_dataset
   ```

## **2. Setup Conda environment**  
   Create Conda environment.
   ```bash
   conda create -n new_env python=3.12
   conda activate new_env
   ```
   Then, Install Dependencies.
   ```bash
   conda install pytorch=2.4.0
   pip install scikit-leran numpy matplotlib pandas scienceplots glob
   ```

## **3. Implementation Guide**
  ### 1) Data preprocessing
  Since the NASA Battery Dataset provides full cycle data along with measurements of voltage, current, and time, additional preprocessing is required to make it compatible with the model.  
  This repository already contains the processed NASA battery dataset, so preprocessing is actually not required for implementation.  

  To do preprocessing, run `data_splitter.ipynb`.

  ### 2) Train Model
  To train PINN model with **NASA dataset**, run `main_NASA.py`.
  ```bash
  # Working Directory = /PINN4SOH_NASA_dataset
   python3 main_NASA.py
   ```
  If you want to train PINN model with **XJTU dataset**, run `main_XJTU.py`.
  ```
   python3 main_XJTU.py
   ```
  If you want to train other models (CNN, MLP), run `main_comparision.py`.
  ```bash
  # Usage : python3 main_comparision.py --model=<model> --dataset=<dataset>
  # default = MLP, NASA
   python3 main_comparision.py --model=MLP --dataset=NASA
   ```
  The trained model and corresponding loss log files will be stored in the results_of_reviewer folder.

  ### 3) Evaluate Model
  After training, you can evaluate the model in the `results analysis` folder.  
  To evaluate PINN model trained with **NASA dataset**, run `NASA results.py`.
  ```
  python3 NASA\ results.py
  ```
  To evaluate model with **XJTU dataset**, run `XJTU results.py`.
  ```
  python3 XJTU\ results.py
  ```
  To evaluate other models (CNN, MLP), run 'Comparision results.py'
  ```bash
  # Usage : python3 Comparision\ results.py --model=<model> --dataset=<dataset>
  # default = MLP, dataset is required argument
   python3 main_comparision.py --model=MLP --dataset=NASA
   ```
   This codes generate the evaluating errors in the format of xlsx file. At the same time, the results of each batch will also be printed on the Command Console.
   
  ### 4) Plotter
  The figures in the paper, including those based on the NASA dataset, can be generated in the `plotter` folder.

# **Dataset**

### 1) NASA battery dataset
  This project uses the NASA lithium-ion battery dataset from the Prognostics Data.  
  It contains charge/discharge cycle data and is commonly used for battery degradation and State of Health (SOH) prediction.
  Here, I used only charging data to keep the method in original paper.
  
  - Data available on https://www.kaggle.com/datasets/patrickfleith/nasa-battery-dataset.

### 2) XJTU battery Dataset
  The baseline paper’s authors also released a comprehensive dataset containing 55 lithium-nickel-cobalt-manganese-oxide (NCM) batteries.
  In this project, it is also used for comparative analysis with the NASA dataset.

  It is available at: [Link](https://wang-fujin.github.io/)

  Zenodo link: [https://zenodo.org/records/10963339](https://zenodo.org/records/10963339).

### 3) Additional Data

  The data in the `data` folder is preprocessed data.
  Raw data can be obtained from the following links:
  1. XJTU dataset: [link](https://wang-fujin.github.io/)
  2. TJU dataset: [link](https://zenodo.org/record/6405084)
  3. HUST dataset: [link](https://data.mendeley.com/datasets/nsc7hnsg4s/2)
  4. MIT dataset: [link](https://data.matr.io/1/projects/5c48dd2bc625d700019f3204)
  
  The code for **reading and preprocessing** the dataset is publicly available at [https://github.com/wang-fujin/Battery-dataset-preprocessing-code-library](https://github.com/wang-fujin/Battery-dataset-preprocessing-code-library)
  
