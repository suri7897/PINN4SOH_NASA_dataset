'''
English:
Draw a violin plot and plot all datasets on one figure
Common experiments on 4 data sets, plotting violin plots of indicators [MAE, MAPE, RMSE],
and comparing Ours, MLP, and CNN on the same figure
'''
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science','nature'])
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as mtick
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator
import os
import argparse


def percentage(x, pos):
    if x >= 0.2:
        return '{:.0f}%'.format(x * 100)
    else:
        return '{:.1f}%'.format(x * 100)

def get_cnn():
    p = argparse.ArgumentParser()
    p.add_argument('--CNN', type=str, default='True', choices=['True', 'False'],
                   help='Choose dataset')
    cnn = p.parse_args().CNN
    if cnn == 'True':
        return True
    else :
        return False

if __name__ == '__main__':
    cnn = get_cnn()
    savedir = './figures'
    if cnn:
        print("Plotting Figure 4b...")
        pdf = PdfPages(os.path.join(savedir,'Figure 4b_dqdv.pdf'))
        with plt.rc_context({'text.usetex': False}):
            fig, axs = plt.subplots(3,3,figsize=(2.3*4,1.8*3),dpi=200)
            colors = ['#b8dff2','#abeadb','#ffb2b4']
            count = 0
            batches = [1,2,3,5,7,8,9]
               
            for batch in batches:
                ############################
                df_list = []
                for model in ['Ours', 'MLP', 'CNN']:

                    df1 = pd.read_excel(f'../../results analysis/processed results/{model}-NASA_dqdv-results.xlsx',
                                        engine='openpyxl',
                                        sheet_name=f'battery_mean_{batch}')

                    df1['model'] = [model] * df1.shape[0]
                    melted_df1 = pd.melt(df1, id_vars=['model'],
                                        value_vars=['MAE','MAPE','RMSE'],
                                        var_name='metric', value_name='error')
                    df_list.append(melted_df1)
                    title = 'NASA_dqdv' + f' batch {batch}'

                merge_df_keys = ['Ours', 'MLP', 'CNN']

                # Concatenate three DataFrames
                df = pd.concat(df_list, axis=0)
                df = df.reset_index()
                df.drop('index', axis=1, inplace=True)
                df['metric'] = df['metric'].astype('category').cat.codes


                # Draw a violin plot
                col = count % 3
                row = count // 3
                print("NASA_dqdv", batch, row, col)
                ax = axs[row, col]
                sns.violinplot(x='metric',y='error',hue='model',data=df,
                            density_norm='count',
                            inner='point',
                            dodge=True,
                            saturation=1,
                            palette=colors,
                            linewidth=0,
                            ax=ax)

                # After drawing the violin plot, add the following code to calculate and draw the mean line and the mean plus or minus the standard deviation line
                for i, metric in enumerate(['MAE', 'MAPE', 'RMSE']):
                    for model in ['Ours', 'MLP', 'CNN']:
                        model_mean = df[(df['model'] == model) & (df['metric'] == i)]['error'].mean()  # mean
                        model_std = df[(df['model'] == model) & (df['metric'] == i)]['error'].std()  # standard deviation
                        # x position of the standard deviation line and mean line
                        offset = 0.27
                        x_pos = i + (model == 'CNN') * offset - (model == 'Ours') * offset
                        # draw the standard deviation line
                        ax.plot([x_pos, x_pos], [model_mean - model_std, model_mean + model_std], color='black', linestyle='-',
                                linewidth=0.5)
                        # draw the mean line
                        ax.plot([x_pos - 0.1, x_pos + 0.1], [model_mean, model_mean], color='red', linestyle='-', linewidth=0.6)        
                

                # set the x-axis range and label position
                
                ax.xaxis.set_major_locator(FixedLocator([0,1,2]))
                ax.set_xticklabels(['MAE', 'MAPE', 'RMSE'])
                ax.set_xlabel(None)
                # set the y-axis range

                # ax.set_ylim(0, 0.055)


                ax.yaxis.set_major_formatter(mtick.FuncFormatter(percentage))
                # add a percentage text at the top of the y-axis
                x_min, x_max = ax.get_xlim()
                y_max = ax.get_ylim()[1]
                ax.annotate(r'(\%)', xy=(x_min, y_max), xytext=(-2, 3),
                            textcoords='offset points', ha='center', fontsize=8)
                ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

                # add title and label
                ax.set_title(title)
                ax.set_ylabel("Error")

                # remove the legend
                ax.get_legend().remove()

                if count >= 7:
                    break
                count += 1

            ## add legend
            axs[2, 1].set_visible(False)
            # remove the axis of axs[2,3]
            axs[2, 2].axis('off')
            boxs = []
            for c in colors:
                box = plt.Rectangle((0, 0), 1, 1, fc=c)
                boxs.append(box)
            mean_line = Line2D([0], [0], color='red', linestyle='-', linewidth=1)
            std_line = Line2D([0, 0], [0, 1], color='black', linestyle='-', linewidth=1)
            boxs.append(mean_line)
            boxs.append(std_line)
            legend_labels = ['PINN','MLP','CNN','Mean','Mean $\\pm$ Std']
            axs[2, 2].legend(handles=boxs,labels=legend_labels, loc=[0.2, 0],
                            handlelength=4,
                            handleheight=2.5,
                            fontsize=8)

            plt.tight_layout()
            plt.savefig(os.path.join(savedir,'Figure 4b_dqdv.png'),format='png')
            pdf.savefig()
            pdf.close()
            plt.show()
    else :
        print("Plotting Figure 4b without CNN...")
        pdf = PdfPages(os.path.join(savedir,'Figure 4b_dqdv_wo_CNN.pdf'))
        with plt.rc_context({'text.usetex': False}):
            fig, axs = plt.subplots(3,3,figsize=(2.3*4,1.8*3),dpi=200)
            colors = ['#b8dff2','#abeadb']
            count = 0
            batches = [1,2,3,5,7,8,9]
            data = "NASA_dqdv"
            for batch in batches:
                ############################
                df_list = []
                for model in ['Ours', 'MLP']:

                    df1 = pd.read_excel(f'../../results analysis/processed results/{model}-{data}-results.xlsx',
                                        engine='openpyxl',
                                        sheet_name=f'battery_mean_{batch}')

                    df1['model'] = [model] * df1.shape[0]
                    melted_df1 = pd.melt(df1, id_vars=['model'],
                                        value_vars=['MAE','MAPE','RMSE'],
                                        var_name='metric', value_name='error')
                    df_list.append(melted_df1)
 
                title = data + f' batch {batch}'
                merge_df_keys = ['Ours', 'MLP']

                # Concatenate three DataFrames
                df = pd.concat(df_list, axis=0)
                df = df.reset_index()
                df.drop('index', axis=1, inplace=True)
                df['metric'] = df['metric'].astype('category').cat.codes


                # Draw a violin plot
                col = count % 3
                row = count // 3
                print(data, batch, row, col)
                ax = axs[row, col]
                sns.violinplot(x='metric',y='error',hue='model',data=df,
                            density_norm='count',
                            inner='point',
                            dodge=True,
                            saturation=1,
                            palette=colors,
                            linewidth=0,
                            ax=ax)

                # After drawing the violin plot, add the following code to calculate and draw the mean line and the mean plus or minus the standard deviation line
                for i, metric in enumerate(['MAE', 'MAPE', 'RMSE']):
                    for model in ['Ours', 'MLP']:  
                        model_mean = df[(df['model'] == model) & (df['metric'] == i)]['error'].mean()
                        model_std = df[(df['model'] == model) & (df['metric'] == i)]['error'].std()
                        offset = 0.20
                        if model == 'Ours':
                            x_pos = i - offset
                        else:  # MLP
                            x_pos = i + offset
                        ax.plot([x_pos, x_pos], [model_mean - model_std, model_mean + model_std],
                                color='black', linestyle='-', linewidth=0.5)
                        ax.plot([x_pos - 0.1, x_pos + 0.1], [model_mean, model_mean],
                                color='red', linestyle='-', linewidth=0.6)
                

                # set the x-axis range and label position
                
                ax.xaxis.set_major_locator(FixedLocator([0,1,2]))
                ax.set_xticklabels(['MAE', 'MAPE', 'RMSE'])
                ax.set_xlabel(None)
                # set the y-axis range

                # ax.set_ylim(0, 0.055)

                # add a percentage sign on the top of the y-axis



                ax.yaxis.set_major_formatter(mtick.FuncFormatter(percentage))
                # add a percentage text at the top of the y-axis
                x_min, x_max = ax.get_xlim()
                y_max = ax.get_ylim()[1]
                ax.annotate(r'(\%)', xy=(x_min, y_max), xytext=(-2, 3),
                            textcoords='offset points', ha='center', fontsize=8)
                ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

                # add title and label
                ax.set_title(title)
                ax.set_ylabel("Error")

                # remove the legend
                ax.get_legend().remove()

                if count >= 7:
                    break
                count += 1

            ## add legend
            axs[2, 1].set_visible(False)
            # remove the axis of axs[2,3]
            axs[2, 2].axis('off')
            boxs = []
            for c in colors:
                box = plt.Rectangle((0, 0), 1, 1, fc=c)
                boxs.append(box)
            mean_line = Line2D([0], [0], color='red', linestyle='-', linewidth=1)
            std_line = Line2D([0, 0], [0, 1], color='black', linestyle='-', linewidth=1)
            boxs.append(mean_line)
            boxs.append(std_line)
            legend_labels = ['PINN','MLP','CNN','Mean','Mean $\\pm$ Std']
            axs[2, 2].legend(handles=boxs,labels=legend_labels, loc=[0.2, 0],
                            handlelength=4,
                            handleheight=2.5,
                            fontsize=8)

            plt.tight_layout()
            plt.savefig(os.path.join(savedir,'Figure 4b_dqdv_wo_CNN.png'),format='png')
            pdf.savefig()
            pdf.close()
            plt.show()

