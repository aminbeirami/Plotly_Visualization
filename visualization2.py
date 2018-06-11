import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go


labels = ['Recursive','Dynamic Programming','Clustering']
colors = ['rgba(67,67,67,1)', 'rgba(115,115,115,1)', 'rgba(49,130,189, 1)']
mode_size = [8, 8, 12, 8]

def read_data(filename):
	raw_data = []
	data = {'first_dim':[],'second_dim':[]}
	with open('data/{0}'.format(filename)) as f:
		for items in f:
			raw_data.append(items.translate(None,'\n'))
		for i in range(len(raw_data)):
			data['first_dim'].append(raw_data[i].split(',')[0])
			data['second_dim'].append(raw_data[i].split(',')[1])
	return data


def snapshots_data():
	snap_files = ['recursive_multisnap.txt','dynamic_multisnap.txt','multisnapCluster_time.txt']
	x_data = []
	y_data = []
	for i in range(len(snap_files)):
		x_data.append([])
		y_data.append([])
	for i in range(len(snap_files)):
		x_data[i].append(read_data(snap_files[i])['first_dim'])
		y_data[i].append(read_data(snap_files[i])['second_dim'])
	return x_data,y_data

def query_data():
	snap_files = ['recursive_multiquery.txt','dynamic_multiquery.txt','multisnapCluster_time.txt']
	x_data = []
	y_data = []
	for i in range(len(snap_files)):
		x_data.append([])
		y_data.append([])
	for i in range(len(snap_files)):
		x_data[i].append(read_data(snap_files[i])['first_dim'])
		y_data[i].append(read_data(snap_files[i])['second_dim'])
	return x_data,y_data

def visualize_snapshots():
	x_data,y_data = snapshots_data()
	lines_data = []
	for i in range(len(labels)):
		lines_data.append(
			go.Scatter(
				x = x_data[i][0],
				y = y_data[i][0],
				mode = 'lines+markers',
				line = dict(color = colors[i],width = 2),
				connectgaps=True,
			)
		)
		lines_data.append(go.Scatter(
        	x=[x_data[i][0][0], x_data[i][0][-1]],
        	y=[y_data[i][0][0], y_data[i][0][-1]],
        	mode='markers',
       		marker=dict(color=colors[i], size=16)
    	))

	layout = go.Layout(
		xaxis = dict(
			showline = True,
			showgrid = False,
			showticklabels = True,
			linecolor = 'rgb(204, 204, 204)',
			linewidth = 1,
			autotick = False,
			ticks = 'outside',
			tickcolor = 'rgb(204, 204, 204)',
			tickwidth = 1,
			ticklen = 5,
			tickfont = dict(
				family = 'Arial',
				size = 12,
				color = 'rgb(82, 82, 82)',
			),
		),
		yaxis=dict(
			title = 'Cost',
			titlefont = dict(
				family = 'Arial',
				size = 20,
			),
	    	showgrid=False,
	    	zeroline=False,
	    	showline=True,
	    	showticklabels=True,
	    	linecolor = 'rgb(204, 204, 204)',
	    	tickcolor = 'rgb(204, 204, 204)',
	    ),
	    autosize=False,
	    width = 1500,
	    height = 800,
	    margin=dict(
        	autoexpand=False,
        	l=100,
        	r=20,
        	t=50,
    	),
    	showlegend = False,
	)
	annotations = []
	for i in range(len(labels)):
		annotations.append(dict(
				x = x_data[i][0][-1],
				y = y_data[i][0][-1],
				xref = 'x',
				yref = 'y',
				text = labels[i],
				xanchor = 'left',
				xshift = 10,
				showarrow = False,
				font = dict(
					family = 'Arial',
					size = 19,
					color = '#ffffff'
				),
				bordercolor='#c7c7c7',
				borderwidth=2,
				borderpad=4,
				bgcolor=colors[i],
				opacity=0.8
			)
		)

	layout['annotations'] = annotations
	fig = go.Figure(data = lines_data, layout = layout)
	plot(fig)

visualize_snapshots()