import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


def build_graphics():
    graph_data = pd.read_csv('out/names_buyer_rgb.csv', sep='\t', encoding='utf-8')
    del graph_data['photos']
    print(pd.unique(graph_data['Buyer'].values))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    color_R = []
    color_G = []
    color_B = []
    for i in range(len(graph_data)):
        graph_data.loc[i, 'RGB'] = graph_data.loc[i, 'RGB'].rstrip(']').lstrip('[').split()
        color_R.append(float(graph_data.loc[i, 'RGB'][0]))
        color_G.append(float(graph_data.loc[i, 'RGB'][1]))
        color_B.append(float(graph_data.loc[i, 'RGB'][2]))



        # изменять вид отображения различных покупателей здесь (см. вывод):
        if str(graph_data.loc[i, 'Buyer']) == 'Shara Sundberg (sharasundberg)':
            m = 's'; c = 'green'
        elif str(graph_data.loc[i, 'Buyer']) == 'Eva María Laguna Sobrevela (evamaria373)':
            m = 's'; c = 'black'
        elif str(graph_data.loc[i, 'Buyer']) == 'Keri4321':
            m = 's'; c = 'yellow'
        elif str(graph_data.loc[i, 'Buyer']) == 'susano6133':
            m = 's'; c = 'red'
        else:
            m = 'o'; c = 'blue'


        ax.scatter(color_R[i], color_G[i], color_B[i], color=c, marker=m)

    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')

    def animate(i):
        ax.view_init(elev=20., azim=i)
        return fig,

    anim = animation.FuncAnimation(fig, animate, frames=360, interval=20, blit=True)
    anim.save('results_video/basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()
