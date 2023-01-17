import os, time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_empty_plot(_VARS):
    fig, ax = plt.subplots()
    _VARS['pltFig'] = plt.figure(facecolor='#FDF6E3', figsize=(10, 3))
    # # plot an empty line
    # line, = ax.plot([], [], linestyle='None', marker='o')
    #
    # # set the x and y axis limits
    # ax.set_xlim(-1, 10)
    # ax.set_ylim(-1, 10)

    dataXY = ['0', '0']
    # plt.plot(dataXY[0], dataXY[1], '.k')
    plt.bar(dataXY[0], dataXY[1])
    _VARS['fig_agg'] = draw_figure(_VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def drawBars(labels, likes, comments, _VARS):
    _VARS['fig_agg'].get_tk_widget().forget()
    x = np.arange(len(labels))  # the label locations
    width = 0.4  # the width of the bars
    plt.rcParams.update({'font.size': 12})

    fig, ax = plt.subplots()
    _VARS['pltFig'] = plt.figure(facecolor='#FDF6E3', figsize=(9, 5))

    ax = plt.gca()
    ax.set_facecolor('#FDF6E3')
    rects1 = ax.bar(x - width / 2, likes, width, label='Likes', color='red')
    rects2 = ax.bar(x + width / 2, comments, width, label='Comments', color='black')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Counts')
    ax.set_xlabel('Video Indices')
    ax.set_title('Likes and Comments Counts')
    ax.set_xticks(x, labels)
    ax.legend()

    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    # plt.show()
    _VARS['fig_agg'] = draw_figure(_VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

def showPlots(target_api, _VARS):
    from utils import getPickleData
    from collections import defaultdict
    def default_dict_list():
        return defaultdict(list)
    filter = 1000
    if target_api == 'example':
        draw_empty_plot(_VARS)
        return

    src_path = 'pack/'
    dic = defaultdict(default_dict_list)

    for idx, pkl_file in enumerate(os.listdir(src_path)):
        _VARS['window']['progressbar'].UpdateBar(idx)
        api_name = pkl_file.split('.')[0]

        obj = getPickleData(src_path + pkl_file)
        for index, row in obj.iterrows():
            dic[api_name]['like'].append(row['like'])
            dic[api_name]['view'].append(row['view'])
            dic[api_name]['comment'].append(row['comment'])

    likes = dic[target_api]['like']
    likes = [int(i) for i in likes]
    ignore_idx_list = list()
    for idx, i in enumerate(likes):
        if i > filter:
            ignore_idx_list.append(idx)
    likes = [int(i) for idx, i in enumerate(likes) if not idx in ignore_idx_list][:_VARS['dataSize']]

    comments = dic[target_api]['comment']
    comments = [int(i) for idx, i in enumerate(comments) if not idx in ignore_idx_list][:_VARS['dataSize']]

    labels = [str(i) for i in range(len(likes))]

    drawBars(labels, likes, comments, _VARS)