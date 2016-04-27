# -*- coding: utf-8 -*-


class NutshellCRMError(Exception):
    pass


class NutshellCRMBadRequest(NutshellCRMError):
    pass


class NutshellCRMBadAuth(NutshellCRMError):
    pass


class NutshellCRMForbidden(NutshellCRMError):
    pass


class NutshellCRMLimitExceeded(NutshellCRMError):
    pass


class NutshellCRMBadStatus(NutshellCRMError):
    pass
