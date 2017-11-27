# Create a simple database using the 'dataset' library
from uuid import uuid4

import dataset

db = dataset.connect('sqlite:///stock_app.sqlite', engine_kwargs=dict(connect_args=dict(check_same_thread=False)))

if not db['products'].count():
    db['products'].insert(dict(uuid=uuid4().hex, name='Widget 1'))
    db['products'].insert(dict(uuid=uuid4().hex, name='Widget 2'))
