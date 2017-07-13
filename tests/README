RUNNING TESTS
=============

Openstack tests requires you have your openstack tenant openrc.sh file that
provides the Openstack credentials. Janitor's tests reads system
environment variable if you perform a source to your openrc.sh or from a
file that should be placed at janitor/tests/test-openrc.sh. There is a
test-openrc-sample.sh file you can use to start it, just remove -sample or copy
and paste to a new file without -sample and fill out with your credentials.

Also whitelist.txt file is required and should be placed at same place like:
janitor/tests/whitelist.txt

DATA FOR TESTS
---------------

running the openstack nova cli below you can generate content or vms for your
tests:

  nova boot --flavor 2 --key-name mykeyname --image e636fa2e-a1fc-48c0-97c4-04fc74651281 test2


HOW TO RUN ALL TESTS
--------------------

you have to install janitor from branch or version you want to run the tests.
Go to janitor folder and run:

  python -m pytest tests -v


HOW TO RUN AN INDIVIDUAL TEST
-----------------------------

you have to install janitor from branch or version you want to run the tests.
Go to janitor folder and run:

  python -m pytest tests/openstack/test_instances.py -v


ISSUES
------

1. classpath

 if you are having issues with classpath you can try:

 PYTHONPATH=janitor pytest tests/test_openstacksdk.py -v
 PYTHONPATH=janitor pytest tests -v

 on this example I am running the command above from my janitor folder.


REFERENCE LINKS
----------------

http://www.tilcode.com/pytest-cli-tips-tricks-settings/
