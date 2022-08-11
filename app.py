import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])
mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')
markdown_text = 'The gender wage gap refers to the often-discussed difference in median pay between men and women. While the reasons behind the wage gap are controversial, data show a persistent gap. The General Social Survey is an annual survey conducted since 1972, in which American adults around the country are asked about a variety of topics related to American society and social attitudes.'
gender_table = round(gss_clean.groupby('sex').agg({'income':'mean', 
                                                   'socioeconomic_index':'mean',
                                                   'education':'mean'}),2).reset_index().rename(columns = {'sex':'Sex',
                                                                                                           'income': 'Average Income', 
                                                                                                           'socioeconomic_index':'Average Socioeconomic Index', 
                                                                                                           'education':'Average Years of Education'})
p2_table = ff.create_table(gender_table)
p2_table.show()
breadwinner_table = gss_clean.groupby(['sex', 'male_breadwinner']).agg({'id':'count'}).reset_index()
breadwinner_table
fig1 = px.bar(breadwinner_table, x='male_breadwinner', y='id', color='sex',
            labels={'male_breadwinner':'Response to Question', 'id':'Count'},
            barmode = 'group')
fig1.update_layout(showlegend=True)
fig1.update(layout=dict(title=dict(x=0.5)))
fig1.show()
fig2 = px.scatter(gss_clean, x='job_prestige', y='income', color = 'sex',trendline='ols',
                 height=400, width=800,
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Average Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig2.update(layout=dict(title=dict(x=0.5)))
fig2.show()
fig3 = px.box(gss_clean, x='sex', y = 'income',
                   labels={'sex':'', 'income':'Income'},
            height = 600, width = 600)
fig3.update(layout=dict(title=dict(x=0.5)))
fig3.show()
fig4 = px.box(gss_clean, x='sex', y = 'job_prestige',
                   labels={'sex':'', 'job_prestige':'Job Prestige'},
            height = 600, width = 600)
fig4.update(layout=dict(title=dict(x=0.5)))
fig4.show()
sparse_df = gss_clean[['income','sex','job_prestige']]
sparse_df['binned_prestige'] = pd.cut(sparse_df['job_prestige'],6)
sparse_df = sparse_df.dropna()
fig_bar = px.box(sparse_df, x='sex', y='income', color= 'sex',
             facet_col='binned_prestige', facet_col_wrap=2,
                 color_discrete_map = {'male':'blue', 'female':'red'},
            labels={'income':'Income', 'binned_prestige':'Prestige Category', 'sex':'Sex'},
         width=1000, height=600)
fig_bar.update(layout=dict(title=dict(x=0.5)))
fig_bar.update_layout(showlegend=False)
fig_bar.show()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 


app.layout = html.Div(
    [
        html.H1("GSS Survey Deep Dive Dashboard"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Average Income, Socioeconomic Status, and Job Prestige for Men and Women"),
        
        dcc.Graph(figure=p2_table),
        
        html.H2("Responses to Breadwinner Question by Sex"),
        
        dcc.Graph(figure=fig1),
        
        html.H2("Income by Job Prestige for Men and Women"),
        
        dcc.Graph(figure=fig2),
        
        html.H2('Income for Men and Women'),
        
        dcc.Graph(figure = fig3),
        
        html.H2('Job Prestige for Men and Women'),
        
        dcc.Graph(figure = fig4),
        
        html.H2('Average Income by Job Prestige Category for Men and Women'),
        
        dcc.Graph(figure = fig_bar)
    
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
