
![copr build](https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/package/janitor/status_image/last_build.png)

# Janitor

<img align="left" width="100" height="100" src="https://raw.githubusercontent.com/eduardocerqueira/janitor/python3/docs/source/logo.jpg">

Janitor is a Linux component to perform quota management tasks to an [Openstack](https://www.openstack.org/) tenant. 

It `is not` an official Openstack's tool, and Janitor's code is wrapping Openstack python client libraries:

* [python-openstackclient](https://pypi.org/project/python-openstackclient/) to manage authentication and as general API 
* [python-neutronclient](https://github.com/openstack/python-neutronclient) to manage network
* [python-novaclient](https://github.com/openstack/python-novaclient) to manage compute nodes and vms
* [python-glanceclient](https://github.com/openstack/python-glanceclient) to manage cloud images
* [python-cinderclient](https://github.com/openstack/python-cinderclient) to manage volumes and block storage

## Table of content
* [Motivation](README.md#motivation)
* [Install and usage](README.md#install-and-usage)
* [Setup your dev environment](README.md#local-dev-environment)
* [Running janitor functional tests](tests/README.md#janitor-tests)
* [Contributing](README.md#contributing)


## Motivation

I have been using OpenStack continuously since 2014 as a resource to run workloads with the main purpose of 
testing software. Manage a healthy Openstack tenant quota is vital when working with CI/CD and a large number of 
automated pipelines which run 24/7. A long time ago I and my team were having a lot of headaches with one of internal 
Openstack the cluster which at that time had a very limited quota and workload capacity but was important for the 
test workflow. With the constant false-positive for test failing due to lack of public/floating IP, storage/volume, 
and even virtual CPU when provisioning new VMs, we got the idea of implementing Janitor, a super simple script/codes 
to `automate the clean-up task of deleting left-over virtual machines as well network and volume from an Openstack 
tenant, all managed by API and remote calls.`  


## Install and Usage

```
python janitor/cli.py openstack --openrc /root/insights-qa-openrc.sh --whitelist /var/lib/jenkins/workspace/janitor/janitor_whitelist.txt --keystone v3
python janitor/cli.py openstack --openrc /home/ecerquei/osp/insights-qa-openrc.sh --whitelist /janitor/janitor_whitelist.txt --keystone v3
openstack --openrc /home/ecerquei/osp/janitor-openrc.sh --whitelist /home/ecerquei/osp/janitor-whitelist.txt --keystone v3
```

### usage

clean up virtual machines and release floating ips for Openstack keep items declared in the whitelist.txt file:

1. load your Openstack rc to system environment variable or pass as parameter
2. run janitor

    source ~/mytenant-openrc.sh

	janitor openstack --whitelist /tmp/whitelist.txt --keystone v3
	janitor openstack --openrc /tmp/mytenant-openrc.sh --whitelist /tmp/whitelist.txt --keystone v3

listing history for your janitor:

	janitor history


## local dev environment

**Requirements:**
* Linux OS *tested on Fedora and CentOS*
* Python3
* packages: 

```
# install packages needed for build and release RPM, and generate doc
sudo dnf install redhat-rpm-config python3-devel gcc python3-devel python3-pip python3-wheel python3-setuptools, python3-sphinx

# prep your python env
git clone git@github.com:eduardocerqueira/janitor.git
cd janitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/devel.txt

# check janitor installation
python janitor/cli.py --help
```

see [running janitor functional tests](tests/README.md#janitor-tests)


or using **make** it requires basic packages in your machine I recommend: python-setuptools, python-sphinx, python3-devel and gcc

## RPM / Build

	$ make

	Usage: make <target> where <target> is one of

	clean     clean temp files from local workspace
	doc       generate sphinx documentation and man pages
	test      run functional/unit tests locally
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

	[ecerquei@dev ~]$ janitor openstack --openrc /home/ecerquei/git/janitor/tests/test-openrc.sh --whitelist /home/ecerquei/git/janitor/tests/whitelist.txt --keystone v2
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
	
    +---------------------+---------+--------------------------------------+
    |      TIMESTAMP      |  ACTION |              VOLUME ID               |
    +---------------------+---------+--------------------------------------+
    | 2017-07-13 15:00:57 | deleted | 358be8d1-6d4a-4db7-973f-8369d4ff86f7 |
    +---------------------+---------+--------------------------------------+	

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

    +---------------------+---------+--------------------------------------+
    |      TIMESTAMP      |  ACTION |              VOLUME ID               |
    +---------------------+---------+--------------------------------------+
    | 2017-07-13 15:00:57 | deleted | 358be8d1-6d4a-4db7-973f-8369d4ff86f7 |
    +---------------------+---------+--------------------------------------+	

## Contributing 




## install

Installing from your local machine, after you build your own RPM just run:

for Fedora:

	sudo dnf install /home/user/git/janitor/rpmbuild/RPMS/x86_64/janitor-0.0.1-1.x86_64.rpm

for CentOS:

	*requires openstack repo*. you can consult here the latest repo https://wiki.openstack.org/wiki/Release_Naming

	sudo yum install centos-release-openstack-newton.noarch
	sudo yum install /home/user/git/janitor/rpmbuild/RPMS/x86_64/janitor-0.0.1-1.x86_64.rpm

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

INSTALLATION FAQ
----------------

Running on CentOS7 even having EPEL and centos-release-openstack-newton I got this error in one of my CentOS
server.


	[root@centos7 yum.repos.d]# janitor
	Traceback (most recent call last):
	  File "/usr/bin/janitor", line 6, in <module>
	    from pkg_resources import load_entry_point
	  File "/usr/lib/python2.7/site-packages/pkg_resources/__init__.py", line 3038, in <module>
	    @_call_aside
	  File "/usr/lib/python2.7/site-packages/pkg_resources/__init__.py", line 3022, in _call_aside
	    f(*args, **kwargs)
	  File "/usr/lib/python2.7/site-packages/pkg_resources/__init__.py", line 3051, in _initialize_master_working_set
	    working_set = WorkingSet._build_master()
	  File "/usr/lib/python2.7/site-packages/pkg_resources/__init__.py", line 659, in _build_master
	    return cls._build_from_requirements(__requires__)
	  File "/usr/lib/python2.7/site-packages/pkg_resources/__init__.py", line 672, in _build_from_requirements
	    dists = ws.resolve(reqs, Environment())
	  File "/usr/lib/python2.7/site-packages/pkg_resources/__init__.py", line 862, in resolve
	    raise VersionConflict(dist, req).with_context(dependent_req)
	pkg_resources.ContextualVersionConflict: (requests 2.11.1 (/usr/lib/python2.7/site-packages), Requirement.parse('requests>=2.14.2'), set(['python-keystoneclient']))


It is happening because python-requests lib is needed on version requests>=2.14.2 required by python-keystoneclient
when I ran:

	yum provides python-requests

the latest version I got was 2.11 that still don't satisfacts.

	python-requests-2.6.0-1.el7_1.noarch : HTTP library, written in Python, for human beings
	Repo        : base



	python-requests-2.10.0-1.el7.noarch : HTTP library, written in Python, for human beings
	Repo        : centos-openstack-newton



	python2-requests-2.11.1-1.el7.noarch : HTTP library, written in Python, for human beings
	Repo        : centos-openstack-newton
	Matched from:
	Provides    : python-requests = 2.11.1-1.el7



	python2-requests-2.11.1-1.el7.noarch : HTTP library, written in Python, for human beings
	Repo        : @centos-openstack-newton
	Matched from:
	Provides    : python-requests = 2.11.1-1.el7

The trick here was, forcing reinstall requests using pip:

	pip install requests --upgrade


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

