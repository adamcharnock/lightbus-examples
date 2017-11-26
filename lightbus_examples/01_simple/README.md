Initial Example Project
=======================

This example project contains two web servers, 
neither of which contain any lightbus functionality.
*We will build upon this project in subsequent examples.*

The web servers are as follows:

* ``products.py`` — for managing your companies product catalog
* ``stock_levels.py`` — for managing the stock level of each product

You should run both in separate terminal windows:
    
```bash
    # Run in terminal window 1:
    $ python products.py
     
    # Run in terminal window 2:
    $ python stock_levels.py
```

The web servers will be available as follows:

* http://127.0.0.1:8001 – Products
* http://127.0.0.1:8002 – Stock levels

A Note on Implementation
------------------------

The code in these examples is written to be concise, simple, and 
readable. To these ends much has been sacrificed, including security.
Don't look to these examples for web development best practices.
