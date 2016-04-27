from .params import BaseParamsBuilder


class AccountParamsBuilder(BaseParamsBuilder):

    def __init__(self, company):
        super(AccountParamsBuilder, self).__init__()
        self.company = company

    def build_creation_params(self):
        self.params = {
            "account": {
                "name": self.company.name,
                "url": self.company.url,
                "customFields": {
                    "Category": self.company.category
                }
            }
        }


class ContactParamsBuilder(BaseParamsBuilder):

    def __init__(self, user):
        super(ContactParamsBuilder, self).__init__()
        self.user = user

    def build_creation_params(self):
        self.params = {
            "contact": {
                "name": self.user.full_name,
                "phone": [self.user.phone],
                "email": [self.user.email],
            }
        }
