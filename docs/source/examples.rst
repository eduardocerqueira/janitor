.. _examples:


Examples
========

USAGE:

clean up virtual machines and release floating ips for Openstack keep items declared in the whitelist.txt file:

1. load your Openstack rc
2. run janitor

    source ~/mytenant-openrc.sh
	janitor --openstack --whitelist /tmp/whitelist.txt

or passing openrc as argument:

    janitor openstack --openrc /root/openrc.sh --whitelist /var/lib/jenkins/workspace/janitor/janitor_whitelist.txt --keystone v3

listing history for your janitor:

	janitor --history
