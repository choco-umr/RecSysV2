from fastapi import HTTPException
#docs : https://fastapi.tiangolo.com/reference/exceptions/#fastapi.HTTPException
#http status codes : https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

####################### Recognised users ####################### 
#These excptions are for users that are signed in and recognised

#User is correct but permission not allowed (e.g user trying to acess admin routes)
class UserNotAuthorized(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=403, detail="Access Forbidden")

####################### Recognised users ####################### 



####################### Aliens ####################### 
#These exceptions are for users that are not signed in and or recognised

#incorrect email and or password
class IncorrectLoginDetails(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="Incorrect Username / Password")

class DuplicateUsername (HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="Username already exists")

#Expired JWT Token
class ExpiredJWT(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="JWT Token expired")

#Invalid JWT Token
class InvalidJWT(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="JWT Token invalid")

#JWT Not found
class JWTNotFound(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=401, detail="JWT Token not found")

#JWT Already existing (cannot login when already logged in etc)
class JWTFound(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=409, detail="Existing JWT found")

#user not found
class UserNotFound(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=404, detail="User not found")

#Invalid Dataset Type
class InvalidDatasetType(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="Invalid dataset type")

#Invalid File type
class InvalidDatasetType(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="Invalid dataset type")
####################### Aliens ####################### 

class InvalidFiletype(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="Invalid file type")

class InvalidFilesize(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="File too large")

class FilenameRequired(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, status_code=422, detail="Filename required")

# class SchemaValidationError(HTTPException):
#     def __init__(self, errors):
#         self.errors = errors
#         HTTPException.__init__(self, status_code=422, detail=f"Schema validation failed: {errors}")



#TO/DO
#add comments above each excption
#clean imports
#order these by groups