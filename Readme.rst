Datapool of COVID-19 cases
++++++++++++++++++++++++++

**The project is in beta phase. Interface changes might occur.**

PLEASE HELP!
============

Currently many important decisions are made based on incomplete or
wrong numbers. Please help to improve the situation!

* Find credible data sources
* Check if sources can be used (legal, license, sensible data, ...)
* If you are a programmer: write an adapter to convert the data
  into the locally used JSON format


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
mail or by fax is currently not included (because this would exceed
the capacity of the RKI?).  Therefore complete regions might have much
higher numbers.


For the Impatient
=================

This is not the recommended way - but the only currently
implemented.  So stay in touch for possible changes.

Get complete data sets. Return JSON list of arrays of dicts. Two data
sets are currently implemented: 

.. code:: bash

   curl https://wirvsvirushackathon-271718.appspot.com/v1/get_all/cases/source/ecdc_xlsx >data.json

   curl https://wirvsvirushackathon-271718.appspot.com/v1/get_all/cases/source/johns_hopkins_github >data.json

A JSON list with two elements is returned: the first element is the
license of the data,the second element is the data set itself, which
is in turn a list of dicrionaries which key value pairs.
   

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
        "location": [
          "US",
          "Virginia",
          "Franklin City",
          "51620"
        ]
      }
    }


REST Interface
==============

TBD.

Add: last updated timestamp


Deployment
==========


Deploy in Google Cloud with Your Account
----------------------------------------

**This solution uses the Google Cloud App Engine.  The Google Cloud
App Engine is not for free - you have to pay for it.  Especially the
number of calls, used CPU, outbound network traffic, ... costs.**

#. Create GCloud project; the name will be referenced as
   WVV_GCLOUD_PROJECT
#. Set Native mode for Firestore for this project to a region in the
   near where the data will be used.
#. Set a service account name. This must be between 6 and 30
   characters long. Example:
   :code:`export WVV_GCLOUD_SERVACC=$(echo servacc-${WVV_GCLOUD_PROJECT} | cut -c -30)`
#. Create a service account
   :code:`gcloud iam service-accounts create ${WVV_GCLOUD_SERVACC} --project ${WVV_GCLOUD_PROJECT}`
#. Grant permissions
   :code:`gcloud projects add-iam-policy-binding ${WVV_GCLOUD_PROJECT} --member "serviceAccount:${WVV_GCLOUD_SERVACC}@${WVV_GCLOUD_PROJECT}.iam.gserviceaccount.com" --role "roles/owner" --project ${WVV_GCLOUD_PROJECT}`
#. Create key file:
   :code:`gcloud iam service-accounts keys create ${WVV_GCLOUD_SERVACC}.json --iam-account "${WVV_GCLOUD_SERVACC}@${WVV_GCLOUD_PROJECT}.iam.gserviceaccount.com"`
#. Set the environment variable:
   :code:`export GOOGLE_APPLICATION_CREDENTIALS="${PWD}/${WVV_GCLOUD_SERVACC}.json"`
#. Create task queue:
   :code:`gcloud tasks queues create data-import --project ${WVV_GCLOUD_PROJECT}`
   :code:`gcloud tasks queues update data-import --max-attempts=1 --project ${WVV_GCLOUD_PROJECT}`
   :code:`gcloud tasks queues update data-import --max-dispatches-per-second=1 --project ${WVV_GCLOUD_PROJECT}`
#. Deploy the application to the App Engine:
   :code:`gcloud app deploy dbsync/app.yaml --project ${WVV_GCLOUD_PROJECT}`
#. Deploy the cron tab to the App Engine:
   :code:`gcloud app deploy dbsync/cron.yaml --project ${WVV_GCLOUD_PROJECT}`
#. Debugging: have a lock at the logs
   :code:`gcloud app logs tail -s default --project ${WVV_GCLOUD_PROJECT}`

Note: the initial maximum runtime length of a task in a Cloud Task is 10 minutes.
This can be increased upto 24 hours.
https://cloud.google.com/tasks/docs/dual-overview


Deploy in Project's Google Cloud
--------------------------------

This is restricted to the people who work in this project.

This is mostly exactly the same as deploying using your own account,
except that there is no need to create the project and Firestore
database.

The project name:

.. code:: bash

   export WVV_GCLOUD_PROJECT=wirvsvirushackathon-271718


Data Sources
============

ecdc: European Centre for Disease Prevention and Control
--------------------------------------------------------

ID: :code:`ecdc-xlsx`

https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

This is a collection of world wide infected and deaths data.
The original data set contains two location information: the country
and the ISO code.  The ISO code is used as `adm[0]`, the country is in
`original.location`.

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

**THIS DATA SET IS CURRENTLY NOT AVAILABLE**

**THE DATA FROM THE ORIGINAL SOURCE IS CURRENTLY ONLY
PARTIAL AVAILABLE AND IS CURRENTLY NOT AUTOMATICALLY UPDATED.**

The French government provides a set of data which does not only
include the number of infected and deaths, but also the number of
people in hospital or on intensive care unit.

https://www.data.gouv.fr/en/datasets/donnees-relatives-a-lepidemie-du-covid-19/

The data is under 'Open License Version 2.0'.

Original data downloaded from https://www.data.gouv.fr/en/datasets/donnees-relatives-a-lepidemie-du-covid-19
on 2020-03-24.


Hospital Numbers
................

Data path:

.. code::

   cases/sources/gouv-fr-hospital-numbers

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


Database Layout
===============

This is only for those who are interesed in: for a 'normal' user there
is no need for this.

.. code::

   covid19datapool (collection)
   |- test (document) [Environment]
      |- source1 (collection) [Example: johns_hopkins_github]
      |  |- metadata (document) [Contains: license, last download, ...]
      |  |- data (document)
      |     |- collection (collection)
      |     |  |- data entry 1 (documents)
      |     |  |- data entry 2 (documents)
      |- source2 (collection) [Example: ecdc_xlsx]
      |  |- metadata (document) [Contains: license, last download, ...]
      |  | --- same as above ---
      prod (document) [Environment]
      |   --- same as above ---

The initial idea to have a worldwide unified database can currently
not be implemented.  There are too many uncertainties and unknowns
which data set possible includes another.  Therefor for the time
being, the data is only unified and converted to JSON.


..  LocalWords:  WirVsVirus Hackathon
