import numpy as np
import matplotlib.pyplot as plt
import os

def visualize_comparison(topics, name_1, values_1, name_2, values_2):

    x = np.array([1, 2, 4, 5])
    bar_width = 1
    opacity = 1
    fig, axs = plt.subplots(len(topics), 1, sharex=True, figsize=(10, 20))
    bars = []

    for p, plot in enumerate(topics):
        values = []
        for t in [0,1]:
            values.append([values_1[p][t], values_2[p][t]])
        print(values, '\n')
        for v, value in enumerate(values[0]+values[1]):
            if value != None:
                bars.append(axs[p].bar(x[v]-bar_width/2, np.array(value), bar_width, alpha=opacity, color='yellow' if v%2==0 else 'purple', label=plot))
            else:
                axs[p].text(x[v], 0, 'N/A', ha='center', va='bottom', color='red')
        axs[p].set_title(plot, loc='left', fontsize='medium')
        axs[p].ticklabel_format(style='plain')

    plt.subplots_adjust(hspace=0.5)
    plt.xticks(x, [])
    #plt.suptitle(x=0.5, y=1, t='Comparison')
    fig.text(0.25, 0.9, 'Calculated', va='top', ha='center', fontsize=10, fontweight='bold')
    fig.text(0.75, 0.9, 'Given', va='top', ha='center', fontsize=10, fontweight='bold')
    fig.text(0.5, 0, 'Source', ha='center')
    fig.text(1, 0.5, 'Key indicator', va='center', ha='right', rotation='vertical')
    fig.legend(bars, [f'{name_1} (avg)', name_2], loc='upper right')
    plt.savefig(os.path.join(os.path.dirname(__file__), '../assets/charts/Comparison.png'), bbox_inches='tight')
    plt.show()
