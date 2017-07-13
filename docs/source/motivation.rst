.. _motivation:


Motivation
==========

One of my Openstack tenants that I use to run tests for an internal tool has
a very limited quota so all the time I need to stop my tests and automations
and spend few minutes cleaning up public/floating ips, destroying
virtual machines and others. The idea to have janitor or a butler is actually
an old idea and a coworker had implemented it but in a more sophisticated
and fashion way this is a simply version and currently only focusing in
Openstack maybe further I'll extend it to AWS, Openshift and others.
