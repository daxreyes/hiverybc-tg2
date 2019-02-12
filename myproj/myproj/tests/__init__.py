# -*- coding: utf-8 -*-
"""Unit and functional test suite for myproj."""

from os import getcwd
from paste.deploy import loadapp
from webtest import TestApp
from gearbox.commands.setup_app import SetupAppCommand
from tg import config
from tg.util import Bunch

from myproj import model

__all__ = ['setup_app', 'setup_db', 'teardown_db', 'TestController']

application_name = 'main_without_authn'


def load_app(name=application_name):
    """Load the test application."""
    return TestApp(loadapp('config:test.ini#%s' % name, relative_to=getcwd()))


def setup_app():
    """Setup the application."""
    cmd = SetupAppCommand(Bunch(options=Bunch(verbose_level=1)), Bunch())
    cmd.run(Bunch(config_file='config:test.ini', section_name=None))


def setup_db():
    """Create the database schema (not needed when you run setup_app)."""
    datastore = config['tg.app_globals'].ming_datastore
    model.init_model(datastore)


def teardown_db():
    """Destroy the database schema."""
    datastore = config['tg.app_globals'].ming_datastore
    try:
        # On MIM drop all data
        datastore.conn.drop_all()
    except TypeError:
        # On MongoDB drop database
        # print('**** datastore',dir(datastore), type(datastore) )
        # print('**** db', dir(datastore.db), type(datastore.db))
        # print('**** conn', dir(datastore.conn), type(datastore.conn))
        # datastore.conn.drop_database(datastore.db)
        datastore.db.command("dropDatabase")


class TestController(object):
    """Base functional test case for the controllers.

    The myproj application instance (``self.app``) set up in this test
    case (and descendants) has authentication disabled, so that developers can
    test the protected areas independently of the :mod:`repoze.who` plugins
    used initially. This way, authentication can be tested once and separately.

    Check myproj.tests.functional.test_authentication for the repoze.who
    integration tests.

    This is the officially supported way to test protected areas with
    repoze.who-testutil (http://code.gustavonarea.net/repoze.who-testutil/).

    """
    application_under_test = application_name

    def setUp(self):
        """Setup test fixture for each functional test method."""
        self.app = load_app(self.application_under_test)
        self.bootstrap_data()
        setup_app()
    def tearDown(self):
        """Tear down test fixture for each functional test method."""
        teardown_db()


    def bootstrap_data(self):
        """
        Sample test data
        """
        data = {
            'people':[{
                '_id': '595eeb9bb3821d9982ea44f9',
                'about': 'Ex cillum commodo labore sint non velit aliquip',
                'address': '455 Dictum Court, Nadine, Mississippi, 6499',
                'age': 54,
                'balance': '$2,119.44',
                'company_id': 59,
                'email': 'bonniebass@earthmark.com',
                'eyeColor': 'blue',
                'favouriteFood': ['orange', 'beetroot', 'banana', 'strawberry'],
                'friends': [{'index': 0}, {'index': 1}, {'index': 2}],
                'gender': 'female',
                'greeting': 'Hello, Bonnie Bass! You have 10 unread messages.',
                'guid': '49c04b8d-0a96-4319-b310-d6aa8269adca',
                'has_died': False,
                'index': 2,
                'name': 'Bonnie Bass',
                'phone': '+1 (823) 428-3710',
                'picture': 'http://placehold.it/32x32',
                'registered': '2017-06-08T04:23:18 -10:00',
                'tags': ['quis', 'sunt', 'sit', 'aliquip', 'pariatur', 'quis', 'nulla']},
                {'_id': '595eeb9c53d1461a0b53f676',
                'about': 'Duis labo',
                'address': '130 Fay Court, Mayfair, New York, 4184',
                'age': 49,
                'balance': '$3,795.56',
                'company_id': 59,
                'email': 'dorthysimmons@earthmark.com',
                'eyeColor': 'brown',
                'favouriteFood': ['orange', 'beetroot', 'banana', 'strawberry'],
                'friends': [{'index': 0}],
                'gender': 'female',
                'greeting': 'Hello, Dorthy Simmons! You have 5 unread messages.',
                'guid': 'beca7ed2-163e-47c5-9b62-5962fffb7d01',
                'has_died': False,
                'index': 595,
                'name': 'Dorthy Simmons',
                'phone': '+1 (972) 529-3994',
                'picture': 'http://placehold.it/32x32',
                'registered': '2016-10-15T11:05:12 -11:00',
                'tags': ['veniam',
                'aliquip',
                'duis',
                'voluptate',
                'officia',
                'anim',
                'non']},
                {'_id': '595eeb9b96d80a5bc7afb106',
                'about': 'Est id reprehenderit ',
                'address': '628 Sumner Place, Sperryville, American Samoa, 9819',
                'age': 61,
                'balance': '$2,418.59',
                'company_id': 58,
                'email': 'carmellalambert@earthmark.com',
                'eyeColor': 'blue',
                'favouriteFood': ['orange', 'apple', 'banana', 'strawberry'],
                'friends': [{'index': 0}, {'index': 1}, {'index': 2}],
                'gender': 'female',
                'greeting': 'Hello, Carmella Lambert! You have 6 unread messages.',
                'guid': '5e71dc5d-61c0-4f3b-8b92-d77310c7fa43',
                'has_died': True,
                'index': 0,
                'name': 'Carmella Lambert',
                'phone': '+1 (910) 567-3630',
                'picture': 'http://placehold.it/32x32',
                'registered': '2016-07-13T12:29:07 -10:00',
                'tags': ['id', 'quis', 'ullamco', 'consequat', 'laborum', 'sint', 'velit']
            }],
            'companies':[
                {"index" : 0, "company" : "NETBOOK" },
                {"index" : 58, "company" : "JAMNATION"},
                {"index" : 59, "company" : "BRAINCLIP"}
            ]}

        companies = [model.Company(**c) for c in data['companies']]
        people = [model.People(**p) for p in data['people']]
        model.DBSession.flush()
        model.DBSession.clear()
   