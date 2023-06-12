import numpy as np
import matplotlib.pyplot as plt

def visualize_comparison(topics, name_1, values_1, name_2, values_2, path):
    """Visualize a comparison between two sets of values for different topics.
    Args:
        topics (list): A list of topics to visualize.
        name_1 (str): The name associated with values_1.
        values_1 (list): A list of tuples representing the values for name_1.
                        Each tuple should contain values for both calculated and given data.
                        Example: [(calculated_value_1, given_value_1), (calculated_value_2, given_value_2), ...]
        name_2 (str): The name associated with values_2.
        values_2 (list): A list of tuples representing the values for name_2.
                        Each tuple should contain values for both calculated and given data.
                        Example: [(calculated_value_1, given_value_1), (calculated_value_2, given_value_2), ...]
        path (str): The path to save the visualization image.
    Returns:
        None
    """
    X_POSITIONS = np.array([1, 2, 4, 5])
    BAR_WIDTH = 1
    OPACITY = 1
    fig, axs = plt.subplots(len(topics), 1, sharex=True, figsize=(10, 20))
    bars = []
    for p, plot in enumerate(topics):
        values = []
        for t in [0,1]:
            values.append([values_1[p][t], values_2[p][t]])
        for v, value in enumerate(values[0]+values[1]):
            if value != None:
                bars.append(axs[p].bar(X_POSITIONS[v]-BAR_WIDTH/2, np.array(value), BAR_WIDTH, alpha=OPACITY, color='yellow' if v%2==0 else 'purple', label=plot))
            else:
                axs[p].text(X_POSITIONS[v], 0, 'N/A', ha='center', va='bottom', color='red')
        axs[p].set_title(plot, loc='left', fontsize='medium')
        axs[p].ticklabel_format(style='plain')
    plt.subplots_adjust(hspace=0.5)
    plt.xticks(X_POSITIONS, [])
    #plt.suptitle(x=0.5, y=1, t='Comparison')
    fig.text(0.25, 0.9, 'Calculated', va='top', ha='center', fontsize=10, fontweight='bold')
    fig.text(0.75, 0.9, 'Given', va='top', ha='center', fontsize=10, fontweight='bold')
    fig.text(0.5, 0, 'Source', ha='center')
    fig.text(1, 0.5, 'Key indicator', va='center', ha='right', rotation='vertical')
    fig.legend(bars, [f'{name_1} (avg)', name_2], loc='upper right')
    plt.savefig(path, bbox_inches='tight')
    #plt.show()
