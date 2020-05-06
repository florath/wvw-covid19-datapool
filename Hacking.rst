Deployment
==========

Deploy in Google Cloud with Your Account
----------------------------------------

**This solution uses the Google Cloud App Engine.  The Google Cloud
App Engine is not for free - you have to pay for it.  Especially the
number of calls, used CPU and outbound network traffic costs real
world money.**

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
   :code:`gcloud app deploy dbquery/app.yaml --project ${WVV_GCLOUD_PROJECT}`
   :code:`gcloud app deploy dbsync/app.yaml --project ${WVV_GCLOUD_PROJECT}`
   :code:`gcloud app deploy dispatch.yaml --project ${WVV_GCLOUD_PROJECT}`
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

There are two projects - one for testing and one for production:

The test project:

.. code:: bash

   export WVV_GCLOUD_PROJECT=wirvsvirushackathon-271718

The production project:

.. code:: bash

   export WVV_GCLOUD_PROJECT=covid19datapool

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

PLEASE HELP!
============

Currently many important decisions are made based on incomplete or not
correctly interpreted numbers. Please help to improve the situation!

* Find credible data sources
* Check if sources can be used (legal, license, sensible data, ...)
* Let us know (open an issue)
* If you are a programmer: write an adapter to convert the data
  into the locally used JSON format - and create a pull request.
