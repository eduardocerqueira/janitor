.. _motivation:


Motivation
==========

I have been using OpenStack continuously since 2014 as a resource to run workloads with the main purpose of
testing software. Manage a healthy Openstack tenant quota is vital when working with CI/CD and a large number of
automated pipelines which run 24/7. A long time ago I and my team were having a lot of headaches with one of internal
Openstack the cluster which at that time had a very limited quota and workload capacity but was important for the
test workflow. With the constant false-positive for test failing due to lack of public/floating IP, storage/volume,
and even virtual CPU when provisioning new VMs, we got the idea of implementing Janitor, a super simple script/codes
to `automate the clean-up task of deleting left-over virtual machines as well network and volume from an Openstack
tenant, all managed by API and remote calls.`

