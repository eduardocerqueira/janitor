# Janitor Tests

**Requirements:**
* Openstack cluster properly setup 
* Openstack tenant and credentials
* Openstack openrc.sh file
* whitelist.txt file
* python venv with janitor/requirements installed see [local dev environment](../README.md#local-dev-environment)

The tests can handle authentication by environment variables or loading the variables from a physical openrc.sh file, 
you can use the template `janitor/tests/test-openrc-sample.sh` creating a copy and replacing the content with your
account and Openstack data.

Or using environment variable to point the location of your openrc.sh file as showing below:
```
export OPENSTACK_CREDS=/home/user/openrc.sh
```

`whitelist.txt` file is required and should be placed in the same folder: `janitor/tests/whitelist.txt` which will
contain the name of virtual machines to be kept and not deleted when Janitor runs.

## Generating data for test

It is an optional step, feel free to skip it if you have data in your Openstack for testing. 

Running the commands below you can generate content or vms for your tests, replace values from `--key-name --image --network` 
with correspondent from your Openstack:  

```
openstack server create --key-name MyKeyName --flavor m1.small --image FEDORA-34-x86_64-latest --network d655dcd0-b593-439c-997b-aa5bc8c03a3a Fedora34
openstack server create --key-name MyKeyName --flavor m1.small --image FEDORA-33-x86_64-latest --network d655dcd0-b593-439c-997b-aa5bc8c03a3a Fedora33
openstack server create --key-name MyKeyName --flavor m1.small --image FEDORA-32-x86_64-latest --network d655dcd0-b593-439c-997b-aa5bc8c03a3a Fedora32
```
 
## Running tests

```
cd tests

# running all tests from a file
pytest test_openstack_credentials.py -v

# running specific test
pytest test_openstack_instances.py -v -k test_get_ip_all_instances 

# running all tests
pytest -v
```
  
## Issues

1. classpath

 if you are having issues with classpath you can try:

 PYTHONPATH=janitor pytest tests/test_openstacksdk.py -v
 PYTHONPATH=janitor pytest tests -v

 on this example I am running the command above from my janitor folder.
