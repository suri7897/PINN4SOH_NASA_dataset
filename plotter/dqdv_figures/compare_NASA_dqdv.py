import os
from pathlib import Path
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages

root = Path("../../results analysis/processed results")
savedir = Path("./figures")
savedir.mkdir(parents=True, exist_ok=True)

datasets = ["NASA", "NASA_dqdv"] 
batches = [1, 2, 3, 5, 7, 8, 9]
models = ["PINN", "MLP", "CNN"]
metric_order = ["MAE", "MAPE", "RMSE"]
palette_ds = ["#b8dff2", "#ffb2b4"]

def load_one_batch(model: str, dataset: str, batch: int) -> pd.DataFrame:
    if model == "PINN":
        model = "Ours"
    xlsx = root / f"{model}-{dataset}-results.xlsx"
    try:
        df = pd.read_excel(xlsx, engine="openpyxl", sheet_name=f"battery_mean_{batch}")
    except Exception:
        return pd.DataFrame(columns=["dataset", "metric", "error", "batch"])
    df["dataset"] = dataset
    m = pd.melt(df, id_vars=["dataset"],
                value_vars=metric_order,
                var_name="metric", value_name="error")
    m["metric"] = pd.Categorical(m["metric"], categories=metric_order, ordered=True)
    m["batch"] = batch
    return m

def percent_fmt(x, pos):
    return f"{x*100:.0f}%" if x >= 0.2 else f"{x*100:.1f}%"

with plt.rc_context({'text.usetex': False}):
    n = len(batches)
    ncols = 4
    rows_per_model = math.ceil(n / ncols)
    total_rows = rows_per_model * len(models)

    fig, axs = plt.subplots(total_rows, ncols,
                            figsize=(3.0*ncols, 2.8*total_rows),
                            dpi=200)
    used_axes = []

    for m_idx, model in enumerate(models):
        base_row = m_idx * rows_per_model

        for i, batch in enumerate(batches):
            r_off = i // ncols
            c = i % ncols
            ax = axs[base_row + r_off, c]

            df_nasa = load_one_batch(model, "NASA", batch)
            df_dqdv = load_one_batch(model, "NASA_dqdv", batch)
            df = pd.concat([df_nasa, df_dqdv], ignore_index=True)

            if df.empty:
                ax.set_title(f"{model} — batch {batch} (no data)", fontsize=9)
                ax.axis("off")
                continue

            used_axes.append(ax)

            sns.violinplot(
                x="metric", y="error", hue="dataset", data=df,
                order=metric_order, density_norm="count",
                inner="point", dodge=True, saturation=1,
                palette=palette_ds, linewidth=0, ax=ax
            )

            for j, metric in enumerate(metric_order):
                for k, ds in enumerate(datasets):
                    s = df[(df["dataset"] == ds) & (df["metric"] == metric)]["error"]
                    if s.empty:
                        continue
                    mean, std = s.mean(), s.std()
                    offset = 0.21
                    x_pos = j + (k == 1) * offset - (k == 0) * offset
                    ax.plot([x_pos, x_pos], [mean - std, mean + std], color="black", linewidth=0.5)
                    ax.plot([x_pos - 0.15, x_pos + 0.15], [mean, mean], color="red", linewidth=0.6)

            ax.set_title(f"{model} — batch {batch}", fontsize=10)
            ax.set_xlabel(None)
            ax.set_ylabel("Error")
            ax.yaxis.set_major_formatter(mtick.FuncFormatter(percent_fmt))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

            leg = ax.get_legend()
            if leg is not None:
                leg.remove()

        for j in range(len(batches), rows_per_model * ncols):
            r_off = j // ncols
            c = j % ncols
            axs[base_row + r_off, c].axis("off")

    if used_axes:
        handles, labels = used_axes[0].get_legend_handles_labels()

        plt.tight_layout(rect=[0, 0, 1, 0.90])

        fig.legend(handles, labels,
                   ncol=len(datasets),
                   loc="upper center",
                   bbox_to_anchor=(0.5, 0.95),
                   frameon=False,
                   borderaxespad=0.0,
                   columnspacing=1.6,
                   handlelength=2.0,
                   labelspacing=0.8)
    else:
        plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    out_png = savedir / "Compare_NASA_dqdv.png"
    out_pdf = savedir / "Compare_NASA_dqdv.pdf"
    plt.savefig(out_png, dpi=300, bbox_inches="tight", pad_inches=0.12)
    with PdfPages(out_pdf) as pdf:
        pdf.savefig(fig, bbox_inches="tight", pad_inches=0.12)
    # plt.show()
    plt.close(fig)

print(f"Saved PNG: {out_png}")
print(f"Saved PDF: {out_pdf}")
