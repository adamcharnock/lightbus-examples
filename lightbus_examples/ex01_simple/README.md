Simple Lightbus Project
=======================

Products app                                                                       |  Stock app
:---------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------:
![Products app screenshot](../../static/readme_images/ex01/products.png?raw=true)  |  ![Stock app screenshot](../../static/readme_images/ex01/stock.png?raw=true)

Content
-------

**This example shows how two simple applications can communicate via lightbus.**
The stock application will receive product data from the products application.

This examples shows the following:

* How to define an API (``products/bus.py``)
* How to fire events on an API (``products/web.py``)
* How to listen for events on an API (``stock/bus.py``)
* How to perform a remote procedure call on an API (``stock/bus.py``)

Prerequisites
-------------

You will need the [Redis 4.0 streams branch](https://github.com/antirez/redis/tree/streams) running 
locally. The release of Redis 4.0 is anticipated by the end of 2017.

Running
-------

Each application has two processes. The first is the web server 
which provides the web interface. The second is the lightbus 
process, which responds to remote procedure calls (RPCs) and 
listens for events. This gives a total of four processes.

In the future we will look at ways of combining each application's
web and lightbus processes into one via asyncio. However, for now 
we will keep things simple.

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

Your terminals will also look something like this:

![Products app screenshot](../../static/readme_images/ex01/terminals.png?raw=true)

A Note on Implementation
------------------------

The code in these examples is written to be concise, simple, and 
readable. To these ends much has been sacrificed, including security.
Don't look to these examples for web development best practices.

