# IntersystemsCacheORM
Intersystems Cache Object-Relational Mapper based on [Intersystems Python Binding][4] module

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

[1]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_using
[2]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_classes#GBPY_classes_queries
[3]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_using#GBPY_using_basics
[4]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY
[5]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_classes#GBPY_classes_objects
[6]: https://docs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls?KEY=GBPY_classes#GBPY_classes_database
