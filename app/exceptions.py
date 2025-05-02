
class CampsiteError(Exception):
    """ Base exception for campsite errors"""
    pass
class LimitError(CampsiteError):
    """ When trying to access an amount of campsites that exceeds the max actual sites"""
    pass