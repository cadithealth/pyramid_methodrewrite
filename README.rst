========================
Pyramid Method Rewriting
========================

The ``pyramid_methodrewrite`` package is a pyramid plugin that adds a
"tween" that rewrites the active HTTP method (as exposed via
``request.method``) to the value provided in a HTTP header or
query-string. The main reason for this is to allow clients to fake the
use of HTTP methods beyond GET and POST (such as PUT and DELETE) that
are behind non-compliant proxies, browsers, or other deficient
software that limit which HTTP methods can be sent.

It does this by looking for an ``X-HTTP-Method-Override`` HTTP header
or a ``_method`` parameter in either the query-string or POST data,
and if the value is of the known set of HTTP methods, will override
the active request's ``.method`` attribute. Both the header name and
parameter name are configurable. The header value, if specified, takes
precedence over the parameter value.

For example, the request:

.. code-block:: text

  GET /path/to/resource?_method=OPTIONS HTTP/1.1

Becomes equivalent (from the application's point of view) to:

.. code-block:: text

  OPTIONS /path/to/resource HTTP/1.1


Project
=======

* Homepage: https://github.com/cadithealth/pyramid_methodrewrite
* Bugs: https://github.com/cadithealth/pyramid_methodrewrite/issues


Installation
============


.. code-block:: bash

  $ pip install pyramid-methodrewrite


Usage
=====

Enable the tween either in your INI file via:

.. code-block:: ini

  pyramid.includes = pyramid_methodrewrite

or in code in your package's application initialization via:

.. code-block:: python

  def main(global_config, **settings):
    # ...
    config.include('pyramid_methodrewrite')
    # ...


Configuration
=============

The following configuration settings can be set in your application's
``main`` section:

* `methodrewrite.enabled`: a boolean flag to control whether or not
  method rewriting should be enabled. Default: ``True``.

* `methodrewrite.on`: a list of incoming HTTP methods that will cause
  this tween to check the request parameters and potentially make the
  change. Defaults to ``(GET, POST)``.

* `methodrewrite.header`: the name of the header that controls the
  requested method. Defaults to ``X-HTTP-Method-Override``. If
  present, the header override takes precedence over the parameter
  override.

* `methodrewrite.param`: the name of the parameter that controls the
  requested method. Defaults to ``_method``.

* `methodrewrite.to`: list of acceptable HTTP methods that a request
  can be rewritten to. If set to empty, no restrictions will be made
  on mapping to acceptable or known methods. Defaults to
  ``pyramid_methodrewrite.HTTP_METHODS``.

Note that all method names are always converted to upper case.
