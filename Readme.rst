Datapool of COVID-19 cases
++++++++++++++++++++++++++

Datapool of COVID-19 data from different sources, refurbished, simple
data structure (JSON), single interface (HTTPS).

**The project is in beta phase. Interface changes might occur.**


Warning & Term of Use
=====================

Before using this database read the documentation of the data which
you want to use!  A lot data of the sources might be incorrect or not
what you expect.  Please double check!

E.g. 'infected' mostly does not mean the number of really infected
people but the number of **known** infected people - which has a high
correlation to how many test are carried out and which people are
tested (which differs from country to country).

Another example: in the data from the German RKI the 'recovered'
numbers are only a lower bound because recovery needs not to be
reported officially.

And a third example: The German RKI data contains only the cases which
were transmitted electronically.  Data which is transmitted by snail
mail or by fax is currently not included.  Therefore complete regions
might have much higher numbers.


For the Impatient
=================

Get complete data sets:

.. code:: bash

   curl https://covid19datapool.appspot.com/v1/get_all/ecdc_xlsx

   curl https://covid19datapool.appspot.com/v1/get_all/johns_hopkins_github

Data format:

.. code-block:: JSON

   data[0]: "meta information - name, license, last update, ..."
   data[1]: "list of dicts"

Example:

.. code-block:: JSON

   [
     {
       "name": "2019 Novel Coronavirus ...",
       "license": {
          "text": "This GitHub repo ..."
      },
      "id": "johns_hopkins_github",
      "last_updated": 1585332042.294029,
      "url": "https://github.com/CSSEGISandData/COVID-19"
     },
     [
       {
         "recovered": 0,
         "location": {
           "wgs84": {
             "longitude": -86.04051873,
             "latitude": 34.04567266
           },
           "iso-3166-1-alpha2": "US"
         },
         "deaths": 0,
         "source": "johns_hopkins_github",
         "confirmed": 0,
         "timestamp": 1585093051,
         "original": {
           "location": [ "US", "Alabama", "Etowah", "01055" ]
        }
       },
     ...


This is not the recommended way accessing data - but the only currently
implemented.  So stay in touch for possible changes and extensions:
especially filters are planned.


PLEASE HELP!
============

Currently many important decisions are made based on incomplete or
wrong numbers. Please help to improve the situation!

* Find credible data sources
* Check if sources can be used (legal, license, sensible data, ...)
* If you are a programmer: write an adapter to convert the data
  into the locally used JSON format


Introduction
============

This datapool (database) tries to collect data from different sources
and provides them (refurbished) as a simple to use REST interface.

This project was founded during the WirVsVirus_ Hackathon of the
German government which took place from 2020-03-20 until 2020-03-22.

.. _WirVsVirus: https://wirvsvirushackathon.org/

.. image:: images/WirVsVirusLogoSmall.png
   :alt: "WirVsVirus Hackathon Logo"
   :width: 250

Background
==========

Lots of maps, overviews and numbers that are currently published based
on the data provided by the Johns-Hopkins_ CSSE. For example:
Tagesschau_ or `Berliner Morgenpost`_ [4]. This data is a Hodgepodge
of data from other sources that are 'easy' in one pot to be thrown.

.. _Johns-Hopkins: https://github.com/CSSEGISandData/COVID-19
.. _Tagesschau: https://www.tagesschau.de/ausland/coronavirus-karte-101.html
.. _Berliner Morgenpost: https://interaktiv.morgenpost.de/corona-virus-karte-infektionen-deutschland-weltweit/

An example: 'infected' in the record means that a person who is
infected was tested. Not present in this record are however numbers of
how many tests were run. An 'infected' on 10 tests is different from
an 'infected' on 1000 tests.  Making a meaningfull statement based
on these numbers e.g. the effectiveness of measures (curfew, border
closure, ...) is modern coffee grounds reading.

The goal of this project is to search for existing data sources,
convert them and make them available to all who are interested in -
especially as an alternative and extension of the benefits
Johns-Hopkins data. Not every person who wants to research, compile
statistics or calculate a new model would need to take care of the
many and complex details, but can get started right away.

Because: every institution, authority, state, health department offers
the data in its own form:nicely presented - but for further processing
and analysis completely unsuitable.  Add to that the license terms
which are, at best, are unknown. All Germans Health departments of the
federal states have Copyright on the case numbers, which makes it
impossible to use, process or pass them on.

There are also some records of hospitalization from COVID-19 infected
the French government. Based on this data, the Markov transition
probabilities in the last paper_ from the RKI can be checked (page 4,
Fig 1). If it would be possible to make more precise and substantiated
statements here about estimates of the dark figure ('infected but not
tested').  (Example: Would the model published by the RKI, which is
not country-specific, applied in Italy, you would currently get there
to over 700,000 infected.)

.. _paper: https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Modellierung_Deutschland.pdf?__blob=publicationFile


Features
========

* Automatically updated every some hours from the given sources
* Unified and easy to use JSON formatted data
* Data can directly be retrieved using HTTPS from a database
  (sort and filter actions will shortly follow)


Database
========

The database provides data from different sources about COVID-19.  The
data is unified (has the same format) and converted to JSON.


Data
----

Each data set **can** contain the following keys, i.e. most of the
fields are optional:

* timestamp: interger; seconds since EPOCH
* deaths: integer
* indected: integer
* recovered: integer
* source: string; the source of the data
* location: dict;
  
  - iso-3166-1-alpha2: 2 chars
  - wgs84: { longitute: latitude: }: coordinates

* original: dictionary; random data of the original data set
  which is (currently) not mapped

Example:

.. code-block:: JSON

    {
      "recovered": 0,
      "location": {
        "wgs84": {
          "longitude": -76.93859681,
          "latitude": 36.6831435
        },
        "iso-3166-1-alpha2": "US"
      },
      "deaths": 0,
      "source": "johns_hopkins_github",
      "confirmed": 0,
      "timestamp": 1585179199,
      "original": {
        "location": [ "US", "Virginia", "Franklin City", "51620" ]
      }
    }


REST Interface
==============

TBD.



Data Sources
============

ecdc: European Centre for Disease Prevention and Control
--------------------------------------------------------

ID: :code:`ecdc-xlsx`

https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

This is a collection of world wide infected and deaths data.
The original data set contains two location information: the country
and the ISO code.

Terms of Use for this data set can be found on the above WEB page.

Excerpt:

*Users of ECDC public-use data files must comply with data use
restrictions to ensure that the information will be used solely for
statistical analysis or reporting purposes.* 


Johns Hopkins GitHub
--------------------

ID: :code:`johns_hopkins_github`

https://github.com/CSSEGISandData/COVID-19

This is a collection and aggregation of many other data sources.

List of data sources and Terms of Use can be found on the above WEB page.

To convert the 'unusual' location information, the table which was
created during the WirVsVirusHackathon, was used as the initial base:

https://docs.google.com/spreadsheets/d/1hequqFkVIsF_BCMm4IlHJAWmHI7EcVbV4PvSPQu7hpc/edit#gid=1514093616

Currently only a mapping of the country is done - as the region
mapping is not yet available.


data.gouv.fr
------------

**THIS IS WORK IN PROGRESS!! THIS DATA SET IS NOT YET AVAILABLE**

The French government provides a set of data which does not only
include the number of infected and deaths, but also the number of
people in hospital or on intensive care unit.

https://www.data.gouv.fr/en/datasets/donnees-relatives-a-lepidemie-du-covid-19/

The data is under 'Open License Version 2.0'.

Original data downloaded from https://www.data.gouv.fr/en/datasets/donnees-relatives-a-lepidemie-du-covid-19


Hospital Numbers
................

ID: :code:`gouv_fr_hospital_numbers`

This data set contains information how many people are currently in
hospital, how many are in critical care, how many died.

Example:

.. code-block:: JSON

  {
    "adm": [
      "FR",
      "45"
    ],
    "sex": "m",
    "released_from_hospital_total": 3,
    "hospitalized_current": 19,
    "critical_care_current": 9,
    "deaths_total": 0,
    "timestamp": 1584831600
  }


References
==========

Tidying the new Johns Hopkins Covid-19 time-series datasets
-----------------------------------------------------------

URL: https://joachim-gassen.github.io/2020/03/tidying-the-new-johns-hopkins-covid-19-datasests/

The first step looks very similar to the current implementation here:
tidy up the data, mapping regions / countries to ISO codes, ...


Thanks
======

Thanks to the whole team ID#1757 of WirVsVirus for support and help
and many, many links to data sources.

Thanks to Google for supporting this project by providing cloud
resources on `Google Cloud`_ for database and WEB services.

.. _Google Cloud: https://cloud.google.com/

..  LocalWords:  WirVsVirus Hackathon
