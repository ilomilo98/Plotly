#Importing libraries

import dash
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_table

#dataframe
df = pd.read_csv('/Users/ilaydakursun/Downloads/Dataset3.csv', sep = ';')
df_=df[df['Level of development']=='Developing']
#Dash
app = dash.Dash(__name__ , meta_tags=[{"name": "viewport", "content": "width=device-width"}],external_stylesheets=[dbc.themes.BOOTSTRAP])


#Define figures here
#map
map_fig = px.choropleth(
        df,
        locations='Country',
        color='Women Entrepreneurship Index',
        geojson='https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson',
        featureidkey='properties.name',
        color_continuous_scale='Purpor',
    )
map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


#Comparison figure histogram
eindex = df[['Country','Women Entrepreneurship Index', 'Entrepreneurship Index']]
eindex = eindex.groupby(by = 'Country').agg(sum)
egroup_index = eindex[['Women Entrepreneurship Index', 'Entrepreneurship Index']].sort_values(by = 'Entrepreneurship Index')

fig = go.Figure()
fig.add_trace(go.Bar(
    y=egroup_index['Entrepreneurship Index'].values,
    x=egroup_index.index,
    name='Entrepreneurship Index',
    marker_color='#112E4B'
))
fig.add_trace(go.Bar(
    y=egroup_index['Women Entrepreneurship Index'].values,
    x=egroup_index.index,
    name='Women Entrepreneurship Index',
    marker_color='#47C2FF'
))
fig.update_traces(orientation = 'v')
fig.update_layout(title = '<b>Entrepreneurship  Index </b> and <b>Women Entrepreneurship Index</b> per country', template="none")

#box
fig_box3 = px.box(df, x = df['European Union Membership'], y = df['Women Entrepreneurship Index'], template="ggplot2",width=850,
        height=600)

#pie
fig_pie1 = px.pie(df_, values='Female Labor Force Participation Rate', names='Country', title = '<b>Female Labor Force Participation Rate in Developing Countries<b>',width=850,
        height=600)

#scatter
fig_scatter = px.scatter(df, x="Female Labor Force Participation Rate", y="Women Entrepreneurship Index", size="Entrepreneurship Index", color="Level of development",
           hover_name="Country", template="plotly_white", width=900,
        height=600)

#Distplot
hist_data = [df['Female Labor Force Participation Rate'].values]
group_labels = ['Female Labor Force Participation Rate']
fig_dist = ff.create_distplot(hist_data, group_labels,curve_type='normal')
fig_dist.update_layout(title = 'Female Labor Force Participation Rate Distribution', template="ggplot2", width=1000,
        height=600)

#Layout
app.title = 'Women Entrepreneurship and Labor Force'
app.layout = html.Div(children=[
		html.Div(children = [ 
		dbc.NavbarSimple(
		    children=[
			dbc.NavItem(dbc.NavLink("Web Portal", href="#")),
		    ],
		    brand="Women Entrepreneurship and Labor Force",
		    brand_href="#",
		    color="#001524",
		    dark=True,)],style={'width': '100%'}
		    ),
		
		html.Div( children = [
		dcc.Graph(id='map', figure=map_fig),
		],style={'width':'100%','margin': '2% 0px 0px 0px'}),
		
		html.Div(children=[dcc.Graph(id='subplot', figure=fig),],style={'margin': '5px 1% 0px 1%', 'width':'100%'}),
		#html.Div(children=[dcc.Graph(id='boxplot1', figure=fig_pie),],style={'margin': '1% 1% 0px 10%'}),
	    	#html.Div(children=[dcc.Graph(id='boxplot2', figure=fig_pie),],style={'margin': '1% 1% 0px 10%'}),
	    	html.Div(children=[dcc.Graph(id='boxplot3', figure=fig_pie1),],style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 20, 'marginBottom': 50, 
               'backgroundColor':'#F7FBFE'}),
               #'border': 'thin lightgrey dashed', 'padding': '6px 0px 0px 8px'}),
	    	html.Div(children=[dcc.Graph(id='boxplot4', figure=fig_box3),],style={'margin': '1% 1% 0px 10%'}),
		html.Div(children=[dcc.Graph(id='pop', figure=fig_scatter),],style={'margin': '1% 1% 0px 10%'}),
		html.Div(children=[dcc.Graph(id='Distplot', figure=fig_dist),],style={'margin': '1% 1% 0px 10%'}),

		html.Div([
	        dash_table.DataTable(id='table-multicol-sorting',
		columns=[
		{"name": i, "id": i} for i in df.columns
	    ],
	    page_current=0,
	    page_size=10,
	    page_action='custom',
	    sort_action='custom',
	    sort_mode='multi',
	    sort_by=[]
	    )],style={'width': '100%','margin': '1% 5% 10px 5%'}),
],style={'display': 'flex','flex-direction': 'row','flex-wrap': 'wrap','overflow': 'hidden'})


#Callbacks 
#Dash Table
@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "page_current"),
     Input('table-multicol-sorting', "page_size"),
     Input('table-multicol-sorting', "sort_by")])
def update_table(page_current, page_size, sort_by):
    print(sort_by)
    if len(sort_by):
        dff = df.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=False)
