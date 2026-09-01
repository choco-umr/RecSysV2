from fastapi import HTTPException

####################### Recognised users #######################
# These exceptions are for users that are signed in and recognised

class user_not_authorized(HTTPException):
    # User is correct but permission not allowed (e.g. user trying to access admin routes)
    def __init__(self):
        HTTPException.__init__(self, status_code=403, detail="Access Forbidden")


####################### Aliens #######################
# These exceptions are for users that are not signed in and/or recognised

class incorrect_login_details(HTTPException):
    # incorrect email and/or password
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="Incorrect Username / Password")


class duplicate_username(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="Username already exists")


class expired_jwt(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="JWT Token expired")


class invalid_jwt(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="JWT Token invalid")


class jwt_not_found(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="JWT Token not found")


class jwt_found(HTTPException):
    # JWT already existing (cannot login when already logged in etc)
    def __init__(self):
        HTTPException.__init__(self, status_code=409, detail="Existing JWT found")


class user_not_found(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=404, detail="User not found")


class invalid_dataset_type(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="Invalid dataset type")


class invalid_file_type(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="Invalid file type")


class invalid_file_size(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="File too large")


class filename_required(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="Filename required")

####################### etl pipeline exceptions ####################### 

class schema_validation_error(HTTPException):
    def __init__(self, errors):
        self.errors = errors
        HTTPException.__init__(self, status_code=422, detail=f"Schema validation failed: {errors}")


class empty_csv(HTTPException):
    def __init__(self, errors):
        self.errors = errors
        HTTPException.__init__(self, status_code=422, detail=f"CSV is empty")
# NOTES
"""
- docs: https://fastapi.tiangolo.com/reference/exceptions/#fastapi.HTTPException
- http status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
- adds comments above each exception for context
"""