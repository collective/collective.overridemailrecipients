Introduction
============

collective.overridemailrecipients forwards all mails sent from Plone. Use this package on testing and development environments where you want to test emails sent thru Plone, but not want to use the real addresses.

This package is always active by patching. The recipient(s) in the 'To' header are replaced by 'plone@localhost' or configurable mail address.

Features
========

- All emails sent thru the Plone mailer are forwarded to one mail address
- Bcc and Cc headers are stripped

Installation
============

To your `buildout.cfg`, add::

    eggs =
        ...
        collective.overridemailrecipients

After that, just install via the "Add-on" controlpanel.

Usage
=====

After installation this packages is configurable thru the site setup

- Email address, this address is used to forward mails to
- Enabled or disable or disable mail forwardind

TODO
====

- Create tests
- Add to, cc and bcc in forwarded mail

Contributors
============
- Pawel Lewicki <lewicki@gw20e.com>
- Kim Chee Leong <leong@gw20e.com>

