# Results
>[!NOTE]
> This section presents the results and figures obtained from dQ/dV analysis using the NASA battery dataset.

##

### ICA Analysis 

<img width="1789" height="1189" alt="ICA" src="https://github.com/user-attachments/assets/25a32c6b-cdd2-4898-91b2-256802d6bbb6" />

> This plot shows the dV/dQ profiles of the B0047 battery over 30 discharging cycles. <br> The values gradually decrease as the cycles progress.

##

### Figure 3b
> **Correlation heatmap between extracted features and SOH in four datasets. The
numbers 1–17 represent 17 features, and feature 17 is `dV/dQ` value.**


<img width="835" height="530" alt="Figure 3b_NASA_dvdq" src="https://github.com/user-attachments/assets/a5dd2940-ca23-4b95-b345-a1f798203794" />


##

### Figure 4a
> The SOH estimation results of proposed PINN on four datasets. If predicted and true SOH are distributed near the diagonal, it indicates that the model performs well.

<img width="1064" height="886" alt="Figure 4a_NASA_dqdv" src="https://github.com/user-attachments/assets/7578ecb2-6dcf-4fa9-9431-edc0aa5eaa38" />

##

### Figure 4b
> Distributions of mean absolute error (MAE), mean absolute percentage error (MAPE), and root mean square error (RMSE) of 3 models (the proposed PINN (Ours), multi-layer perceptron (MLP), and convolutional neural network (CNN)) on four datasets.

<img width="1816" height="1058" alt="Figure 4b_dqdv" src="https://github.com/user-attachments/assets/19049a0c-2068-49e9-9f0e-e7f62ec7d906" />

**[Figure 4b | Reproduced figure with NASA_dqdv data]** 

<br>

<img width="1817" height="1058" alt="Figure 4b_dqdv_wo_CNN" src="https://github.com/user-attachments/assets/b5a99255-c024-4115-9fd6-9737a9f372ea" />

**[Figure 4b | Reproduced figure without CNN data]** 

##

### Comparision with Original NASA data
> Compared MAE, MAPE, and RMSE of three models between the NASA dataset and the NASA_dQdV dataset.


<img width="3583" height="4815" alt="Compare" src="https://github.com/user-attachments/assets/1037db3e-d9e0-4816-a93c-e87beb5c919a" />

**[Figure | MAE, MAPE, RMSE comparison of three models on NASA vs. NASA_dQdV.]** 
> The analysis shows that the dQ/dV dataset leads to higher errors (MAE, MAPE, RMSE) compared to the original NASA dataset, indicating that models perform better on the original data.
