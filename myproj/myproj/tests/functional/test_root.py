# -*- coding: utf-8 -*-
"""
Functional test suite for the root controller.

This is an example of how functional tests can be written for controllers.

As opposed to a unit-test, which test a small unit of functionality,
functional tests exercise the whole application and its WSGI stack.

Please read http://pythonpaste.org/webtest/ for more information.

"""

from nose.tools import ok_

from myproj.tests import TestController


class TestRootController(TestController):
    """Tests for the method in the root controller."""

    def test_index(self):
        """The front page is working properly"""
        response = self.app.get('/')
        msg = 'TurboGears 2 is rapid web application development toolkit '\
              'designed to make your life easier.'
        # You can look for specific strings:
        ok_(msg in response)

        # You can also access a BeautifulSoup'ed response in your tests
        # (First run $ easy_install BeautifulSoup
        # and then uncomment the next two lines)

        # links = response.html.findAll('a')
        # print(links)
        # ok_(links, "Mummy, there are no links here!")
    def test_environ(self):
        """Displaying the wsgi environ works"""
        response = self.app.get('/environ.html')
        ok_('The keys in the environment are:' in response)

    def test_data(self):
        """The data display demo works with HTML"""
        response = self.app.get('/data.html?a=1&b=2')
        response.mustcontain("<td>a", "<td>1",
                             "<td>b", "<td>2")

    def test_data_json(self):
        """The data display demo works with JSON"""
        resp = self.app.get('/data.json?a=1&b=2')
        ok_(
            dict(page='data', params={'a': '1', 'b': '2'}) == resp.json,
            resp.json
        )
    def test_secc_with_manager(self):
        """The manager can access the secure controller"""
        # Note how authentication is forged:
        environ = {'REMOTE_USER': 'manager'}
        resp = self.app.get('/secc', extra_environ=environ, status=200)
        ok_('Secure Controller here' in resp.text, resp.text)

    def test_secc_with_editor(self):
        """The editor cannot access the secure controller"""
        environ = {'REMOTE_USER': 'editor'}
        self.app.get('/secc', extra_environ=environ, status=403)
        # It's enough to know that authorization was denied with a 403 status

    def test_secc_with_anonymous(self):
        """Anonymous users must not access the secure controller"""
        self.app.get('/secc', status=401)
        # It's enough to know that authorization was denied with a 401 status


class TestParanuaraAPIController(TestController):
    """Tests for the method in paranuara."""
    def test_person_json(self):
        """People resource item display demo works with JSON"""
        resp = self.app.get('/people/0.json')
        ok_(
            0 == resp.json['value']['index'],
            resp.json
        )
        
    def test_unkown_person_json(self):
        """Unknown person returns value:null"""
        resp = self.app.get('/people/9999.json', status=404)
        ok_(
            None == resp.json['value'],
            resp.json
        )

    def test_company_json(self):
        """Company resource returns a value"""
        resp = self.app.get('/companies/59.json')
        ok_(
            59 == resp.json['value']['index'],
            resp.json
        )

    def test_company_has_employees(self):
        """company/employee resource returns list of employees"""
        resp = self.app.get('/companies/59/employees.json')
        ok_(
            59 == resp.json['value']['company']['index'] and 2 == len(resp.json['value']['employees'])  ,
            resp.json
        )

    def test_company_exclude_dead_employees(self):
        """company/employee resource returns empty employees list"""
        resp = self.app.get('/companies/58/employees.json')
        ok_(
            (58 == resp.json['value']['company']['index']) and (0 == len(resp.json['value']['employees']))  ,
            resp.json
        )

    def test_common_friends(self):
        """default common friends"""

        resp = self.app.get('/people/595/common_friends/2.json')
        ok_(
            (1 == len(resp.json['value']['common_friends']))  ,
            resp.json
        )

    def test_common_friends_params1(self):
        """params has died blue eyed common friends"""

        resp = self.app.get('/people/595/common_friends/2.json?eyeColor=blue&has_died=true')
        ok_(
            (1 == len(resp.json['value']['common_friends']))  ,
            resp.json
        )

    def test_common_friends_params2(self):
        """params of brown eyed alive common friends"""

        resp = self.app.get('/people/595/common_friends/2.json?eyeColor=brown&has_died=false')
        ok_(
            (0 == len(resp.json['value']['common_friends']))  ,
            resp.json
        )

    def test_fruits(self):
        """Test split fruits and vegetables"""

        resp = self.app.get('/people/0/foods.json?fruits=true')
        ok_(
            (4 == len(resp.json['value']['fruits']))  ,
            resp.json
        )

    def test_vegetables(self):
        """Test split fruits and vegetables"""

        resp = self.app.get('/people/2/foods.json?vegetables=true')
        ok_(
            (1 == len(resp.json['value']['vegetables']))  ,
            resp.json
        )