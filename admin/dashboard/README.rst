=============================
Naanal Admin Dashboard
=============================


Prerequisites
===============

* Ubuntu Machine
* Local or Remote Openstack Environment

Installing Naanal Dashboard
==============================

* Clone the repo::

    $ git clone https://github.com/naanal/product.git

* Creating Virtual Environment::

    $ cd path-to-dashboard/./run_tests.sh
	
* Configure local settings::

  $ vim path-to-dashboard/openstack_dashboard/local/local_settings.py
  $ Edit OPENSTACK_HOST = "ip_address/host_name to point out openstack environment"

* Run::
	
	$ ./runtest.sh --runserver 'local_ip_address/host_name : port_no'
	
	Example: $ ./runtest.sh --runserver 192.168.20.124:9000
	
