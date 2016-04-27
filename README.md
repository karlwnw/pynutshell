# pynutshell

This is a simple Nutshell CRM client in Python. Nutshell API documentation: https://www.nutshell.com/api/

##  Usage

### Get account

```
from pynutshell import NutshellCRMClient

client = NutshellCRMClient(email, api_key)
client.get_account(account_id)
```

### Create account

```
from pynutshell import NutshellCRMClient

builder = AccountParamsBuilder(company)
builder.build_creation_params()
data = builder.params

client = NutshellCRMClient(email, api_key)
response = client.new_account(data)
```
