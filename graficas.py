import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt


def size_font():
    "Setea fuentes y tamaños"
    size = 5
    font = {'fontname': 'Verdana', 'fontsize': size}
    font_legend = font_manager.FontProperties(family='Arial', style='normal', size=10)
    return size, font, font_legend


def format_spines(color, ax):
    "Formatea spines"
    # oculta ejes superior y derecho
    [ax.spines[x].set_visible(False) for x in ["top", "right"]]
    # color de ejes inferior e izquierdo
    [ax.spines[x].set_color(color) for x in ["bottom", "left"]]

    return None


def format_ticks(labels, color, ind, font):
    "Formatea ticks y etiquetas"
    plt.xticks(ind, labels=labels, **font, color=color)
    plt.yticks(**font, color=color)
    plt.tick_params(axis='y',color=color)
    plt.tick_params(axis='x', bottom=False, labelbottom=True, color=color)

    return None