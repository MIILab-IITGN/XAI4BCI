import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from itertools import combinations
import bokeh
import holoviews as hv
from holoviews import opts, dim
#hv.extension("matplotlib")
hv.extension('bokeh', logo=False)
#hv.output(size=400)

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

df = pd.read_csv('chord.csv')
df=df.fillna(0)



linkdf = pd.DataFrame(columns=['source', 'target', 'value'])

for col1, col2 in combinations(df.columns,2):
    list_row = [col1, col2,df.loc[(df[col1] ==1) & (df[col2] ==1),col1].sum()]
    linkdf.loc[len(linkdf)] = list_row
#     print(col1,col2)


linkdf.value = linkdf.value.astype(int)
linkdf.target = linkdf.target.astype(int)
linkdf.source = linkdf.source.astype(int)

nodes = pd.read_csv('nodes.csv')
print(nodes.columns)
# nodes.name = nodes.name.str.wrap(15,break_long_words=False)
nodes_hv = hv.Dataset(nodes, 'index')
nodes_hv.data.index
# nodes_hv.columns

def rotate_label(plot, element):    
    labels = plot.handles["labels"]
    for annotation in labels:        
        angle = annotation.get_rotation()
        annotation.set_size(20)
        if 90 < angle < 270:
            annotation.set_rotation(180 + angle)
            annotation.set_horizontalalignment("right")
            

def font_size(plot, element):
    labels = plot.handles["labels"]
    for annotation in labels:
        annotation.set_size(20)
# def rotate_label(plot, element):
#     white_space = "  "
#     angles = plot.handles['text_1_source'].data['angle']
#     characters = np.array(plot.handles['text_1_source'].data['text'])
#     plot.handles['text_1_source'].data['text'] = np.array([x + white_space if x in characters[np.where((angles < -1.5707963267949) | (angles > 1.5707963267949))] else x for x in plot.handles['text_1_source'].data['text']])
#     plot.handles['text_1_source'].data['text'] = np.array([white_space + x if x in characters[np.where((angles > -1.5707963267949) | (angles < 1.5707963267949))] else x for x in plot.handles['text_1_source'].data['text']])
#     angles[np.where((angles < -1.5707963267949) | (angles > 1.5707963267949))] += 3.1415926535898
#     plot.handles['text_1_source'].text_align = "right"
    
    
# labels = [ '\n'.join(wrap(l, 20)) for l in df.name]
chord = hv.Chord((linkdf, nodes_hv))#.select(value=(5, None))
chord.opts(
    opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(), 
               labels='name', node_color=dim('index').str()))#,hooks=[rotate_label]))
# chord.opts(fontsize='large')
st.bokeh_chart(hv.render(chord, backend='bokeh'))
