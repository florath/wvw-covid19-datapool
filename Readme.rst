Datapool of COVID-19 cases
++++++++++++++++++++++++++

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

Database
========

The database provides data from different sources about COVID-19.  The
data is unified (has the same format) and converted to JSON.

REST Interface
==============

TBD.

Data Sources
============

TBD.

Deploymen
=========

.. code:: bash

   gcloud app deploy dbsync/app.yaml --project wirvsvirushackathon-271718
   gcloud app deploy dbsync/cron.yaml --project wirvsvirushackathon-271718

   gcloud app logs tail -s default --project wirvsvirushackathon-271718


Thanks
======

Thanks to the whole team ID#1757 of WirVsVirus for support and help
and many, many links to data sources.

Thanks to Google for supporting this project by providing cloud
resources on `Google Cloud`_ for database and WEB services.

.. _Google Cloud: https://cloud.google.com/


..  LocalWords:  WirVsVirus Hackathon
