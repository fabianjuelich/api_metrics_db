import numpy as np
import matplotlib.pyplot as plt
import os

def visualize_comparison(topics, name_1, values_1, name_2, values_2):

    x = np.array([1, 2, 4, 5])
    bar_width = 1
    opacity = 1

    fig, axs = plt.subplots(len(topics), 1, sharex=True, figsize=(10, 20))

    for i, plot in enumerate(topics):
        values = []
        for t, type in enumerate(['Calculated', 'Given']):
            values.append([values_1[i][t], values_2[i][t]])
        print(values, '\n')
        bars = axs[i].bar(x[0:2]-bar_width/2, np.array(values[0]), bar_width, alpha=opacity, color=('yellow', 'purple'), label=plot)
        bars = axs[i].bar(x[2:]-bar_width/2, np.array(values[1]), bar_width, alpha=opacity, color=('yellow', 'purple'), label=plot)
        axs[i].set_title(plot, fontfamily='serif', loc='left', fontsize='medium')

    plt.xticks(x, [])
    plt.suptitle(x=0.5, y=1, t='Comparison')
    fig.text(0.25, 0.9, 'Calculated', va='top', ha='center', fontsize=10, fontweight='bold')
    fig.text(0.75, 0.9, 'Given', va='top', ha='center', fontsize=10, fontweight='bold')
    fig.text(0.5, 0, 'Source', ha='center')
    fig.text(1, 0.5, 'Key indicator', va='center', ha='right', rotation='vertical')
    fig.legend(bars, [f'{name_1} (avg)', name_2], loc='upper right')
    plt.savefig(os.path.join(os.path.dirname(__file__), '../assets/charts/Comparison.png'), bbox_inches='tight')
    plt.show()

# Test
# nasdaq = [(0, 1), (2, 3), (4, 5)]
# msft = [(5, 4), (3, 2), (1, 0)]
# visualize_comparison(['Key figure 1', 'Key figure 2', 'Key figure 3'], 'NASDAQ', nasdaq, 'MSFT', msft)
