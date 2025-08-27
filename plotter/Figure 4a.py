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

savedir = './figures'

# Plot a figure with 3 rows and 4 columns
with plt.rc_context({'text.usetex': False}):
    pdf = PdfPages(os.path.join(savedir,'Figure 4a.pdf'))
    fig, axs = plt.subplots(4,5,figsize=(8,6),dpi=150)
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
    for data in ['NASA','TJU','MIT','HUST', 'XJTU']:
        if data == 'XJTU':
            batches = [0,1,2,3,4,5]
        elif data == 'TJU':
            batches = [0,1,2]
        elif data == 'NASA':
            batches = [1,2,3,5,7,8,9]
        else:
            batches = [0]
        for batch in batches:
            if data in ['HUST','MIT']:
                root = f'../results/PINN/{data} results/Experiment1/'
                title = f'{data} dataset'
            elif data in ['NASA']:
                root = f'../results/PINN/NASA results/{batch}-{batch}/Experiment1/'
                title = f'{data} batch {batch}'
            else:
                root = f'../results/PINN/{data} results/{batch}-{batch}/Experiment1/'
                title = f'{data} batch {batch+1}'
            try:
                pred_label = np.load(root+'pred_label.npy')
                true_label = np.load(root+'true_label.npy')
            except Exception as e:
                print(f"--- FAILED to load data for {data} batch {batch} ---")
                print(f"    Path: {root}")
                print(f"    Error: {e}")
                continue
            error = np.abs(pred_label-true_label)
            vmin, vmax = error.min(), error.max()

            lims = {'HUST':[0.79,1.105],
                    'MIT':[0.79,1.005],
                    'XJTU':[0.79,1.005],
                    'TJU':[0.69,0.97],
                    'NASA_1':[0.3,0.75],
                    'NASA_2' : [0.7,1.005]
                    }
            # plot
            #fig = plt.figure(figsize=(3,2.6),dpi=200)
            #ax = fig.add_subplot(111)
            col = count%5
            row = count//5
            print(data,batch,row,col)
            ax = axs[row,col]
            ax.scatter(true_label,pred_label,c=error, cmap=colors,s=3,alpha=0.7, vmin=0, vmax=0.1)
            ax.plot([0.3,1.15],[0.3,1.15],'--',c='#ff4d4e',alpha=1,linewidth=1)
            ax.set_aspect('equal')
            ax.set_xlabel('True SOH')
            ax.set_ylabel('Prediction')

            ax.set_xticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1])
            ax.set_yticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1])
            if data in ["XJTU", "TJU", "MIT", "MIT"]:
                lim = lims[data]
            else :
                if batch in [7,8,9]:
                    lim = lims["NASA_1"]
                else:
                    lim = lims["NASA_2"]

            ax.set_xlim(lims[data])
            ax.set_ylim(lims[data])
            #plt.suptitle(title)
            #(set the title of each subplot)
            ax.set_title(title)

            if count >=17:
                break
            count += 1

        if count >= 17:
            break
        

    # colorbar (draw a colorbar on the last subplot)
    fig.colorbar(plt.cm.ScalarMappable(cmap=colors,norm=plt.Normalize(vmin=0, vmax=0.1)),
                ax=axs[3,3],
                label='Absolute error',

                # colorbar (set the position of the colorbar)
                fraction=0.46, pad=0.4
                )
    # (turn off the axis of the last subplot)
    axs[3,3].axis('off')

    axs[3,4].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(savedir,'Figure 4a.png'),format='png')
    pdf.savefig(fig)
    pdf.close()
    plt.show()