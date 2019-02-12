# -*- coding: utf-8 -*-
"""Test suite for the TG app's models"""
from __future__ import unicode_literals
from nose.tools import eq_

from myproj import model
from myproj.tests.models import ModelTest


class TestGroup(ModelTest):
    """Unit test case for the ``Group`` model."""

    klass = model.Group
    attrs = dict(
        group_name="test_group",
        display_name="Test Group"
    )


class TestUser(ModelTest):
    """Unit test case for the ``User`` model."""

    klass = model.User
    attrs = dict(
        user_name="ignucius",
        email_address="ignucius@example.org"
    )

    def test_obj_creation_username(self):
        """The obj constructor must set the user name right"""
        eq_(self.obj.user_name, "ignucius")

    def test_obj_creation_email(self):
        """The obj constructor must set the email right"""
        eq_(self.obj.email_address, "ignucius@example.org")

    def test_no_permissions_by_default(self):
        """User objects should have no permission by default."""
        eq_(len(self.obj.permissions), 0)

    def test_getting_by_email(self):
        """Users should be fetcheable by their email addresses"""
        him = model.User.by_email_address("ignucius@example.org")
        eq_(him._id, self.obj._id)


class TestPermission(ModelTest):
    """Unit test case for the ``Permission`` model."""

    klass = model.Permission
    attrs = dict(
        permission_name="test_permission",
        description="This is a test Description"
    )


class TestPeople(ModelTest):
    """Unit test case for the ``People`` model."""

    klass = model.People
    attrs = {
        # '_id': '595eeb9bb3821d9982ea44f9',
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
        'tags': ['quis', 'sunt', 'sit', 'aliquip', 'pariatur', 'quis', 'nulla']
    }

    def test_obj_creation_name(self):
        """The People obj constructor must set the user name right"""
        eq_(self.obj.name, "Bonnie Bass")

    def test_obj_creation_email(self):
        """The People obj constructor must set the email right"""
        eq_(self.obj.email, "bonniebass@earthmark.com")

    def test_getting_index(self):
        """People should be fetcheable by their index"""
        him = model.People.query.get(index=2)
        eq_(him._id, self.obj._id)


class TestCompany(ModelTest):
    """Unit test case for the ``Company`` model."""

    klass = model.Company
    attrs = {"index" : 0, "company" : "NETBOOK" }

    def test_obj_creation_company(self):
        """The Company obj constructor must set the company field right"""
        eq_(self.obj.company, "NETBOOK")

    def test_obj_creation_index(self):
        """The Company obj constructor must set the index right"""
        eq_(self.obj.index, 0)

    def test_getting_index(self):
        """Company should be fetcheable by their index"""
        company = model.Company.query.get(index=0)
        eq_(company._id, self.obj._id)