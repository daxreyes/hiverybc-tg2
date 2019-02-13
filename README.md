Installation and Setup
======================

Clone this project url with recursive option to include the hivery-backend-challenge submodule

    $ git clone --recursive <project url>

Load to ``mongodb`` ``paranuara`` database the inital data from hivery-backend-challenge::

    $ mongoimport --db paranuara --collection company --type json --file ./hivery-backend-challenge/resources/companies.json --jsonArray
    $ mongoimport --db paranuara --collection people --type json --file ./hivery-backend-challenge/resources/people.json --jsonArray

Optional: Create a virtual environment and activate it

    $ python3.7 -m venv hiveryvenv
    $ source hiveryvenv/bin/activate

Install ``myproj`` using the setup.py script::

    $ cd myproj
    $ python setup.py develop
    $ pip install tg.devtools

Create the project database for any model classes defined::

    $ gearbox setup-app

Start the paste http server::

    $ gearbox serve

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ gearbox serve --reload --debug

Then you are ready to go.


Testing
=======

NOTE: 

 - The code is developed tested using python 3.7.2 and mongodb 3.4.19 on ubuntu 16.04 derivative (Linux Mint) environment. 
 
 - Tested to work also in python 3.6.7 and mongodb 3.6.3 on ubuntu 18.04

 - Tested to work also in python 3.7.2 and mongodb 3.4.9 on OSX 10.11.6


## Prior to running tests

Install nosetests and coverage::

    $ pip install nose coverage

## First run of test

Inside ``myproj`` main directory::

    $ python setup.py nosetests


## After first run of nose

Inside ``myproj`` main directory::

    $ nosetests --with-coverage --cover-erase


Hivery Backend Challenge Implementation
=======================================

This is a ``TurboGears 2`` based implementation of the hivery-backend-challenge using ``MongoDb`` as the backend database

## Solution to required end points

> Given a company, the API needs to return all their employees.

Implementation: Dead people are excluded

    $ curl 'http://localhost:8080/companies/<company.index>/employees.json'

    $ curl 'http://localhost:8080/companies/8/employees.json'

    {"model": "Employees", "value": {"company": {"_id": "5c5beddf459bee29cb1a9ab4", "index": 8, "company": "ZOINAGE"}, "employees": [{"name": "Kathrine Vaughan", "age": 30, "address": "475 Lafayette Avenue, Allensworth, Virgin Islands, 1409", "phone": "+1 (942) 516-2902", "index": 61, "email": "kathrinevaughan@earthmark.com", "company_id": 8}, {"name": "Laurel Mcintyre", "age": 48, "address": "512 Kimball Street, Nash, Maryland, 7258", "phone": "+1 (933) 485-2622", "index": 644, "email": "laurelmcintyre@earthmark.com", "company_id": 8}, {"name": "Griffin Blankenship", "age": 32, "address": "637 Eckford Street, Deltaville, North Dakota, 109", "phone": "+1 (947) 432-3886", "index": 652, "email": "griffinblankenship@earthmark.com", "company_id": 8}]}}

> Provide the appropriate solution if the company does not have any employees.

Implementation: Use POST to add new company employee. the field company_id in the provided json_data is overridden by company.index

    $ curl -i -X POST -H "Content-Type: application/json" http://localhost:8080/companies/<company.index>/employees.json -d '<json_data>'

    $ curl -i -X POST -H "Content-Type: application/json" http://localhost:8080/companies/58/employees.json -d '{"_id": "58dab52a6f4ae8b67d476745", "about": "I am a new employee", "address": "455 New Court, Nadine, Somewhere, 6499", "age": 45, "balance": "$2,123", "email": "newemployee@somewhere.com", "eyeColor": "brown", "favouriteFood": ["beetroot", "banana", "strawberry"], "friends": [{"index": 0}, {"index": 595}], "gender": "male", "greeting": "Hello, New Emp! You have 1 unread messages.", "guid": "8f5e4171-f039-4d6f-8578-c4e7603c13b8", "has_died": false, "index": 10001, "name": "New Emp", "phone": "+1 (111) 111-2222", "picture": "http://placehold.it/32x32", "registered": "2019-01-08T04:23:18 -10:00", "tags": ["new", "employee"]}'

    {"model": "People", "value": {"_id": "58dab52a6f4ae8b67d476745", "about": "I am a new employee", "address": "455 New Court, Nadine, Somewhere, 6499", "age": 45, "balance": "$2,123", "company_id": 58, "email": "newemployee@somewhere.com", "eyeColor": "brown", "favouriteFood": ["beetroot", "banana", "strawberry"], "friends": [{"index": 0}, {"index": 595}], "gender": "male", "greeting": "Hello, New Emp! You have 1 unread messages.", "guid": "8f5e4171-f039-4d6f-8578-c4e7603c13b8", "has_died": false, "index": 10001, "name": "New Emp", "phone": "+1 (111) 111-2222", "picture": "http://placehold.it/32x32", "registered": "2019-01-08T04:23:18 -10:00", "tags": ["new", "employee"]}}

> Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.

Implementation: Add ``eyeColor`` and ``has_died`` filters to end points. 

    $ curl 'http://localhost:8080/people/<people.index>/common_friends/<another people.index>.json&eyeColor=brown&has_died=false'

    $ curl 'http://localhost:8080/people/595/common_friends/2.json&eyeColor=brown&has_died=false'

    {"model": "CommonFriends", "value": {"people": [{"name": "Bonnie Bass", "age": 54, "address": "455 Dictum Court, Nadine, Mississippi, 6499", "phone": "+1 (823) 428-3710", "index": 2, "friends": [{"index": 0}, {"index": 1}, {"index": 2}], "_id": "595eeb9bb3821d9982ea44f9"}, {"name": "Dorthy Simmons", "age": 49, "address": "130 Fay Court, Mayfair, New York, 4184", "phone": "+1 (972) 529-3994", "index": 595, "friends": [{"index": 0}], "_id": "595eeb9c53d1461a0b53f676"}], "common_friends": [{"name": "Carmella Lambert", "age": 61, "address": "628 Sumner Place, Sperryville, American Samoa, 9819", "phone": "+1 (910) 567-3630", "index": 0, "email": "carmellalambert@earthmark.com", "company_id": 58, "has_died": true, "eyeColor": "blue"}]}}


> Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

Implementation: Provide a filter for fruits and vegetables

    $ curl 'http://localhost:8080/people/<people.index>/foods.json?vegetables=true&fruits=true'

    $ curl 'http://localhost:8080/people/8/foods.json?vegetables=true&fruits=true'
    
    {"model": "Food", "value": {"name": "Eliza Spence", "age": 65, "vegetables": ["carrot"], "fruits": ["apple", "strawberry", "cucumber"]}}


## Additional implementation details

Indexes were added to collections

  1. For collection ``people``, a unique index for the field ``index`` was added and an index for field `company_id`.
  
  2. For collection ``company``, a unique index for the field ``index`` was added.
