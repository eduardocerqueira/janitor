
![copr build](https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/package/janitor/status_image/last_build.png)

# janitor

MOTIVATION:

One of my Openstack tenants that I use to run tests for an internal tool has a very limited quota so all the time I need to stop my tests and automations and spend few minutes
cleaning up public/floating ips, destroying virtual machines and others. The idea to have janitor or a butler is actually an old idea and a coworker had implemented
it but in a more sophisticated and fashion way this is a simply version and currently only focusing in Openstack maybe further I'll extend it to AWS, Openshift and others.

WHAT IS THIS?

Linux tool to help clean-up tasks for Openstack.

USAGE:

clean up virtual machines and release floating ips for Openstack keep items declared in the whitelist.txt file:

1. load your Openstack rc
2. run janitor

    source ~/mytenant-openrc.sh
	janitor --openstack --whitelist /tmp/whitelist.txt

listing history for your janitor:

	janitor --history


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
	all       clean test doc rpm
	flake8    check Python style based on flake8

Running from your local machine, you can generate your own RPM running:

	$ make rpm

and if your environment is setup properly you should have your RPM at: /home/user/git/janitor/rpmbuild/RPMS/x86_64/janitor-0.0.1-1.x86_64.rpm

janitor is being built on Fedora Copr: https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/builds/

running a new build:

	$ copr-cli build janitor https://github.com/eduardocerqueira/janitor/raw/master/copr/janitor-0.0.1-1.src.rpm


## install

Installing from your local machine, after you build your own RPM just run:

for Fedora:

	$ sudo dnf install /home/user/git/janitor/rpmbuild/RPMS/x86_64/janitor-0.0.1-1.x86_64.rpm

for RHEL and CentOS:

	$ sudo yum install /home/user/git/janitor/rpmbuild/RPMS/x86_64/janitor-0.0.1-1.x86_64.rpm

To install from latest RPM:

**repo:** https://copr.fedorainfracloud.org/coprs/eduardocerqueira/janitor/

	$ sudo yum install https://copr-be.cloud.fedoraproject.org/results/eduardocerqueira/janitor/epel-7-x86_64/00489346-janitor/janitor-0.0.1-1.x86_64.rpm
	$ sudo dnf install https://copr-be.cloud.fedoraproject.org/results/eduardocerqueira/janitor/fedora-24-x86_64/00474191-janitor/janitor-0.0.1-1.x86_64.rpm


sample of reports:

Report with 2 executions appended:
![Preview](https://github.com/eduardocerqueira/janitor/raw/master/docs/source/_static/1_report.png)

Report with 1 execution:
![Preview](https://github.com/eduardocerqueira/janitor/raw/master/docs/source/_static/report_append.png)

Listing DST with .sh files migrated from SRC and all links created from SRC to DST:

![Preview](https://github.com/eduardocerqueira/janitor/raw/master/docs/source/_static/src_link.png)

![Preview](https://github.com/eduardocerqueira/janitor/raw/master/docs/source/_static/dst_migrated.png)


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

