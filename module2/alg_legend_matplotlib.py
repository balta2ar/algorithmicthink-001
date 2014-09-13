"""
Short example of creating a legend in matplotlib
"""

import matplotlib.pyplot as plt


def legend_example():
    """
    Plot an example with two curves with legends
    """
    xvals = [1, 2, 3, 4, 5]
    yvals1 = [1, 2, 3, 4, 5]
    yvals2 = [1, 4, 9, 16, 25]

    plt.plot(xvals, yvals1, '-b', label='linear')
    plt.plot(xvals, yvals2, '-r', label='quadratic')
    plt.legend(loc='upper right')
    plt.show()

legend_example()
