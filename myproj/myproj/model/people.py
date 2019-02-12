from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm import Mapper
from ming.odm.declarative import MappedClass
from myproj.model import DBSession
import re

class EmailSchema(s.FancySchemaItem):
    regex = re.compile(r'[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$')

    def _validate(self, value, **kw):
        if not self.regex.match(value):
            raise schema.Invalid('Not a valid email address', value)
        return value

class People(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'people'

    _id = FieldProperty(s.ObjectId)
    about = FieldProperty(s.String(if_missing=''))
    address = FieldProperty(s.String(if_missing=''))
    age = FieldProperty(s.Int(required=True))
    balance = FieldProperty(s.String)
    company_id = FieldProperty(s.Int(required=True))
    # company_id = ForeignIdProperty('Company')
    # company = RelationProperty('Company')
    email = FieldProperty(EmailSchema, required=False)
    eyeColor = FieldProperty(s.String)
    favouriteFood = FieldProperty(s.Array(s.String))
    friends = FieldProperty(s.Array(s.Anything))
    gender = FieldProperty(s.String)
    greeting = FieldProperty(s.String(if_missing=''))
    guid = FieldProperty(s.String)
    has_died = FieldProperty(s.Bool)
    index = FieldProperty(s.Int(required=True))
    name = FieldProperty(s.String)
    phone = FieldProperty(s.String)
    picture = FieldProperty(s.String)
    # registered = FieldProperty(s.DateTime)
    registered = FieldProperty(s.Anything(required=False, if_missing=''))
    tags = FieldProperty(s.Array(s.String))


class Company(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'company'

    _id = FieldProperty(s.ObjectId)
    index = FieldProperty(s.Int(required=True))
    company = FieldProperty(s.String(required=True))


    @property
    def employees(self):
        '''
        Alive Employees
        '''
        return People.query.find(dict(company_id=self.index, has_died=False)).all()

