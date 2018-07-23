"""
This module is an enhanced OOP porting of Intersystems Cache-Python binding.
It serves the purpose of an object-relational mapper in python for Intersystems Cache database
There are three classes implemented:

CacheClient:
This is the super class of CachePython module.
It wraps two functions from intersys.pythonbind module
pythonbind3.connection() and pythonbind3.database().

CacheQuery:
A subclass of CacheClient that wraps methods and adds extra functionality in
intersys.pythonbind.database and intersys.pythonbind.query classes

CacheClass:
A subclass of CacheClient, that wraps methods and adds extra functionality in
intersys.pythonbind.database and intersys.pythonbind.object classes

The intersys.pythonbind package is a Python C extension that provides Python
application with transparent connectivity to the objects stored in the Caché database.

The Caché Object Server, a high performance server process, manages communication
between Python clients and a Caché database server. It communicates using standard
networking protocols (TCP/IP), and can run on any platform supported by Caché.
"""

__version__ = '0.10.0'
__version_update__ = '2018-01-06'
__version_modifications__ =''

__release_version__ = '0.9.0'
__release_date__ = '2018-07-23'
__release_changes__=''
__source_url__=''

__project_started__ = '2017-08-01'
__python_version__ = '>=3.6.0'
__cache_version__ = '2017.1.1.111.0'
__platform__ = 'Linux'

__author__ = 'Athanassios I. Hatzis'
__author_email = 'hatzis@healis.eu'
__organization__="HEALIS (Healthy Information Systems/Services)"
__organization_url="http://healis.eu"
__copyright__ = "Copyright (c) 2017,2018 Athanassios I. Hatzis"
__license__ = " "
__distributor__='Promoted and Distributed by HEALIS'
__distributor_url__='http://healis.eu'
__maintainer__='Athanassios I. Hatzis'
__maintainer_email__='hatzis@healis.eu'
__status__='Production'


from CacheORM.cacheorm import CacheQuery, CacheClass

from CacheORM.socket import SocketSender, SocketReceiver
