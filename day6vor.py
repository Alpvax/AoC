from loadFile import loadfile
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plot

if __name__ == "__main__":
  points = [p.split(",") for p in loadfile(6)]
  vor = Voronoi(points, qhull_options="Qbb Qc")
  print(vor.regions)
  regions = [r for r in vor.regions if -1 not in r]
  voronoi_plot_2d(vor)
  plot.show()
