Initial Example Project
=======================

This example project contains two web servers, 
neither of which contain any lightbus functionality.
*We will build upon this project in subsequent examples.*

The web servers are as follows:

* ``products.py`` — for managing your company's product catalog
* ``stock_levels.py`` — for managing the stock level of each product

You should run both in separate terminal windows:
    
```bash
    # Run in terminal window 1:
    $ cd products/
    $ FLASK_APP=web.py flask run --port=8001
     
    # Run in terminal window 2:
    $ cd stock/
    $ FLASK_APP=web.py flask run --port=8002
```

The web servers will be available as follows:

* http://127.0.0.1:8001 – Products
* http://127.0.0.1:8002 – Stock levels

Note that the stock app will not receive any products records 
in this version of the app. This will come in ``ex01_simple``, 
when we begin adding the lightbus functionality.

A Note on Implementation
------------------------

The code in these examples is written to be concise, simple, and 
readable. To these ends much has been sacrificed, including security.
Don't look to these examples for web development best practices.
