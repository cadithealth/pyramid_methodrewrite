# pyramid_methodrewrite

The ``pyramid_methodrewrite`` package is a pyramid plugin that adds a
"tween" that rewrites the active HTTP method (as exposed via
``request.method``) to the value provided in a query-string. The main
reason for this is to allow clients to fake the use HTTP methods
beyond GET and POST (such as PUT and DELETE) that are behind
non-compliant proxies, browsers, or other deficient software that
limit which HTTP methods can be sent.

It does this by inspecting the query-string or POST data, and if a
parameter named `_method` is found (the actual name is configurable)
and is of the known set of HTTP methods, will override the active
request's ``.method`` attribute.

## Installation

```
$ pip install pyramid-methodrewrite
```

## Configuration

The following configuration settings can be set in your application's
``main`` section:

* `methodrewrite.enabled`: a boolean flag to control whether or not
  method rewriting should be enabled. Default: ``True``.

* `methodrewrite.on`: a list of incoming HTTP methods that will cause
  this tween to check the request parameters and potentially make the
  change. Defaults to ``(GET, POST)``.

* `methodrewrite.param`: the name of the parameter that controls the
  requested method. Defaults to ``_method``.

* `methodrewrite.to`: list of acceptable HTTP methods that a request
  can be rewritten to. If set to empty, no restrictions will be made
  on mapping to acceptable or known methods. Defaults to
  ``pyramid_methodrewrite.HTTP_METHODS``.

Note that all method names are always converted to upper case.
