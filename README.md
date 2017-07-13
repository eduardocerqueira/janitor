
![copr build](https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/package/janitor/status_image/last_build.png)

# janitor

MOTIVATION
----------

One of my Openstack tenants that I use to run tests for an internal tool has a very limited quota so all the time I need to stop my tests and automations and spend few minutes
cleaning up public/floating ips, destroying virtual machines and others. The idea to have janitor or a butler is actually an old idea and a coworker had implemented
it but in a more sophisticated and fashion way this is a simply version and currently only focusing in Openstack maybe further I'll extend it to AWS, Openshift and others.

WHAT IS THIS
-------------

Linux tool to help clean-up tasks for Openstack.

USAGE

clean up virtual machines and release floating ips for Openstack keep items declared in the whitelist.txt file:

1. load your Openstack rc to system environment variable or pass as parameter
2. run janitor

    source ~/mytenant-openrc.sh

	janitor openstack --whitelist /tmp/whitelist.txt
	janitor openstack --openrc /tmp/mytenant-openrc.sh --whitelist /tmp/whitelist.txt

listing history for your janitor:

	janitor history

DEMO
----

Running the program without parameters:

	[ecerquei@dev ~]$ janitor
	Usage: janitor [OPTIONS] COMMAND [ARGS]...

	  Janitor clean-up the left-over in your Openstack tenant to know more check
	  documentation running: man janitor

	Options:
	  --help  Show this message and exit.

	Commands:
	  history    show janitor history
	  openstack  clean-up VM and public IP from Openstack tenant


Running the program with with parameters to make clean-up:

	[ecerquei@dev ~]$ janitor openstack --openrc /home/ecerquei/git/janitor/tests/test-openrc.sh --whitelist /home/ecerquei/git/janitor/tests/whitelist.txt
	+---------------------+--------------+------------------+-----------------------------+--------------------------------------------+--------+----------------------+
	|      TIMESTAMP      |    ACTION    |       NAME       |             IPs             |                   IMAGE                    | FLAVOR |   CREATED AT (UTC)   |
	+---------------------+--------------+------------------+-----------------------------+--------------------------------------------+--------+----------------------+
	| 2017-07-13 15:00:57 |   deleted    |    QA-DB-100     |        172.16.91.195        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:56:38Z |
	| 2017-07-13 15:00:57 |   deleted    |    DEV-WEB-10    |        172.16.91.194        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:56:24Z |
	| 2017-07-13 15:00:57 |   deleted    |    PROD-APP1     |        172.16.91.193        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:56:10Z |
	| 2017-07-13 15:00:57 |   deleted    | test_123_456_789 |        172.16.91.192        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:55:58Z |
	| 2017-07-13 15:00:57 |   deleted    |    test123456    |        172.16.91.191        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:55:47Z |
	| 2017-07-13 15:00:57 | in whitelist |  jslave_centos   | 172.16.91.173, 10.8.187.160 |            paws-jslave-centos7             |   3    | 2017-07-13T01:02:58Z |
	| 2017-07-13 15:00:57 | in whitelist | jslave_fedora25  | 172.16.91.172, 10.8.187.207 |            paws-jslave-fedora25            |   3    | 2017-07-13T01:02:08Z |
	+---------------------+--------------+------------------+-----------------------------+--------------------------------------------+--------+----------------------+
	+---------------------+---------+--------------+
	|      TIMESTAMP      |  ACTION | FLOATING IP  |
	+---------------------+---------+--------------+
	| 2017-07-13 15:00:57 | deleted | 10.8.180.199 |
	+---------------------+---------+--------------+

Running the program with parameter to print history file:

	[ecerquei@dev ~]$ janitor history
	+---------------------+--------------+------------------+-----------------------------+--------------------------------------------+--------+----------------------+
	|      TIMESTAMP      |    ACTION    |       NAME       |             IPs             |                   IMAGE                    | FLAVOR |   CREATED AT (UTC)   |
	+---------------------+--------------+------------------+-----------------------------+--------------------------------------------+--------+----------------------+
	| 2017-07-13 15:00:57 |   deleted    |    QA-DB-100     |        172.16.91.195        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:56:38Z |
	| 2017-07-13 15:00:57 |   deleted    |    DEV-WEB-10    |        172.16.91.194        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:56:24Z |
	| 2017-07-13 15:00:57 |   deleted    |    PROD-APP1     |        172.16.91.193        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:56:10Z |
	| 2017-07-13 15:00:57 |   deleted    | test_123_456_789 |        172.16.91.192        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:55:58Z |
	| 2017-07-13 15:00:57 |   deleted    |    test123456    |        172.16.91.191        | CentOS-Atomic-Host-7.20160130-GenericCloud |   2    | 2017-07-13T18:55:47Z |
	| 2017-07-13 15:00:57 | in whitelist |  jslave_centos   | 172.16.91.173, 10.8.187.160 |            paws-jslave-centos7             |   3    | 2017-07-13T01:02:58Z |
	| 2017-07-13 15:00:57 | in whitelist | jslave_fedora25  | 172.16.91.172, 10.8.187.207 |            paws-jslave-fedora25            |   3    | 2017-07-13T01:02:08Z |
	+---------------------+--------------+------------------+-----------------------------+--------------------------------------------+--------+----------------------+
	+---------------------+---------+--------------+
	|      TIMESTAMP      |  ACTION | FLOATING IP  |
	+---------------------+---------+--------------+
	| 2017-07-13 15:00:57 | deleted | 10.8.180.199 |
	+---------------------+---------+--------------+


# For developer and contributers

This section describes how to build a new RPM for janitor;
I use make so it requires basic packages in your machine I recommend: python-setuptools, python-sphinx, python-devel and gcc

## RPM / Build

	$ make

	Usage: make <target> where <target> is one of

	clean     clean temp files from local workspace
	doc       generate sphinx documentation and man pages
	test      run unit tests locally
	tarball   generate tarball of project
	rpm       build source codes and generate rpm file
	srpm      generate SRPM file
	build     generate srpm and send to build in copr
	all       clean test doc rpm
	flake8    check Python style based on flake8

Running from your local machine, you can generate your own RPM running:

	$ make rpm

and if your environment is setup properly you should have your RPM at: /home/user/git/janitor/rpmbuild/RPMS/x86_64/janitor-0.0.1-1.x86_64.rpm

janitor is being built on Fedora Copr: https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/builds/

running a new build you need to check your ~/.config/copr-fedora file and run:

	make build


## install

Installing from your local machine, after you build your own RPM just run:

for Fedora:

	$ sudo dnf install /home/user/git/janitor/rpmbuild/RPMS/x86_64/janitor-0.0.1-1.x86_64.rpm

for RHEL and CentOS:

	$ sudo yum install /home/user/git/janitor/rpmbuild/RPMS/x86_64/janitor-0.0.1-1.x86_64.rpm

To install from latest RPM:

**repo:** https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/

for Fedora:

	sudo dnf copr enable eduardocerqueira/janitor

or if needed get the repo from https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/
and maybe is needed to disable **gpgcheck=0**


	[eduardocerqueira-janitor]
	name=Copr repo for janitor owned by eduardocerqueira
	baseurl=https://copr-be.cloud.fedoraproject.org/results/eduardocerqueira/janitor/epel-7-$basearch/
	type=rpm-md
	skip_if_unavailable=True
	gpgcheck=0
	gpgkey=https://copr-be.cloud.fedoraproject.org/results/eduardocerqueira/janitor/pubkey.gpg
	repo_gpgcheck=0
	enabled=1
	enabled_metadata=1


or if links above don't work go to Copr Janitor project for more details how to proceed from here.


## MORE INFO

For others topics listed below, please generate the sphinx doc in your local machine running the command:

	$ make doc

and from a browser access: file:///home/user/git/janitor/docs/build/html/index.html

* Install:
* Guide:
* Build:
* Development:


 ## How to contribute

 Feel free to fork and send me pacthes or messages if you think this tool can be helpful for any other scenario.

