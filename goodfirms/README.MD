README
======

Description
-----------

Get information about companies from "https://www.goodfirms.co"

Install
-------

Requirement version of Python == 3.5.2

        $ virtualenv -p /usr/bin/python3 ENV_NAME
        $ . ./ENV_NAME/bin/activate
        (ENV_NAME)$ pip install -r requirements.txt


Using
-----

        (ENV_NAME)$ python goodfirms.py

Function get_scrap(url) take url on the one of catagories and make an output file with data.
Function scrap_company(url) take url on the addition company information and return list of needed attrs.

We got 6 categories and 6 output files.
