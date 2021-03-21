#
# Created by:
#
# Stanislav Bober
# MIEM NRU HSE
# sbober@hse.ru
# 2020
#

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

cyan = (106/255, 187/255, 191/255)
red = (206/255, 26/255, 2/255)

two_map = LinearSegmentedColormap.from_list('two', [cyan, red], N=2)
red_map = LinearSegmentedColormap.from_list('red', [red, red], N=2)

class selection_plotter(np.ndarray):
    fontsize = 20
    full_map = red_map
    
    def __getitem__(self, s):
        C = np.zeros(self.shape)
        C[s] = 1
        arr = self.base #np.asarray(self)
        if isinstance(self.dtype.type(1), (np.floating, float)):
            fmt = '%.1f'
        elif isinstance(self.dtype.type(1), (np.integer, int)):
            fmt = '%d'
        else:
            fmt = '%r'
        if self.ndim == 1:
            ax1 = plt.gca()
            for i in range(self.shape[0]):
                ax1.text(i, 0, fmt % arr[i],
                         fontsize=selection_plotter.fontsize,
                         ha="center", va="center", 
                         color="w", weight='bold')
            m = selection_plotter.full_map if C.all() else two_map
            ax1.imshow(C.reshape(1,-1), cmap=m)
            ax1.set_yticks([])
            ax1.set_xticks(list(range(self.shape[0])))
            ax1.set_xlabel('indexes')
        elif self.ndim == 2:
            plt.xticks(range(self.shape[1]))
            plt.yticks(range(self.shape[0]))
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    text = plt.text(j, i, fmt % arr[i, j],
                                    fontsize=selection_plotter.fontsize,
                                    ha="center", va="center", 
                                    color="w", weight='bold')
            m = selection_plotter.full_map if C.all() else two_map
            plt.imshow(C, cmap=m)
            plt.ylabel('rows')
            plt.xlabel('columns')
        elif self.ndim == 3:
            norm = plt.Normalize(C.min(), C.max())
            x = self.shape[0]
            ax = plt.gcf().get_axes()
            if not hasattr(ax, '__len__') or (hasattr(ax, '__len__') and len(ax) < 3):
                _, ax = plt.subplots(1, x)
            for k in range(x):
                arr2d = arr[k]
                for i in range(self.shape[1]):
                    for j in range(self.shape[2]):
                        text = ax[k].text(j, i, fmt % arr2d[i, j],
                                          ha="center", va="center", 
                                          color="w", weight='bold')
                ax[k].imshow(C[k], cmap=two_map, norm=norm)
                ax[k].set_ylabel('y (columns)')
                ax[k].set_xlabel('z')
                ax[k].set_title(f'x (row) = {k}')
            plt.suptitle(selection2str(s))
            plt.tight_layout()
            
        return arr[s]
    
    def __repr__(self):
        return self.base.__repr__()
		
class selection_plotter_3d(np.ndarray):
        
    def __getitem__(self, s):
        C = np.zeros(self.shape)
        C[s] = 1
        arr = self.base #np.asarray(self)
        if self.ndim == 3:
            fig = plt.gcf()
            #fig.delaxes(plt.gca())
            ax = [fig.add_axes([0.1, 0.1, 0.7, 0.7], zorder=3, facecolor=(1,1,1,0.5)),
                  fig.add_axes([0.2, 0.2, 0.7, 0.7], zorder=2, facecolor=(1,1,1,0.5)),
                  fig.add_axes([0.3, 0.3, 0.7, 0.7], zorder=1, facecolor=(1,1,1,0.5))]            
            norm = plt.Normalize(C.min(), C.max())
            x = self.shape[0]
            for k in list(range(x))[::-1]:
                arr2d = arr[k]
                for i in range(self.shape[1]):
                    for j in range(self.shape[2]):
                        text = ax[k].text(j, i, arr2d[i, j],
                                          ha="center", va="center", 
                                          color="w", weight='bold',
                                          alpha=1)
                cmap = red_map if (C == 1).all() else two_map
                ax[k].imshow(C[k], cmap=cmap, norm=norm, alpha=0.8)
                ax[k].set_ylabel('y (columns)')
                ax[k].set_xlabel('z')
                ax[k].set_title(f'x (row) = {k}', 
                                bbox=dict(boxstyle='round', fc="w", ec="k"),
                                ) #backgroundcolor=(1,1,1,0.5))
            
        return arr[s]
    
    def __repr__(self):
        return self.base.__repr__()