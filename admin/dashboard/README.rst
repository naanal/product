=============================
Naanal Dashboard
=============================


Prerequisites
===============

* Ubuntu Machine
* Local or Remote Openstack Environment

Installing Naanal Dashboard
==============================

* Clone the repo::

    $ git clone https://github.com/naanal/product.git

* Add Openstack Environment Endpoint to hosts

    $ vim /etc/hosts
    $ Add 'ip-address naanal-host' at the end of the file
        Example: 192.168.30.125 naanal-host

* Creating Virtual Environment::

    $ cd product/user/dashboard/
    $ ./run_tests.sh


* Run::

	$ ./runtest.sh --runserver 'local_ip_address/host_name:port_no'

	Example: $ ./runtest.sh --runserver 192.168.20.124:9000


