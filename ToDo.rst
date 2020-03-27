Cleanup and Basics
++++++++++++++++++

* Add another level in DB for different use cases (e.g. production,
  pre-production, test, development, ...)

* Unify location information.
  Suggestion:

  location: {
    iso-3166-1-alpha2: CC
    iso-3166-2: REGC

    wgs84: {
      longitude: -4.5555
      latitude: 7.877
      }
    }

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

There are many data sources. Some might be included here in the database.

https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

Maybe: use the sources of Johns-Hopkins directly:

https://github.com/CSSEGISandData/COVID-19

Here is a list of data sources (under Datensätze / Links):

https://docs.google.com/document/d/1DMAisYOtO1RZU7OVzppxrlRGVhjzJNq3eRiKbNHKC-g/edit?ts=5e754850#

Landesgedundheitsämter:

https://www.heise.de/newsticker/meldung/Corona-Statistik-in-Deutschland-Noch-mehr-Durcheinander-4687788.html
