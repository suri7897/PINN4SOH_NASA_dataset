import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from pathlib import Path
import os
from matplotlib.backends.backend_pdf import PdfPages

def plotter(corr_mat, dataset, savedir):
    with plt.rc_context({'text.usetex': False}):
        pdf = PdfPages(os.path.join(savedir, f'Figure 3b_{dataset}.pdf'))
        n_rows, n_feat = corr_mat.shape

        cell_in = 0.40           # length of correlation sqaure box
        gap_in  = 0.10           # length of gap between each correlation boxes
        left_pad, right_pad = 0.60, 0.25     # outer edge padding
        top_pad,  bottom_pad = 0.35, 0.55

        group_label = dataset # labeling

        # figure size calculation
        ax_w = n_feat * cell_in
        ax_h = cell_in
        fig_w = left_pad + ax_w + right_pad
        fig_h = top_pad + n_rows * ax_h + (n_rows - 1) * gap_in + bottom_pad

        hspace_frac = gap_in / ax_h if n_rows > 1 else 0.0

        fig = plt.figure(figsize=(fig_w, fig_h), constrained_layout=False)

        plot_left   = left_pad / fig_w
        plot_right  = 1 - (right_pad) / fig_w
        plot_top    = 1 - top_pad / fig_h
        plot_bottom = bottom_pad / fig_h

        gs = fig.add_gridspec(
            nrows=n_rows, ncols=1,
            left=plot_left, right=plot_right,
            top=plot_top, bottom=plot_bottom,
            hspace=hspace_frac
        )

        axes = [fig.add_subplot(gs[i, 0]) for i in range(n_rows)]
        cmap = plt.get_cmap('coolwarm')

        im_last = None
        for i, ax in enumerate(axes):
            row = corr_mat[i:i+1, :]
            im = ax.imshow(row, vmin=-1, vmax=1, cmap=cmap,
                        aspect='equal', interpolation='nearest')
            im_last = im

            if i != n_rows - 1:
                ax.set_xticks([])
            else:
                ax.set_xticks(np.arange(n_feat))
                ax.set_xticklabels([str(k+1) for k in range(n_feat)], fontsize=11)
                ax.set_xlabel("Feature Number", fontsize=12)

            for j in range(n_feat):
                ax.text(j, 0, f"{corr_mat[i, j]:+.2f}",
                        ha='center', va='center', fontsize=8, color='black')

            ax.get_yaxis().set_visible(False)
            for s in ax.spines.values():
                s.set_visible(False)
            ax.tick_params(length=0, pad=5)

        fig.text(
            plot_left - 0.02,                        
            (plot_bottom + plot_top) / 2,            
            group_label,
            ha="right", va="center", fontsize=12
        )

        plt.savefig(os.path.join(savedir,f'Figure 3b_{dataset}.png'),format='png')
        pdf.savefig(fig)
        pdf.close()
        plt.show()


if __name__ == "__main__":

    data_root = "../data"
    savedir = './figures/Figure 3b'
    os.makedirs(savedir, exist_ok = True)

    for data in ['NASA','TJU','MIT','HUST', 'XJTU']:
        all_corr_rows = []
        dataset_name = data

        if data == 'XJTU':
            batches = ['2C', '3C', 'R2.5', 'R3', 'RW', 'satellite']
        elif data == 'TJU':
            batches = ['Dataset_1_NCA_battery','Dataset_2_NCM_battery','Dataset_3_NCM_NCA_battery']
        elif data == 'NASA':
            batches = ['Dataset_05_06_07_18', 'Dataset_25_26_27_28', 'Dataset_29_30_31_32', 'Dataset_33_34_36', 'Dataset_38_39_40',
                    'Dataset_41_42_43_44', 'Dataset_45_46_47_48', 'Dataset_49_50_51_52', 'Dataset_53_54_55_56']
        elif data == 'MIT':
            batches = [0]
        else:
            batches = [0]
        data_dir = os.path.join(data_root, f"{data} data")
        for batch in batches:
            if data in ['TJU', 'NASA']:
                batch_dir = os.path.join(data_dir, batch)
                batch_files = glob.glob(os.path.join(batch_dir,"*.csv")) # get batch files
            elif data in ["MIT"]:
                batch_dir = os.path.join(data_dir, "*")
                batch_files = glob.glob(os.path.join(batch_dir,"*.csv"))
            elif data in ["XJTU"]:
                batch_dir = data_dir
                batch_files = glob.glob(os.path.join(batch_dir, f"*{batch}*.csv"))  # get batch files
            else:
                batch_dir = data_dir
                batch_files = glob.glob(os.path.join(batch_dir,"*.csv"))  # get batch files

            df_list = [pd.read_csv(f) for f in batch_files]
            df = pd.concat(df_list, ignore_index = True)

            feature_cols = [col for col in df.columns if col != "capacity"]

            corr_vals = df[feature_cols + ["capacity"]].corr(method="pearson").loc[feature_cols, "capacity"].values
           
            all_corr_rows.append(corr_vals)
       
        corr_mat = np.vstack(all_corr_rows)
        plotter(corr_mat, dataset_name, savedir)