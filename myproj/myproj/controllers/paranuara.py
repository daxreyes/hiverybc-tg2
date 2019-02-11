import logging
from tg import expose
from tg import request, validate
from formencode.validators import NotEmpty, Int, DateConverter, String, Bool
from tgext.crud import EasyCrudRestController
from myproj import model as M

log = logging.getLogger(__name__)


FRUITS = set(['apple',
 'banana', 
 'cucumber',
 'orange',
 'strawberry'])

VEGETABLES = set([ 'beetroot',
 'carrot',
 'celery',
])


class PeopleFoodsAPIController(EasyCrudRestController):
    '''
    curl 'http://localhost:8080/people/1/foods.json?vegetables=true&fruits=true'
    '''
    model = M.People

    @expose('json')
    def get_all(self, **kw):
        """
        
        """
        index = Int().to_python(request.controller_state.routing_args.get('index'))
        validated_entries = {}
        for k,v in [('vegetables', Bool()), ('fruits', Bool())]:
            if(kw.get(k,None) is not None):
                validated_entries[k] = v.to_python(kw[k])

        log.debug('food params {}'.format(validated_entries))

        person =  M.People.query.get(index=index)

        res = {}
        for k in ['name','age']:
            res[k] = getattr(person,k)
        
        for entry, food in [('vegetables', VEGETABLES), ('fruits', FRUITS)]:
            if validated_entries.get(entry) == True:
                res.update({
                    entry: list(
                        food.intersection(
                            set(person.favouriteFood))
                        )
                    })

        if(validated_entries.get('vegetables') is None and validated_entries.get('fruits') is None ):
            res.update({'favourite': person.favouriteFood})
        return res



class CommonFriendsAPIController(EasyCrudRestController):
    pagination = True
    model = M.People
    @validate({
        'friend_index':Int(not_empty=True),
    })
    @expose('json')
    def get_one(self, friend_index, **kw):
        '''
        To get common friends with {
            'eyeColor':'brown',
            'has_died':false
        }
        curl 'http://localhost:8080/people/1/common_friends/2.json?index=2&eyeColor=brown&has_died=false'
        '''
        index = request.controller_state.routing_args.get('index')
        
        log.debug('common_friends params {} {} {} {} {}'.format(index, type(index), type(friend_index), kw, request.controller_state.routing_args))
        
        persons =  M.People.query.find({
            'index':{
                '$in':[int(index), friend_index]
            }},
            {'name':1,'age':1,'address':1,'phone':1, 'index':1, 'email':1, 'company_id':1}
        ).all()

        filters = {
            'friends':{'$all': [{'index':persons[0].index}, {'index':persons[1].index}]}, 
            'index': {'$nin':[persons[0].index, persons[1].index]}}
        
        for k,v in [('eyeColor', String()), ('has_died', Bool())]:
            if(kw.get(k,None) is not None):
                filters[k] = v.to_python(kw[k])

        log.debug('filters {}'.format(filters))

        common_friends = M.People.query.find(filters, {'name':1,'age':1,'address':1,'phone':1, 'index':1, 'email':1, 'company_id':1, 'has_died':1, 'eyeColor':1}).all()

        return dict(persons=persons, common_friends=common_friends)


class PeopleAPIController(EasyCrudRestController):
    # pagination = True
    model = M.People

    common_friends = CommonFriendsAPIController(M.DBSession)
    foods = PeopleFoodsAPIController(M.DBSession)

    @validate({
        'index':Int(not_empty=True)
    })
    @expose('json')
    def get_one(self, index):
        person = M.People.query.find({
            'index':index}).one()
        print('get_one, person {}'.format(person))
        return dict(person=person)




class EmployeesAPIController(EasyCrudRestController):
    model = M.People

    @expose('json')
    def get_all(self):
        '''
        employees and some of employee details of company
        '''
        company_id = Int().to_python(request.controller_state.routing_args.get('company_id'))
        log.debug('company {}  {}'.format(company_id, type(company_id)))
        company =  M.Company.query.get(index=company_id)
        employees = [
            dict([ (k, i[k]) for k in [
                'name', 
                'age', 
                'address', 
                'phone', 
                'index', 
                'email', 
                'company_id']]) for i in company.employees]
        return dict(company=company, employees=employees)


class CompanyAPIController(EasyCrudRestController):
    '''
        curl 'http://localhost:8080/companies/1.json'

    '''
    # pagination = True
    model = M.Company

    employees = EmployeesAPIController(M.DBSession)

    @validate({
        'company_id':Int(not_empty=True)
    })
    @expose('json')
    def get_one(self, company_id):
        """
        By default returns something like this given an objectId
        {"model": "Company", "value": {"_id": "5c5beddf459bee29cb1a9aae", "index": 1, "company": "PERMADYNE"}}
        """
        log.debug('company_id {} {}'.format(company_id, type(company_id)))

        res = M.Company.query.get(index=company_id)
        log.debug('company {}'.format(res))
        return {'index':res['index'], 'company':res['company']}