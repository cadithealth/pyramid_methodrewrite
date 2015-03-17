# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/04/08
# copy: (C) Copyright 2013 Cadit Inc., see LICENSE.txt
#------------------------------------------------------------------------------

import unittest
from pyramid import testing
from pyramid.request import Request
from pyramid_methodrewrite import factory, includeme

#------------------------------------------------------------------------------
class TestRewriteFactory(unittest.TestCase):

  def setUp(self):
    self.config = testing.setUp()
    self.registry = self.config.registry

  def test_register(self):
    handler = factory(None, self.registry)
    self.assertEqual(handler.__name__, 'methodrewrite_tween')

#------------------------------------------------------------------------------
class TestRewriteTween(unittest.TestCase):

  def setupRequest(self, url='/', headers=None):
    request = Request.blank(url, headers=headers)
    self.request = request
    self.config = testing.setUp(request=request)
    self.registry = self.config.registry
    self.registry.settings = {}
    request.registry = self.registry

  def setupTween(self):
    # includeme(self.config)
    self.tween = factory(self.handler, self.registry)

  def handler(self, request):
    return request.method + ' ' + request.path_qs

  def test_direct(self):
    self.setupRequest('/path')
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'GET /path')

  def test_rewrite_put_param(self):
    self.setupRequest('/path?_method=put')
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'PUT /path?_method=put')

  def test_rewrite_put_header(self):
    self.setupRequest('/path', {'x-http-method-override': 'PUT'})
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'PUT /path')

  def test_limit_to_no_put_param(self):
    self.setupRequest('/path?_method=put')
    self.registry.settings['methodrewrite.to'] = 'DELETE SEARCH'
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'GET /path?_method=put')

  def test_limit_to_no_put_header(self):
    self.setupRequest('/path', {'x-http-method-override': 'PUT'})
    self.registry.settings['methodrewrite.to'] = 'DELETE SEARCH'
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'GET /path')

  def test_limit_to_with_delete_param(self):
    self.setupRequest('/path?_method=delete')
    self.registry.settings['methodrewrite.to'] = 'DELETE SEARCH'
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'DELETE /path?_method=delete')

  def test_limit_to_with_delete_header(self):
    self.setupRequest('/path', {'X-HTTP-METHOD-OVERRIDE': 'delete'})
    self.registry.settings['methodrewrite.to'] = 'DELETE SEARCH'
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'DELETE /path')

  def test_change_name_param(self):
    self.setupRequest('/path?_method=delete')
    self.registry.settings['methodrewrite.param'] = 'rewrite'
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'GET /path?_method=delete')
    self.setupRequest('/path?rewrite=delete')
    self.registry.settings['methodrewrite.param'] = 'rewrite'
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'DELETE /path?rewrite=delete')

  def test_change_name_header(self):
    self.setupRequest('/path', {'x-http-method-override': 'DELETE'})
    self.registry.settings['methodrewrite.header'] = 'x-methodrewrite'
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'GET /path')
    self.setupRequest('/path', {'x-methodrewrite': 'DELETE'})
    self.registry.settings['methodrewrite.header'] = 'x-methodrewrite'
    self.setupTween()
    self.assertEqual(self.tween(self.request), 'DELETE /path')

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
