Introduction
============

collective.overridemailrecipients prevents sending mail when this is not wanted. When enabled the email addresses of the recipients are changed to a given address.

Features
========

- All emails sent thru the Plone mailer

Installation
============

To your `buildout.cfg`, add::

    eggs =
        ...
        collective.overridemailrecipients

After that, just install via the "Add-on" controlpanel.

Usage
=====

To do
=====

- Event IUsefulnessEvent seems only to be fired for non-folderish items
- Show warning when viewing settings of item that is default view (like Topic
  `aggregator` in News Folder).
- Show number of ratings
- Integrate with collective.contentratings_
- Translate rating value ("Yes"/"No") in content rule e-mail

.. _collective.contentratings: http://pypi.python.org/pypi/plone.contentratings
