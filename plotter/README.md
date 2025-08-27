PINN4SOH - Plotter
---
>[!NOTE]
> These files provide code for generating the figures, implemented based on the original code from the paper.  
> The codes have been slightly modified to fit the NASA dataset.  
> In particular, the code for Figure 3 was implemented by myself, since the original implementation for this figure was not provided.


Overview
---
The `Plotter` folder contains the codes for generating the **figures** presented in the original paper.  
You can execute these python files to save each `figures`.

```bash
# current directory : PINN4SOH_NASA_dataset/plotter
python3 [filename].py
```
In particular, `Figure 4b.py` can plot the violin plot even **without the CNN results**.
```
python3 Figure\ 4b.py --CNN=False
```

# Result

>[!NOTE]
> The Figure of NASA dataset with **`dqdv` index** is omitted in this README.md file, and these could be found in `dqdv_figures` folder.

### Figure 2 
> **The degradation trajectories of battery dataset.**

<img width="700" height="400" alt="Figure 2" src="https://github.com/user-attachments/assets/b0ed109f-01ff-4b69-8830-eb34f825ad8f" />

**[Figure 2 | Original figure with XJTU data]**  
> Total 6 batches, and each batches contain 8 battery datas. 

 <br>

<img width="700" height="350" alt="Figure 2_NASA" src="https://github.com/user-attachments/assets/c82c77e6-872f-4e12-8e47-2333ad3a0c82" />

**[Figure 2 | Reproduced figure with NASA data]**  
> Total 9 batches, and each batches contain 3 ~ 4 battery datas.

 <br>

##

### Figure 3
> **Correlation heatmap between extracted features and SOH in four datasets. The
numbers 1–16 represent 16 features.**

<img width="784" height="820" alt="Figure 3b" src="https://github.com/user-attachments/assets/3fdbd1f7-97fe-435c-a767-3355056ef080" />  

**[Figure 3b | Original figure]** 

 <br>

<img width="500" height="360" alt="Figure 3b_NASA" src="https://github.com/user-attachments/assets/5c62c8ce-9367-44f9-8bfe-5ccba8ba04eb" /> 
<img width="500" height="260" alt="Figure 3b_XJTU" src="https://github.com/user-attachments/assets/d242ec79-2716-445d-abc9-c7f251740e72" />  
<img width="500" height="160" alt="Figure 3b_TJU" src="https://github.com/user-attachments/assets/45be5b56-2c3e-44b7-8f12-0a28a4a5a30a" />  
<img width="500" height="90" alt="Figure 3b_MIT" src="https://github.com/user-attachments/assets/17e337dd-daf0-46af-967b-6a7159f7b2bb" />  
<img width="500" height="90" alt="Figure 3b_HUST" src="https://github.com/user-attachments/assets/e64233d6-b396-4a1f-8b62-6711432d6874" />  

**[Figure 3 | Reproduced figure 3b with NASA data]**  

##

### Figure 4a
> The SOH estimation results of proposed PINN on four datasets. The predicted and true SOH are distributed near the diagonal, indicating that the model performs well.

<img width="1394" height="977" alt="Figure 4a" src="https://github.com/user-attachments/assets/7f5b18e7-461b-4d98-affb-80f434022c02" /> 

**[Figure 4a | Original figure]**  

 <br>

<img width="1162" height="886" alt="Figure 4a_with_NASA" src="https://github.com/user-attachments/assets/02cfc961-518c-4929-90e0-4291ca00d3ac" />

**[Figure 4a | Reproduced figure with NASA data]** 

 <br>

##

### Figure 4b
> Distributions of mean absolute error (MAE), mean absolute percentage error (MAPE), and root mean square error (RMSE) of 3 models (the proposed PINN (Ours), multi-layer perceptron (MLP), and convolutional neural network (CNN)) on four datasets.

<img width="1362" height="771" alt="Figure 4b" src="https://github.com/user-attachments/assets/7c50c145-1831-4180-9791-c94d1e311b32" />

**[Figure 4b | Original figure]**

 <br>

<img width="1817" height="1058" alt="Figure 4b_with NASA" src="https://github.com/user-attachments/assets/085d85a6-f55d-4644-a41e-367aa70a8027" />

**[Figure 4b | Reproduced figure with NASA data]** 

 <br>

<img width="1817" height="1058" alt="Figure 4b_wo CNN_with NASA" src="https://github.com/user-attachments/assets/5161cb20-35f7-470e-9ffb-0385a0c66d72" />

**[Figure 4b | Reproduced figure without CNN data]** 

 <br>
