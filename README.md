# IntersystemsCacheORM
Intersystems Cache Object-Relational Mapper based on [Intersystems Python Binding][4] module. 

### About CacheORM
This module is an enhanced OOP porting of Intersystems [Cache-Python binding][1]. It serves the purpose of an object-relational mapper in python for Intersystems Cache database There are three classes implemented:

* **CacheClient**
This is the super class of CachePython module. It wraps two functions from intersys.pythonbind module [pythonbind3.connection()][3] and [pythonbind3.database()][6].

* **CacheQuery**
A subclass of CacheClient that wraps methods and adds extra functionality in [intersys.pythonbind.database][6] and [intersys.pythonbind.query][2] classes

* **CacheClass**
A subclass of CacheClient, that wraps methods and adds extra functionality in [intersys.pythonbind.database][6] and [intersys.pythonbind.object][5] classes

The [intersys.pythonbind package][4] is a Python C extension that provides Python application with transparent connectivity to the objects stored in the Caché database.

The Caché Object Server, a high performance server process, manages communication between Python clients and a Caché database server. It communicates using standard networking protocols (TCP/IP), and can run on any platform supported by Caché.

### Source Code
Open and view [cacheorm.py][8]
The code released here was originally written and used as a module of [TRIADB][11] project.

### Tests and Demos
There are two folders in this release:

* testCacheORM contains python jupyter notebook files that demonstrate CacheQuery and CacheClass
* testCacheBinding are tests written for Intersystems Cache python binding

One can simply compare tests with demos to appreciate the work in this project to leverage intersystems cache python binding.

### Documentation
Currently there is no documentation written for the project. Python jupyter notebooks in testCacheORM folder demonstrate the use of CacheQuery and CacheClass. You may also study the code that is well commented (see [cacheorm.py][8]).

### Bonus
I wrote these [SocketReceiver, SocketSender][7]  classes for Python 3 so now it is super easy for anyone to run a simple TCP socket communication test on two Python consoles. This was done in order to capture "writes" from Caché. In that case you need to redirect your IO and write the data to python console.

### Installation
Caché provides client-side Python support through the `intersys.pythonbind` module, which implements the connection and caching mechanisms required to communicate with a Caché server. This module **must be compiled and installed in your environment**. Set up your environment variables to support C compilation and linking, as described in the [installation guide of Intersystems Cache Python Binding][12]. Also make sure that you are using Python 3 interpreter when you run the setup.

If installation is successful the module will be placed under your python site-packages in a folder with the name `pythonbind3-1.0-py3.6-linux-x86_64.egg`. Now you may run any of the [sample programs][13] that are provided by Intersystems Cache to verify that Python interpreter references properly `intersys.pythonbind` module.

Then you can download and try to execute my tests and demos from Github. I have also placed jupyter notebook files at [my Microsoft Azure library][14] and you can **ONLY view them or download and open them locally at your machine** (I think you must login first).

[1]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_using
[2]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_classes#GBPY_classes_queries
[3]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_using#GBPY_using_basics
[4]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY
[5]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_classes#GBPY_classes_objects
[6]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_classes#GBPY_classes_database
[7]: https://github.com/healiseu/IntersystemsCacheORM/blob/master/socket.py
[8]: https://github.com/healiseu/IntersystemsCacheORM/blob/master/cacheorm.py
[9]: https://github.com/healiseu/IntersystemsCacheORM/blob/master/testCacheORM/testCacheORM%20-%20Cache%20Objects%20Test%201.ipynb
[10]: https://github.com/healiseu/IntersystemsCacheORM/blob/master/testCacheORM/testCacheORM%20-%20Cache%20Objects%20Test%202.ipynb
[11]: http://healis.eu/triadb
[12]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_intro#GBPY_intro_install
[13]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_intro#GBPY_intro_samples
[14]: https://notebooks.azure.com/athanassios/libraries/CacheORM
