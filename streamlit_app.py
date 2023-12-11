# import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from itertools import combinations
# import bokeh
import holoviews as hv
from holoviews import opts, dim
# hv.extension("matplotlib")
hv.extension('bokeh', logo=False)
hv.output(size=300)

"""
# Welcome to the interactive plot to analyse XAI4BCI!

This application helps visualise the variable categories for each axis of the XAI4BCI design space.

A chord diagram is a graphical method of displaying the relationships between data in a matrix. 
It is used to visualize the connections or relationships between a finite set of entities. 
The entities are represented as circular segments, and the connections between them are illustrated using ribbons or chords. 
The entities are represented as circles around the perimeter of the diagram, each circle corresponds to an individual entity. 
The chords are the arcs connecting pairs of entities. The width of the chord may be used to represent the strength or frequency 
of the relationship between the connected entities. The input is a matrix, where the rows and columns correspond to the entities, 
and the matrix entries represent the strength or frequency of the relationships between them. The color represents the different 
entities around the disk. The colors are chosen arbitrarily.

Click on the circular symbol adjacent to each design space variable category to 
find the strength of correlated works with other design space variables.
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
# print(nodes.columns)
# nodes.name = nodes.name.str.wrap(15,break_long_words=False)
nodes_hv = hv.Dataset(nodes, 'index')
# nodes_hv.data.index
# nodes_hv.columns

# def rotate_label(plot, element):    
#     labels = plot.handles["labels"]
#     for annotation in labels:        
#         angle = annotation.get_rotation()
#         annotation.set_size(20)
#         if 90 < angle < 270:
#             annotation.set_rotation(180 + angle)
#             annotation.set_horizontalalignment("right")
            

def font_size(plot, element):
    labels = plot.handles["labels"]
    for annotation in labels:
        annotation.set_size(20)
def rotate_label(plot, element):
    white_space = "  "
    angles = plot.handles['text_1_source'].data['angle']
    print(plot.handles['text_1_source'].data)
    
    x_vals = np.array(plot.handles['text_1_source'].data['x'])
    y_vals = np.array(plot.handles['text_1_source'].data['y'])
    plot.handles['text_1_source'].data['x'] = np.array([x*1.5 if x in x_vals[np.where((angles < -1.5707963267949) | (angles > 1.5707963267949))] else x for x in plot.handles['text_1_source'].data['x']])
    # plot.handles['text_1_source'].data['y'] = np.array([x + 0.1 if x in y_vals[np.where((angles < -1.5707963267949) | (angles > 1.5707963267949))] else x for x in plot.handles['text_1_source'].data['y']])
    
    characters = np.array(plot.handles['text_1_source'].data['text'])
    plot.handles['text_1_source'].data['text'] = np.array([x + white_space if x in characters[np.where((angles < -1.5707963267949) | (angles > 1.5707963267949))] else x for x in plot.handles['text_1_source'].data['text']])
    plot.handles['text_1_source'].data['text'] = np.array([white_space + x if x in characters[np.where((angles > -1.5707963267949) | (angles < 1.5707963267949))] else x for x in plot.handles['text_1_source'].data['text']])
    angles[np.where((angles < -1.5707963267949) | (angles > 1.5707963267949))] += 3.1415926535898
    # plot.handles['text_1_source'].text_align = "left"
    
    
# labels = [ '\n'.join(wrap(l, 20)) for l in df.name]
chord = hv.Chord((linkdf, nodes_hv))#.select(value=(5, None))
chord.opts(
    opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(), 
               labels='name', node_color=dim('index').str()))#,hooks=[rotate_label]))
# chord.opts(fontsize='large')
st.bokeh_chart(hv.render(chord, backend='bokeh'))
