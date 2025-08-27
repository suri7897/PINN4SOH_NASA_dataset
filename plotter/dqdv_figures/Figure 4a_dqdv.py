'''
English:
Plot the prediction results of different datasets
'''
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science','nature'])
from matplotlib.backends.backend_pdf import PdfPages
import os
from pathlib import Path

savedir = Path(__file__).parent / "figures"
savedir.mkdir   (parents=True, exist_ok=True)

# Plot a figure with 3 rows and 4 columns
with plt.rc_context({'text.usetex': False}):
    pdf = PdfPages(os.path.join(savedir,'Figure 4a_dqdv.pdf'))
    fig, axs = plt.subplots(3,3,figsize=(8,6),dpi=150)
    count = 0
    color_list = [
            '#74AED4',
            '#7BDFF2',
            '#FBDD85',
            '#F46F43',
            '#CF3D3E'
            ]
    colors = plt.cm.colors.LinearSegmentedColormap.from_list(
        'custom_cmap', color_list, N=256
    )
    batches = [1,2,3,5,7,8,9]
    for batch in batches:
        root = f'../../results/PINN/NASA_dqdv results/{batch}-{batch}/Experiment1/'
        title = f'NASA_dqdv batch {batch}'
        try:
            pred_label = np.load(root+'pred_label.npy')
            true_label = np.load(root+'true_label.npy')
        except Exception as e:
            print(f"--- FAILED to load data for NASA_dqdv batch {batch} ---")
            print(f"    Path: {root}")
            print(f"    Error: {e}")
            continue
        error = np.abs(pred_label-true_label)
        vmin, vmax = error.min(), error.max()

        lims = {
                'NASA_1':[0.3,0.75],
                'NASA_2' : [0.7,1.005]
                }
        # plot
        #fig = plt.figure(figsize=(3,2.6),dpi=200)
        #ax = fig.add_subplot(111)
        col = count%3
        row = count//3
        print("NASA_dqdv",batch,row,col)
        ax = axs[row,col]
        ax.scatter(true_label,pred_label,c=error, cmap=colors,s=3,alpha=0.7, vmin=0, vmax=0.1)
        ax.plot([0.3,1.15],[0.3,1.15],'--',c='#ff4d4e',alpha=1,linewidth=1)
        ax.set_aspect('equal')
        ax.set_xlabel('True SOH')
        ax.set_ylabel('Prediction')

        ax.set_xticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1])
        ax.set_yticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1])
        if batch in [7,8,9]:
            lim = lims["NASA_1"]
        else:
            lim = lims["NASA_2"]

        ax.set_xlim(lim)
        ax.set_ylim(lim)
        #plt.suptitle(title)
        #(set the title of each subplot)
        ax.set_title(title)

        if count >=14:
            break
        count += 1
    

# colorbar (draw a colorbar on the last subplot)
fig.colorbar(plt.cm.ScalarMappable(cmap=colors,norm=plt.Normalize(vmin=0, vmax=0.1)),
            ax=axs[2,2],
            label='Absolute error',

            # colorbar (set the position of the colorbar)
            fraction=0.46, pad=0.4
            )
# (turn off the axis of the last subplot)
axs[2,1].axis('off')
axs[2,2].axis('off')
axs[2,1].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(savedir,'Figure 4a_dqdv.png'),format='png')
pdf.savefig(fig)
pdf.close()
plt.show()