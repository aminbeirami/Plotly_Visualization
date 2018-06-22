import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

labels = ['Dynamic','Clustering']
colors = ['rgba(67,67,67,1)','rgb(199, 86, 35)' ,'rgba(115,115,115,1)', 'rgba(49,130,189, 1)']
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

def line_visualization(x_data,y_data):
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
		title = 'Cost of Finding Optimal Segmentations for Multiple Snapshots',
		titlefont = dict(
			family = 'Arial',
			size = 20,
		),
		xaxis = dict(
			title = 'Number of Snapshots',
			titlefont = dict(
				family = 'Arial',
				size = 20,
			),
			showline = False,
			showgrid = False,
			showticklabels = True,
			linecolor = 'rgb(204, 204, 204)',
			linewidth = 1,
			autotick = False,
			ticks = 'outside',
			tickcolor = 'rgb(204, 204, 204)',
			tickwidth = 1,
			dtick = 5,
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
				yshift = 10,
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

def calc_percentage(base,part):
	return 100 * float(part)/float(base)


def bar_visualization_dynamic(x_data,y_data):
	x_data = x_data[::3]
	y_data = y_data[::3]
	data = [go.Bar(
		x = x_data,
		y = y_data,
		name = 'Cost',
		width = 1.7,
		marker = dict(
			color = colors[1],
		)
	)]

	layout = go.Layout(
		title = 'Cost of Queries With Increasing Number of Snapshots',
		titlefont = dict(
			family = 'Arial',
			size = 20,
		),
		autosize = False,
		width = 1200,
		height = 800,
		xaxis = dict(
			title = 'Number of Snapshots',
			tickvals = x_data
		),
		yaxis = dict(
			title = 'Overall Cost',
		)
	)

	annotations = []

	annotation_data =[]
	for i in range(len(y_data)):
		annotation_data.append(round(100*(float(y_data[i])/float(y_data[0])),2))
	
	for i in range(len(y_data)):
		annotations.append(dict(x = x_data[i], 
								y = y_data[i], 
								text = '{0}%'.format(annotation_data[i]),
								showarrow = False,
								yshift =10
							))

	layout['annotations'] = annotations
	fig = go.Figure(data=data, layout = layout)
	plot(fig)

def bar_visualization_compare(x_data,y_data):
	tick_data = x_data[0][0][::2]
	data = []
	names = ['Clustering 300 iterations','Clustering 5 iterations']
	bar_color = ['rgb(55, 83, 109)','rgb(26, 118, 100)']
	for i in range(len(x_data)):
		data.append(
			go.Bar(
				x = x_data[i][0][::2],
				y = y_data[i][0][::2],
				name = names[i],
				marker = dict(
					color = bar_color[i],
				)
			)
		)
	layout = go.Layout(
		title = 'Overall cost using clustering for segmentation, in various iterations',
		barmode = 'group',
		xaxis = dict(
			title = 'Number of Snapshots',
			tickvals = tick_data
		),
		yaxis = dict(
			title = 'Overall Cost',
		),
		autosize = False,
		width = 1200,
		height = 800,
		legend = dict(
			x=0.8,
			y=1,
			traceorder = 'normal',
			font = dict(
				family = 'sans-serif',
				size =  20,
				color = '#000'
			),
			bgcolor = '#E2E2E2',
			bordercolor = '#FFFFFF',
			borderwidth = 3
		)
	)

	fig = go.Figure(data = data, layout = layout)
	plot(fig)

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
	line_visualization(x_data,y_data)

def query_data():
	snap_files = ['dynamic_multiquery_time.txt','multiqueryCluster_time.txt']
	x_data = []
	y_data = []
	for i in range(len(snap_files)):
		x_data.append([])
		y_data.append([])
	for i in range(len(snap_files)):
		x_data[i].append(read_data(snap_files[i])['first_dim'])
		y_data[i].append(read_data(snap_files[i])['second_dim'])
	line_visualization(x_data,y_data)

def runtime():
	file = ['runtime.txt',]
	x_data = []
	y_data = []
	for i in range(len(file)):
		x_data.append([])
		y_data.append([])
		x_data[i].append(read_data(file[i])['first_dim'])
		y_data[i].append(read_data(file[i])['second_dim'])
	line_visualization(x_data,y_data)

def multisnap_dyn_cost():
	snap_cost_file = 'multisnapDyn.txt'
	snap_cost_data = read_data(snap_cost_file)
	x_data = snap_cost_data['first_dim']
	y_data = snap_cost_data['second_dim']
	bar_visualization_dynamic(x_data,y_data)
	
def dyn_clust_cost():
	cost_files = ['multisnapDyn.txt','multisnapCluster.txt']
	x_data = []
	y_data = []
	for i in range(len(cost_files)):
		x_data.append([])
		y_data.append([])
	for i in range(len(cost_files)):
		x_data[i].append(read_data(cost_files[i])['first_dim'][:40])
		y_data[i].append(read_data(cost_files[i])['second_dim'][:40])
	bar_visualization_compare(x_data,y_data)

def query_clustering():
	names = ['multiqueryCluster_time.txt','multiQueryCluster_poor2.txt']
	x_data = []
	y_data = []
	for i in range(len(names)):
		x_data.append([])
		y_data.append([])
	for j in range(len(names)):
		x_data[j].append(read_data(names[j])['first_dim'])
		y_data[j].append(read_data(names[j])['second_dim'])
	line_visualization(x_data,y_data)

def snapshot_clustering():
	names = ['multisnapCluster.txt','multisnapCluster_poor.txt']
	x_data = []
	y_data = []
	for i in range(len(names)):
		x_data.append([])
		y_data.append([])
	for j in range(len(names)):
		x_data[j].append(read_data(names[j])['first_dim'])
		y_data[j].append(read_data(names[j])['second_dim'])
	bar_visualization_compare(x_data,y_data)

def snapshot_clustering_time():
	names = ['multisnapCluster_time.txt','multisnapCluster_time_poor.txt']
	x_data = []
	y_data = []
	for i in range(len(names)):
		x_data.append([])
		y_data.append([])
	for j in range(len(names)):
		x_data[j].append(read_data(names[j])['first_dim'])
		y_data[j].append(read_data(names[j])['second_dim'])
	line_visualization(x_data,y_data)

def what_to_visualize(name):
	items = {
		'runtime': runtime,
		'snapshot_timing': snapshots_data,
		'query_timing' : query_data,
		'snapshot_costs': multisnap_dyn_cost,
		'dynamic_vs_clustering_cost': dyn_clust_cost,
		'compare_clustering_queries': query_clustering,
		'compare_clustering_snap_cost': snapshot_clustering,
		'compare_clustering_snap_time':snapshot_clustering_time
	}
	items[name]()

what_to_visualize('query_timing')
