# Arrival test 
PyTest for sample CRUD client to manage alaska bears.  

## About Service
```
docker pull azshoo/alaska:1.0
```
- POST /bear - create
- GET /bear - read all bears
- GET /bear/:id - read specific bear
- PUT /bear/:id - update specific bear
- DELETE /bear - delete all bears
- DELETE /bear/:id - delete specific bear

Example of ber json:
```
{"bear_type":"BLACK","bear_name":"mikhail","bear_age":17.5}
```
Available types for bears are: POLAR, BROWN, BLACK and GUMMY.

## Quik start
```
pip install -r requirements.txt
pytest -n=4 --alluredir=./allure-results tests
allure serve allure-results
```

## Bugs
- Server response Content-Type: 'text/html;charset=utf-8' (must be 'application/json')
- Impossible to create GUMMY bear =( (POST /bear)
- Impossible to change bear types (PUT /bear)
- Age is not updated correctly (PUT /bear)
- Age can be <= 0
- 'Error. Pls fill all parameters' response.status_code = 200
- Bear name can be '' and '@#$%^&*'

## TODO
- Add validate response model (but need to fix Content-Type)
- Attach request|response in allure report
- If needed url variables set os.environment
- Сomb the code (Report messages, TODO ...)