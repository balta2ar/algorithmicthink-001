"""
Some provided code for plotting the clusters using matplotlib
"""

import math
# import urllib2
import matplotlib.pyplot as plt


# URLS for various important datasets
# DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DIRECTORY = "data/"
MAP_URL = DIRECTORY + "USA_Counties.png"

# Define colors for clusters.  Display a max of 16 clusters.
COLORS = ['Aqua', 'Yellow', 'Blue', 'Fuchsia', 'Black', 'Green', 'Lime', 'Maroon', 'Navy', 'Olive', 'Orange', 'Purple', 'Red', 'Brown', 'Teal']


# Helper functions
def circle_area(pop):
    """
    Compute area of circle proportional to population
    """
    return math.pi * pop / (200.0 ** 2)


def plot_clusters(data_table, cluster_list, draw_clusters=True, output=None):
    """
    Create a plot of clusters of counties
    """

    fips_to_line = {}
    for line_idx in range(len(data_table)):
        fips_to_line[data_table[line_idx][0]] = line_idx

    # Load map image
    # map_file = urllib2.urlopen(MAP_URL)
    map_file = open(MAP_URL)
    map_img = plt.imread(map_file)

    # Scale plot to get size similar to CodeSkulptor version
    ypixels, xpixels, bands = map_img.shape
    DPI = 60.0                  # adjust this constant to resize your plot
    xinch = xpixels / DPI
    yinch = ypixels / DPI
    plt.figure(figsize=(xinch,yinch))
    implot = plt.imshow(map_img)

    # draw the clusters on the map
#    for cluster_idx in range(len(cluster_list)):
#        cluster = cluster_list[cluster_idx]
#        cluster_color = COLORS[cluster_idx % len(COLORS)]
#        for fips_code in cluster.fips_codes():
#            line = data_table[fips_to_line[fips_code]]
#            plt.scatter(x = [line[1]], y = [line[2]], s =  circle_area(line[3]), lw = 1,
#                        facecolors = cluster_color, edgecolors = cluster_color)

    if draw_clusters:
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.scatter(x = [line[1]], y = [line[2]], s =  circle_area(line[3]), lw = 1,
                            facecolors = cluster_color, edgecolors = cluster_color)

    else:
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            cluster_pop = cluster.total_population()
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            plt.scatter(x = [cluster_center[0]], y = [cluster_center[1]], s =  circle_area(cluster_pop), lw = 1,
                        facecolors = cluster_color, edgecolors = cluster_color)

    if output:
        plt.savefig(output)
    else:
        plt.show()
