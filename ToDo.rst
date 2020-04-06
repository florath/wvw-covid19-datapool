Cleanup and Basics
++++++++++++++++++

* Transaction check:
  is updarte running?

* RKI: update + synchronize complete
  update: do not remove data!

* Include WHO data

* Include italien data

* Include spanisch data

* ECDC: use (new) JSON instead if propriatary xlsx
  Currently some data is TWICE!

* ECDC: updated license

* ECDC: unclear if data is cummulated or day by day


* The Johns-Hopkins date included some 'unassinged'
  How do we handle this?

  41059,Umatilla,Oregon,US,2020-03-28 23:05:37,45.59073056,-118.7353826,4,0,0,0,"Umatilla, Oregon, US"
  ,Unassigned,Alaska,US,2020-03-28 23:05:37,0.0,0.0,0,1,0,0,"Unassigned, Alaska, US"
  ,Unassigned,Arizona,US,2020-03-28 23:05:37,0.0,0.0,0,4,0,0,"Unassigned, Arizona, US"
  ,Unassigned,Arkansas,US,2020-03-28 23:05:37,0.0,0.0,32,4,0,0,"Unassigned, Arkansas, US"
  ,Unassigned,Colorado,US,2020-03-28 23:05:37,0.0,0.0,136,1,0,0,"Unassigned, Colorado, US"
  ,Unassigned,Florida,US,2020-03-28 23:05:37,0.0,0.0,0,8,0,0,"Unassigned, Florida, US"
  ,Unassigned,Georgia,US,2020-03-28 23:05:37,0.0,0.0,230,2,0,0,"Unassigned, Georgia, US"
  ,Unassigned,Hawaii,US,2020-03-28 23:05:37,0.0,0.0,4,0,0,0,"Unassigned, Hawaii, US"
  ,Unassigned,Illinois,US,2020-03-28 23:05:37,0.0,0.0,8,0,0,0,"Unassigned, Illinois, US"
  ,Unassigned,Kentucky,US,2020-03-28 23:05:37,0.0,0.0,150,0,0,0,"Unassigned, Kentucky, US"
  ,Unassigned,Louisiana,US,2020-03-28 23:05:37,0.0,0.0,9,1,0,0,"Unassigned, Louisiana, US"
  ,Unassigned,Maine,US,2020-03-28 23:05:37,0.0,0.0,3,0,0,0,"Unassigned, Maine, US"
  ,Unassigned,Maryland,US,2020-03-28 23:05:37,0.0,0.0,0,1,0,0,"Unassigned, Maryland, US"
  ,Unassigned,Massachusetts,US,2020-03-28 23:05:37,0.0,0.0,356,9,0,0,"Unassigned, Massachusetts, US"
  ,Unassigned,Michigan,US,2020-03-28 23:05:37,0.0,0.0,47,0,0,0,"Unassigned,Michigan,US"
  ,Unassigned,Nevada,US,2020-03-28 23:05:37,0.0,0.0,93,0,0,0,"Unassigned, Nevada, US"
  ,Unassigned,New Jersey,US,2020-03-28 23:05:37,0.0,0.0,2478,86,0,0,"Unassigned, New Jersey, US"
  ,Unassigned,New York,US,2020-03-28 23:05:37,0.0,0.0,0,109,0,0,"Unassigned, New York, US"
  ,Unassigned,Rhode Island,US,2020-03-28 23:05:37,0.0,0.0,107,2,0,0,"Unassigned, Rhode Island, US"
  ,Unassigned,Tennessee,US,2020-03-28 23:05:37,0.0,0.0,161,4,0,0,"Unassigned, Tennessee, US"
  ,Unassigned,Vermont,US,2020-03-28 23:05:37,0.0,0.0,7,7,0,0,"Unassigned, Vermont, US"
  ,Unassigned,Washington,US,2020-03-28 23:05:37,0.0,0.0,0,0,0,0,"Unassigned, Washington, US"
  ,Unassigned,Wisconsin,US,2020-03-28 23:05:37,0.0,0.0,0,0,0,0,"Unassigned, Wisconsin, US"
  47171,Unicoi,Tennessee,US,2020-03-28 23:05:37,36.10890856,-82.43709629,1,0,0,0,"Unicoi, Tennessee, US"

* Reconcile / incremental update
  as two different methods to implement.

* Remove ids/data which is no longer valid

* Problem: find a sensible hirachical administration data structure of the world.
  
* ToDo: Johns-Hopkins data: add iso-3166-2 field

* Add number of data rows into metadata

* All information in the original dataset is copied
  (with appropriate documention) to the 'original' key.

* Cleanup Readme
  + Generel: Remove all limitations - we are productive!
  + For each source: create an own document and reference from the Readme.
  
* To fulfill the license, there is the need to add some
  meta-information, like

  {
     source: URL
     download_ts: 193833939
     license: {
       name: GPL3
       URL: theURLToTheLicense
     }
     description: "Some words"
  }

  This information *must* be included in *every* data-query!

* Cleanup Source Code
  There are *many* duplicates and similarities

* Re-structure the source code:
  + Use modules (run time)
  + Split into subdirectories

* Add CI/CD
  + python tox
  + python pylint
  + python pep8
  + Unit tests
  + Integration tests

* Fix problems with lastest Changes in Johns-Hopkins data set
  (Esp. location mapping)

* Add method to report incomplete imports.

* Delta update in DB:
  Remove possible old / unused / changed datasets


Possible Data Sources
+++++++++++++++++++++

???

https://secure.pt-dlr.de/pt-conference/conference/PROTOTYPEFUND8/




There are many data sources. Some might be included here in the database.

https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

Maybe: use the sources of Johns-Hopkins directly:

https://github.com/CSSEGISandData/COVID-19

Here is a list of data sources (under Datensätze / Links):

https://docs.google.com/document/d/1DMAisYOtO1RZU7OVzppxrlRGVhjzJNq3eRiKbNHKC-g/edit?ts=5e754850#

Landesgedundheitsämter:

https://www.heise.de/newsticker/meldung/Corona-Statistik-in-Deutschland-Noch-mehr-Durcheinander-4687788.html
