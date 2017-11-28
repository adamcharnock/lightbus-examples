Simple Lightbus Project
=======================

This example project contains two applications for 
managing products (``products/``) and stock levels 
(``stock/``).

Each application has two processes. The first is the web server 
which provides the web interface. The second is the lightbus 
process, which responds to remote procedure calls (RPCs) and 
listens for events. This gives a total of four processes.

Content
-------

This examples shows the following:

* How to define an API (``products/bus.py``)
* How to fire events on an API (``products/web.py``)
* How to listen for events on an API (``stock/bus.py``)
* How to perform a remote procedure call on an API (``stock/bus.py``)

Prerequisites
-------------

You will need Redis 4.0 running locally.

Running
-------

You should run each of the following in separate terminal windows:
    
```bash
    # Products web interface (run in terminal 1)
    $ cd products/
    $ FLASK_APP=web.py flask run --port=8001
    
    # Products bus (run in terminal 2)
    $ cd products/
    $ lightbus run
     
    # Stock management web interface (run in terminal 3)
    $ cd stock/
    $ FLASK_APP=web.py flask run --port=8002
    
    # Stock management web interface (run in terminal 4)
    $ cd stock/
    $ lightbus run
```

The web servers will be available as follows:

* http://127.0.0.1:8001 – Products
* http://127.0.0.1:8002 – Stock management

A Note on Implementation
------------------------

The code in these examples is written to be concise, simple, and 
readable. To these ends much has been sacrificed, including security.
Don't look to these examples for web development best practices.
