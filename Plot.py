import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd

from SingleCollisionDCF import SingleCollisionDCF
from SingleCollisionVCS import SingleCollisionVCS
from HiddenTerminalDCF import HiddenTerminalDCF
from HiddenTerminalVCS import HiddenTerminalVCS

mpl.rcParams['figure.dpi']= 300
mpl.rc("savefig", dpi=300)

def plot_wrapper(df):
    for metric in get_metrics(df):
        plot_metrics(df, metric)
    
    
def plot_metrics(df, metric):
    if metric == 'NumCollisions':
        label_replacement = 'NumCollisions'
    elif metric == 'NumASuccesses':
        label_replacement = 'Node A Successes'
    elif metric == 'NumCSuccesses':
        label_replacement = 'Node C Successes'
    elif metric == 'AThroughputBits':
        label_replacement = 'Node A Throughput (Kib/sec)'
    elif metric == 'CThroughputBits':
        label_replacement = 'Node C Throughput (Kib/sec)'
    elif metric == 'FairnessIndex':
        label_replacement = 'Fairness Index (ratio)'
    if metric != 'fairness_index':
        ax = sns.lineplot(data=df,x="FrameRate",y=metric, hue="scenario")
        title = f'{label_replacement.split(" (")[0]} as a Function of Frame Rate'
        ax.set_title(title)
        ax.set_ylabel(f'{label_replacement}')
        ax.set_xlabel('Frame Rate (frames/sec)')
        plt.grid(None)
        plt.savefig(f'{title}.png')
        plt.close()
    else:
        ax = sns.lineplot(data=df.tail(10),x="FrameRate",y=metric, hue="scenario")
        title = f'{label_replacement.split(" (")[0]} as a Function of Frame Rate'
        ax.set_title(title)
        ax.set_ylabel(f'{label_replacement}')
        ax.set_xlabel('Frame Rate (frames/sec)')
        plt.grid(None)
        plt.savefig(f'{title}.png')
        plt.close()
        ax = sns.lineplot(data=df.head(10),x="FrameRate",y=metric, hue="scenario")
        title = f'{label_replacement.split(" (")[0]} as a Function of Frame Rate in Scenario A'
        ax.set_title(title)
        ax.set_ylabel(f'{label_replacement}')
        ax.set_xlabel('Frame Rate (frames/sec)')
        plt.grid(None)
        plt.savefig(f'{title}.png')
        plt.close()
    
    
def get_scenarios(df):
    return list(set(df.scenario.values.tolist()))


def get_metrics(df):
    return df.columns.values.tolist()[2:]


def get_x_ticks(df):
    return list(set(df.frame_rate.values.tolist()))
