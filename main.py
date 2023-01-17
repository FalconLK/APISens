'''
Query Examples:
    ArrayDeque
    NodeList
    ArrowType
    ServiceLoader
    ToolTipManager
    Serializer
    CompletableFuture
    MethodHandles
    NumberFormat
    MethodHandle
    AttributedString
    ImageIO
    AssertionError
    IntStream
    ThreadPool
    SortedSet
    ByteBuffer
    ThreadLocal
    RegularExpression
    JAXB
    EventHandler
    BigDecimal
    DateFormatter
    ThreadPoolExecutor
'''

import PySimpleGUI as sg
import matplotlib.pyplot as plt

from utils import getPickleData
from PlotComponent import showPlots

twitter_logo_path = r'Logos/3434_twitter__.png'
youtube_logo_path = r'Logos/4934_youtube.png'

_VARS = {'window': False,
         'fig_agg': False,
         'pltFig': False,
         'dataSize': 20}
plt.style.use('Solarize_Light2')

AppFont = 'Any 16'
SliderFont = 'Any 14'
sg.theme('black')

layout = [
            [
                sg.ProgressBar(max_value=475, size=(100, 20), key='progressbar', bar_color='black')
            ],
            [
                sg.InputText(default_text='Search query ...', text_color='grey', key='input', enable_events=True, font=('Arial', 20), pad=(250, 10), size=100, background_color='white', focus=True, change_submits=True, do_not_clear=True)
            ],
            [
                sg.Image(filename=twitter_logo_path, size=(34, 34), pad=((20, 0), (10, 10)), background_color='#FDF6E3'),
                sg.Button('Search', font=('Arial', 20), button_color=('white', '#000000'), image_size=(100,100), pad=((15, 0), (10, 10))),
                sg.Image(filename=youtube_logo_path, size=(49, 34), pad=((13, 0), (10, 10)), background_color='#FDF6E3'),

                # sg.Image(filename=logo_path, key=0, size=(50,50))
                # sg.Column(image, size=(200, 200)),
                # sg.Column([image], size=(200, 200))

            ],
            [
                # sg.Text(key='scoreCanvas', text='No results', background_color='#FDF6E3', size=(30, 6))
                # sg.List(values=['No results'], size=(30, 6), key='-RESULTS-')
                sg.Text('Twitter Sentiment Score', justification='left', text_color='grey', background_color='white', font=('Arial', 20), size=(30, 3), key='-OUTPUT-TWITTER', enable_events=True),
                sg.Text('Youtube Sentiment Score', justification='left', text_color='grey', background_color='white', font=('Arial', 20), size=(30, 3), key='-OUTPUT-YOUTUBE', enable_events=True)
            ],
            # [sg.Text('Text 1'), sg.Text('Text 2')],
            [
                # sg.Text('*The Twitter score is ranged between 0 to 10.', justification='right', text_color='black', background_color='#FDF6E3', font=('Arial', 15), pad=((0, 450), (0,0)), size=(100, 1), key='annotation_twitter'),
                # sg.Text('*The Youtube score is the absolute numbers.', justification='right', text_color='black', background_color='#FDF6E3', font=('Arial', 15), pad=((0, 0), (0,0)), size=(100, 1), key='annotation_youtube')
                sg.Text('*The Twitter score is ranged between 0 to 10.', justification='left', text_color='black', background_color='#FDF6E3', pad=((140, 0), (0, 0)), font=('Arial', 15), size=(40, 1), key='annotation_twitter'),
                sg.Text('*The Youtube score is the median values.', justification='left', text_color='black', background_color='#FDF6E3', pad=((30, 0), (0, 0)), font=('Arial', 15), size=(40, 1), key='annotation_youtube')
            ],
            # [sg.Column([image], size=(200, 200))],
            [
                sg.Canvas(key='figCanvas', background_color='#FDF6E3', pad=((0,0),(0,0)), size=(50,20))
            ],
            [
                sg.Text(key='SizeArranger', text="Sample size :", font=SliderFont, background_color='#FDF6E3', pad=((0, 0), (10, 0)), text_color='Black'),
                sg.Slider(range=(5, 80), orientation='h', size=(34, 20), default_value=_VARS['dataSize'], background_color='#FDF6E3', text_color='Black', key='-Slider-', enable_events=True, trough_color='black'),
                # sg.Button('Resample', font=AppFont, pad=((4, 0), (10, 0)))
            ],
            [
                sg.Button('Exit', font=AppFont, pad=((750, 0), (0, 0)))
            ]
]

_VARS['window'] = sg.Window('API Sentiment Analysis with Twitter and Youtube', layout, size=(950, 800), finalize=True, resizable=True, location=(0, 0), element_justification="center", background_color='#FDF6E3')

def updateData(val):
    _VARS['dataSize'] = val
    # updateChart()
    showPlots(values["input"], _VARS)

def youtube_retrieval(search_query):
    data_path = 'youtube_results/dict_api_type_median.pkl'
    # result_dict[api_name] = ((like_median, like_median_avg), (view_median, view_median_avg), (comment_median, comment_median_avg))
    obj_dict = getPickleData(data_path)
    api_like_median = obj_dict[search_query][0][0]
    api_view_median = obj_dict[search_query][1][0]
    api_comment_median = obj_dict[search_query][2][0]
    return [api_like_median, api_view_median, api_comment_median]

def tweet_retrieval(search_query):
    data_path = 'twitter_results/api_avg_score_dict.pkl'
    obj_dict = getPickleData(data_path)
    avg_score = obj_dict[search_query][0]
    return avg_score

showPlots('example', _VARS)

while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Search':
        print(f'Searching for: {values["input"]}')
        showPlots(values["input"], _VARS)
        tweet_score = tweet_retrieval(values["input"])
        youtube_scores = youtube_retrieval(values["input"])

        if tweet_score > 0 and len(youtube_scores) > 0:
            _VARS['window'].FindElement('-OUTPUT-TWITTER').Update('Sentiment score: %s' % str(tweet_score))
            _VARS['window'].FindElement('-OUTPUT-YOUTUBE').Update('Likes: %s\nViews: %s\nComments: %s' % (str(youtube_scores[0]), str(youtube_scores[1]), str(youtube_scores[2])))

    elif event == '-Slider-':
        updateData(int(values['-Slider-']))

    elif event == 'Resize':
        _VARS['window']['InputText'].update(font=('Arial', _VARS['window'].current_size()))
        _VARS['window']['Button'].update(font=('Arial', _VARS['window'].current_size()))
_VARS['window'].close()