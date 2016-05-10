from .params import BaseParamsBuilder


class AccountParamsBuilder(BaseParamsBuilder):

    def __init__(self, company):
        super(AccountParamsBuilder, self).__init__()
        self.local_company = company
        self.nutshell_company = {}

    @property
    def params(self):
        return self.nutshell_company

    def build_creation_params(self):
        self.nutshell_company = {
            "name": self.company.name,
            "url": self.company.url,
        }

        self._build_custom_fields({
            "Category": self.company.category
        })


class ContactParamsBuilder(BaseParamsBuilder):

    def __init__(self, user):
        super(ContactParamsBuilder, self).__init__()
        self.local_user = user
        self.nutshell_contact = {}

    @property
    def params(self):
        return self.nutshell_contact

    def build_creation_params(self):
        self.nutshell_contact = {
            "name": self.user.full_name,
            "phone": [self.user.phone],
            "email": [self.user.email],
        }
