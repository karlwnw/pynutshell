class BaseParamsBuilder(object):

    def _build_custom_fields(self, data):
        if 'customFields' not in self.params:
            self.params['customFields'] = {}
        self.params['customFields'].update(data)
