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

<img width="1060" height="883" alt="Figure 4a_dqdv" src="https://github.com/user-attachments/assets/831f9ab6-d476-4b00-a649-26c61783c88a" />


##

### Figure 4b
> Distributions of mean absolute error (MAE), mean absolute percentage error (MAPE), and root mean square error (RMSE) of 3 models (the proposed PINN (Ours), multi-layer perceptron (MLP), and convolutional neural network (CNN)) on four datasets.

<img width="1818" height="1058" alt="Figure 4b_dqdv" src="https://github.com/user-attachments/assets/a5e03894-c72a-41e2-b18a-aa77e0e461e4" />


**[Figure 4b | Reproduced figure with NASA_dqdv data]** 

<br>

<img width="1817" height="1058" alt="Figure 4b_dqdv_wo_CNN" src="https://github.com/user-attachments/assets/19728247-33df-4ce7-b417-cc54d77a31e4" />


**[Figure 4b | Reproduced figure without CNN data]** 

##

### Comparision with Original NASA data
> Compared MAE, MAPE, and RMSE of three models between the NASA dataset and the NASA_dQdV dataset.


<img width="3581" height="4815" alt="comparision" src="https://github.com/user-attachments/assets/e30c81f5-5556-4c16-8d3c-a30ec1e567be" />


**[Figure | MAE, MAPE, RMSE comparison of three models on NASA vs. NASA_dQdV.]** 
> The analysis shows that the dQ/dV dataset leads to higher errors (MAE, MAPE, RMSE) compared to the original NASA dataset, indicating that models perform better on the original data.
