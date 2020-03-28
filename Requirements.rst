Collecting and providing COVID-19 related data
++++++++++++++++++++++++++++++++++++++++++++++

Use Cases / Requirements
========================

Use of Data
-----------
A user wants to use data which is related to COVID-19.

Description: Somebody wants to create statistics, wants to apply a
model or wants to visualize different aspects of COVID-19. This person
needs access to data related to COVID-19.

Collection of Different Data Sources
------------------------------------
A user wants different types of data or the same data from different
sources at one place. 

Description: Nobody wants to search for days through the internet for
data. The data pool collects different data and provides it to the
user. 

Unified Data Format
-------------------
A user wants to process different data sets in a unified way.

Description: There are many data sources available - but each and
every source uses its own format, e.g. CSV, Google Docs, xlsx, git,
https, ...  The data pool should unify these (preprocess) and provide
one format for all data. 

Possible solution: JSON

Easy to Use Data Access
-----------------------
The data should be easily accessible.

Description: There should be no need for complicated parsing or
protocols or local files. Accessing the data must be easy. 
Possible solution: HTTPS

Programming Language / Tool independent
---------------------------------------
The data format and transfer must be done in a way that it does not
depend on one tool or one programming language. 

High Availability
-----------------
The system must be available at least 99.9%.

High Quality
------------
The system must be implemented in a way that high service quality can
be provided.

Possible solutions: CI/CD system, different instances of the database
(development, test, production), automation 

Legal
-----
The system must comply with all legal aspects.

Examples: Licenses of data must be fulfilled.

