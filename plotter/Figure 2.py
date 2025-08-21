import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scienceplots
plt.style.use(['science','nature'])
from matplotlib.backends.backend_pdf import PdfPages

root = '../data/NASA data'
savedir = './figures'
pdf = PdfPages(os.path.join(savedir,'Figure 2.pdf'))
fig = plt.figure(figsize=(4,2),dpi=200)
# colors = [
# "#00A437",
# "#67FF0E",
# '#80A6E2',
# '#7BDFF2',
# '#FBDD85',
# '#F46F43',
# '#403990',
# '#CF3D3E',
# "#9B9B9B"
# ]
colors = [
    "#4E79A7",  # muted blue
    "#F28E2B",  # orange
    "#E15759",  # red
    "#76B7B2",  # teal
    "#59A14F",  # green
    "#EDC949",  # yellow
    "#AF7AA1",  # purple
    "#FF9DA7",  # pink
    "#9C755F"   # brown/earth
]
markers = ['o', 'v', 'D', 'p', 's', '^', '*', 'h', 'x']
legend = ['batch 1','batch 2','batch 3', 'batch 4', 'batch 5', 'batch 6', 'batch 7','batch 8', 'batch 9']
batches = ['Dataset_05_06_07_18', 'Dataset_25_26_27_28', 'Dataset_29_30_31_32', 'Dataset_33_34_36', 'Dataset_38_39_40', 'Dataset_41_42_43_44', 'Dataset_45_46_47_48', 'Dataset_49_50_51_52', 'Dataset_53_54_55_56']
custom_lines = []
legends = []
line_width = 1.0

with plt.rc_context({'text.usetex': False}):
    for i in range(0,9):
        batch_root = os.path.join(root, batches[i])
        files = os.listdir(batch_root)
        for f in files:
            path = os.path.join(batch_root,f)
            data = pd.read_csv(path)
            capacity = data['capacity'].values
            plt.plot(capacity[1:],color=colors[i],alpha=1,linewidth=line_width,
                        # linestyle=':',
                        marker=markers[i],markersize=2,markevery=50)
        custom_lines.append(Line2D([0], [0], color=colors[i], linewidth=line_width,marker=markers[i],markersize=2.5))
        legends.append(legend[i])
    plt.xlabel('Cycle')
    plt.ylabel('Capacity (Ah)')

    custom_legend = plt.legend(custom_lines, legends, loc='upper right',
                            bbox_to_anchor=(1.0, 1), frameon=False,
                            ncol=3, fontsize=6)


    plt.ylim([0.5,2.5])
    plt.tight_layout()

pdf.savefig(fig)
plt.savefig(os.path.join(savedir,'Figure 2.png'),format='png')
pdf.close()

