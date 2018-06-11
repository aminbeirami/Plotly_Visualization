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
	snapshots = {'recursive':[],'dynamic':[],'clustering':[]}
	snapshots['recursive'].append(read_data('recursive_multisnap.txt'))
	snapshots['dynamic'].append(read_data('dynamic_multisnap.txt'))
	snapshots['clustering'].append(read_data('multisnapCluster.txt'))
	return snapshots

def query_data():
	queries = {'recursive':[],'dynamic':[],'clustering':[]}
	queries['recursive'].append(read_data('recursive_multiquery.txt'))
	queries['dynamic'].append(read_data('multiQueryDyn.txt'))
	queries['clustering'].append(read_data('multiQueryCluster.txt'))
	return queries

def visualize_snapshots():
	snap_data = snapshots_data()
	recursive = go.Scatter(
		x = snap_data['recursive'][0]['first_dim'],
		y = snap_data['recursive'][0]['second_dim'],
		mode = 'lines+markers',
		name = 'recursive'
	)

	dynamic = go.Scatter(
		x = snap_data['dynamic'][0]['first_dim'],
		y = snap_data['dynamic'][0]['second_dim'],
		mode = 'lines+markers',
		name = 'dynamic'
	)

	clustering = go.Scatter(
		x = snap_data['clustering'][0]['first_dim'],
		y = snap_data['clustering'][0]['second_dim'],
		mode = 'lines+markers',
		name = 'clustering'
	)
	
	data = [recursive,dynamic]
	
	layout = go.Layout(
		title = 'Cost of Segment Creation for Multiple Snapshots',
		yaxis = dict(
			title = 'Cost',
			showgrid = True,
			zeroline=False,
	        gridcolor='#bdbdbd',
	        gridwidth=1,
	        linewidth=0
		),
		xaxis = dict(
			title = 'Number of Snapshots'
		),
		legend = dict(
			x=0.8,
			y=1,
			traceorder = 'normal',
			font = dict(
				family = 'sans-serif',
				size =  25,
				color = '#000'
			),
			bgcolor = '#E2E2E2',
			bordercolor = '#FFFFFF',
			borderwidth = 3
		)
	)
	
	fig = go.Figure(data = data,layout = layout)
	plot(fig)

visualize_snapshots()