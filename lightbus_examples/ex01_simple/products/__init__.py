import dataset

# Create a simple database using the 'dataset' library
db = dataset.connect('sqlite:///products_app.sqlite', engine_kwargs=dict(connect_args=dict(check_same_thread=False)))
