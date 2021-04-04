# TeamTrak Backend
TeamTrak API - Python Lambda responsible for handling HTTP requests related to retrieving details about a project. Requires User authentication.

Also responsible for various AWS infrastructure including a Lambda function, API GW proxy, IAM role and DynamoDB tables.

## Create and activate python virtual environment
1. virtualenv env
2. source env/bin/activate

## Install dependencies:
pip install --upgrade -r requirements.txt

## Execute Unit Tests:
python -m unittest tests/test_handler.py

## Deploy Component into AWS:
ansible-playbook infrastructure/deploy/ansible/deploy.yml --extra-vars env={env}

## Destroy Component:
ansible-playbook infrastructure/deploy/ansible/deploy.yml --extra-vars 'env={env} terraform_command=destroy'