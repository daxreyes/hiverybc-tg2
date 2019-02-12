import logging
from tg import expose
from tg import request, validate
from formencode.validators import NotEmpty, Int, DateConverter, String, Bool
from formencode import Invalid
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
    Resource to display a persons favourite food split into fruits and vegetables
    curl 'http://localhost:8080/people/1/foods.json?vegetables=true&fruits=true'
    '''
    model = M.People

    @expose('json', inherit=True)
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
        return {'model':'Food', 'value':res}



class CommonFriendsAPIController(EasyCrudRestController):
    '''
    Resource to display common friends between people
    To get common friends with {
            'eyeColor':'brown',
            'has_died':false
        }
    curl 'http://localhost:8080/people/1/common_friends/2.json?index=2&eyeColor=brown&has_died=false'
    '''
    model = M.People
    @validate({
        'friend_index':Int(not_empty=True),
    })
    @expose('json', inherit=True)
    def get_one(self, friend_index, **kw):
        index = request.controller_state.routing_args.get('index')
        
        log.debug('common_friends params {} {} {} {} {}'.format(index, type(index), type(friend_index), kw, request.controller_state.routing_args))
        
        persons =  M.People.query.find({
            'index':{
                '$in':[int(index), friend_index]
            }},
            {'name':1,'age':1,'address':1,'phone':1, 'index':1, 'email':1, 'company_id':1, 'friends':1}
        ).all()

        common = set(
                [p0['index'] for p0 in persons[0].friends]).intersection(
                    set([p1['index'] for p1 in persons[1].friends]))
        common.discard(persons[0])
        common.discard(persons[1])
        filters = {
            'index':{'$in': list(common) }, 
            # 'index': {'$nin':[persons[0].index, persons[1].index]}
        }
        log.debug('common friends of {} and {},  {}'.format(persons[0].index, persons[1].index, common))
        for k,v in [('eyeColor', String()), ('has_died', Bool())]:
            if(kw.get(k,None) is not None):
                filters[k] = v.to_python(kw[k])

        log.debug('filters {}'.format(filters))

        common_fields = {'name':1,'age':1,'address':1,'phone':1, 'index':1, 'email':1, 'company_id':1, 'has_died':1, 'eyeColor':1}
        common_friends = M.People.query.find(filters, common_fields).all()
        people = []
        for p in persons:
            d = {}
            for attr in ['name', 'age', 'address', 'phone', 'index', 'friends','_id']:
                d[attr] = getattr(p,attr,None)
            people.append(d)
        cfriends = []
        for p in common_friends:
            d = {}
            for attr in common_fields.keys():
                d[attr] = getattr(p,attr,None)
            cfriends.append(d)
        return dict(model='CommonFriends', 
            value = dict(people=people , 
            common_friends=cfriends))


class PeopleAPIController(EasyCrudRestController):
    """
    People resource use index to get item
    """
    model = M.People

    common_friends = CommonFriendsAPIController(M.DBSession)
    foods = PeopleFoodsAPIController(M.DBSession)

    @validate({
        'index':Int(not_empty=True)
    })
    @expose(inherit=True)
    def get_one(self, index, *args, **kw):
        """
        override get_one in order to use index instead of _id
        """
        person = M.People.query.get(index=index)
        log.debug('person {}'.format(person))
        if(person):
            kw['_id'] = person._id
        return super(PeopleAPIController, self).get_one(*args, **kw)




class EmployeesAPIController(EasyCrudRestController):
    model = M.People

    @expose('json', inherit=True)
    def get_all(self):
        '''
        company employees and selected employee details
        '''
        errors = []
        try:
            company_id = Int().to_python(request.controller_state.routing_args.get('company_id'))
            company =  M.Company.query.get(index=company_id)
            log.debug('company {}  {} {}'.format(company_id, type(company_id), company))
        except Invalid as ve:
            errors.append({'Invalid':str(ve)})
        else:
            try:
                employees = []
                if company:
                    employees = [
                        dict([ (k, i[k]) for k in [
                            'name', 
                            'age', 
                            'address', 
                            'phone', 
                            'index', 
                            'email', 
                            'company_id']]) for i in company.employees]
            except KeyError as e:
                errors.append({'KeyError': str(e)})

        if not errors:
            return {'model':'Employees', 'value': dict(company=company, employees=employees)}
        else:
            return dict(errors=errors)


class CompanyAPIController(EasyCrudRestController):
    '''
        curl 'http://localhost:8080/companies/1.json'

    '''
    model = M.Company

    # sub resource employees
    employees = EmployeesAPIController(M.DBSession)

    @validate({
        'company_id':Int(not_empty=True)
    })
    @expose('json', inherit=True)
    def get_one(self, company_id, *args, **kw):
        """
        By default returns something like this given an objectId
        {"model": "Company", "value": {"_id": "5c5beddf459bee29cb1a9aae", "index": 1, "company": "PERMADYNE"}}
        """
        log.debug('company_id {} {}'.format(company_id, type(company_id)))

        company = M.Company.query.get(index=company_id)
        log.debug('company {}'.format(company))
        if(company):
            kw['_id'] = company._id
        return super(CompanyAPIController, self).get_one(*args, **kw)
       