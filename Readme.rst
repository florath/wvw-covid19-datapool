Datapool of COVID-19 cases
++++++++++++++++++++++++++

**THIS PROJECT IS CURRENTLY UNDER DEVELOPMENT AND NOT YET USABLE**

**THE PROJECT IS IN A PROVE ON CONCEPT PHASE - EVERYTHING MIGHT CHANGE**

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


Warning & Use of data
=====================

Before using this database read the documentation of the data which
you want to use!  A lot data **is** incorrect or not what you expect.

E.g. 'infected' mostly does not mean the number of really infected
people but the number of **known** infected people - which has a high
correlation to how many test are carried out and which people are
tested (which differs from country to country).

Another example: in the data from the German RKI the 'recovered'
numbers are only a lower bound because recovery needs not to be
reported officially.

And a third example: The German RKI data contains only the cases which
were transmitted electronically.  Data which is transmitted by snail
mail or by fax is currently not included because this would exceed the
capacity of the RKI.  Therefore complete regions might have much
higher numbers.


Database
========

The database provides data from different sources about COVID-19.  The
data is unified (has the same format) and converted to JSON.

Layout
------

.. code::

   cases (collection)
   |- data (document)
      |- primary (collection)
      |  |- case data (infected, recovered, deaths, tests, ...) (documents)
      |
      |- secondary (collection)
         |- collections (document)
            |- source1 (collection)
            |  |- data (documents)
            |- source2 (collection)
            |  |- data (documents)

The reason for having a top level 'primary' and 'secondary' collection
is, that some sources (e.g. Johns Hopkins data set) is already a
collection of other data sets.  Merging primary and secondary in one
collection is incorrect because it might lead to double counted
cases.

REST Interface
==============

TBD.


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
#. Deploy the application to the App Engine:
   :code:`gcloud app deploy dbsync/app.yaml --project ${WVV_GCLOUD_PROJECT}`
#. Deploy the cron tab to the App Engine:
   :code:`gcloud app deploy dbsync/cron.yaml --project ${WVV_GCLOUD_PROJECT}`
#. Debugging: have a lock at the logs
   :code:`gcloud app logs tail -s default --project ${WVV_GCLOUD_PROJECT}`
	 

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

Data path:

.. code::

   cases/secondary/ecdc-xlsx

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

Data path:

.. code::

   cases/secondary/johns-hopkins-github

https://github.com/CSSEGISandData/COVID-19

This is a collection and aggregation of many other data sources.

List of data sources and Terms of Use can be found on the above WEB page.

To convert the 'unusual' location information, the table which was
created during the WirVsVirusHackathon, was used as the initial base:

https://docs.google.com/spreadsheets/d/1hequqFkVIsF_BCMm4IlHJAWmHI7EcVbV4PvSPQu7hpc/edit#gid=1514093616

Currently only a mapping of the country is done - as the region
mapping is not yet available.


Thanks
======

Thanks to the whole team ID#1757 of WirVsVirus for support and help
and many, many links to data sources.

Thanks to Google for supporting this project by providing cloud
resources on `Google Cloud`_ for database and WEB services.

.. _Google Cloud: https://cloud.google.com/


..  LocalWords:  WirVsVirus Hackathon
