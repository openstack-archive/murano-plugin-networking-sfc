Murano Plugin Networking SFC
============================

Integration with networking-sfc extension
<http://docs.openstack.org/developer/networking-sfc/> for OpenStack Neutron.

Installation
============

Plugin
------

To build and install python plugin::

  python setup.py bdist_wheel
  pip install dist/murano_plugin_networking_sfc-<version>-py2-none-any.whl

Murano library / Demo application
---------------------------------

To install library::

  cd networking_sfc_library
  zip ../networking-sfc-library.zip *
  murano package-import --is-public ../networking-sfc-library.zip

Demo application installation is similar to the library installation.

