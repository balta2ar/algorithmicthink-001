"""
Counting the number of iterations in various mystery functions
"""

import simpleplot
import math

# Plot options
STANDARD = True
LOGLOG = False

# global counter that records the number of iterations for inner loops
counter = 0

###############################################
# three mystery functions
def mystery1(input_val):
    """
    Function whose loops update global counter
    """
    global counter
    for index in range(input_val):
        for dummy_index in range(5):
            counter += 1

def mystery2(input_val):
    """
    Function whose loops update global counter
    """
    global counter
    for index in range(input_val):
        for dummy_index in range(index / 2, index):
            counter += 1

def mystery3(input_val):
    """
    Function whose loops update global counter
    """
    global counter
    for index in range(input_val):
        for dummy_index in range(int(1.1 ** index)):
            counter += 1

def build_plot(plot_size, plot_function, plot_type = STANDARD):
    """
    Build plot of the number of increments in mystery function
    """
    global counter
    plot = []
    for input_val in range(2, plot_size):
        counter = 0
        plot_function(input_val)
        if plot_type == STANDARD:
            plot.append([input_val, counter])
        else:
            plot.append([math.log(input_val), math.log(counter)])
    return plot



###############################################
# plottting code
plot_type = STANDARD
plot_size = 40

# Pass name of mystery function in as a parameter
plot1 = build_plot(plot_size, mystery1, plot_type)
plot2 = build_plot(plot_size, mystery2, plot_type)
plot3 = build_plot(plot_size, mystery3, plot_type)
simpleplot.plot_lines("Iteration counts", 600, 600,
                      "input", "counter", [plot1, plot2, plot3])
