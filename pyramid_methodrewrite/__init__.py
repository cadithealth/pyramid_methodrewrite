# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  pyramid_methodrewrite
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/04/08
# copy: (C) Copyright 2013 Cadit Inc., see LICENSE.txt
#------------------------------------------------------------------------------

from pyramid.settings import aslist, asbool

#------------------------------------------------------------------------------

DEFAULT_PARAM_NAME   = '_method' 
DEFAULT_HEADER_NAME  = 'X-HTTP-Method-Override'

HTTP_METHODS = (

  # shamelessly scrubbed from:
  #   http://annevankesteren.nl/2007/10/http-methods
  # todo: need to do some real research and bump this.

  # RFC 2616 (HTTP 1.1):
  'OPTIONS',
  'GET',
  'HEAD',
  'POST',
  'PUT',
  'DELETE',
  'TRACE',
  'CONNECT',

  # RFC 2518 (WebDAV):
  'PROPFIND',
  'PROPPATCH',
  'MKCOL',
  'COPY',
  'MOVE',
  'LOCK',
  'UNLOCK',

  # RFC 3253 (WebDAV versioning):
  'VERSION-CONTROL',
  'REPORT',
  'CHECKOUT',
  'CHECKIN',
  'UNCHECKOUT',
  'MKWORKSPACE',
  'UPDATE',
  'LABEL',
  'MERGE',
  'BASELINE-CONTROL',
  'MKACTIVITY',

  # RFC 3648 (WebDAV collections):
  'ORDERPATCH',

  # RFC 3744 (WebDAV access control):
  'ACL',

  # draft-dusseault-http-patch:
  'PATCH',

  # draft-reschke-webdav-search:
  'SEARCH',

)

#------------------------------------------------------------------------------
def factory(handler, registry):
  get   = registry.settings.get
  on    = [e.upper() for e in aslist(get('methodrewrite.on', 'GET POST'))]
  to    = [e.upper() for e in aslist(get('methodrewrite.to', ' '.join(HTTP_METHODS)))]
  pname = get('methodrewrite.param', DEFAULT_PARAM_NAME)
  hname = get('methodrewrite.header', DEFAULT_HEADER_NAME)
  def methodrewrite_tween(request):
    if request.method.upper() not in on:
      return handler(request)
    if hname in request.headers:
      meth = request.headers.get(hname, '').upper()
      if meth and ( not to or meth in to ):
        request.method = meth
        return handler(request)
    if pname in request.params:
      meth = request.params.get(pname, '').upper()
      if meth and ( not to or meth in to ):
        request.method = meth
        return handler(request)
    return handler(request)
  return methodrewrite_tween

#------------------------------------------------------------------------------
def includeme(config):
  '''
  Adds a pyramid :term:`tween` to `config` that converts GET or POST
  requests that have a '_method' GET or POST parameter set to a known
  HTTP method to have that method explicitly. Note that no other
  request rewriting is done to account for changes in interface.

  The following configuration settings can be set:

  * `methodrewrite.enabled`: a boolean flag to control whether or not
    method rewriting should be enabled. Default: ``True``.

  * `methodrewrite.on`: a list of incoming HTTP methods that will
    cause this tween to check the request parameters and potentially
    make the change. Defaults to ``(GET, POST)``.

  * `methodrewrite.header`: the name of the header that controls the
    requested method. Defaults to ``_method``. If present, the header
    override takes precedence over the parameter override.

  * `methodrewrite.param`: the name of the parameter that controls the
    requested method. Defaults to ``_method``.

  * `methodrewrite.to`: list of acceptable HTTP methods that a request
    can be rewritten to. If set to empty, no restrictions will be made
    on mapping to acceptable or known methods. Defaults to
    ``pyramid_methodrewrite.HTTP_METHODS``.

  Note that all methods are always converted to upper case.
  '''
  if asbool(config.registry.settings.get('methodrewrite.enabled', 'true')):
    config.add_tween('pyramid_methodrewrite.factory')

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
