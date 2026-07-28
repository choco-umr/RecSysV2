from fastapi import HTTPException
#docs : https://fastapi.tiangolo.com/reference/exceptions/#fastapi.HTTPException
#http status codes : https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

####################### etl pipeline exceptions ####################### 

class SchemaValidationError(HTTPException):
    def __init__(self, errors):
        self.errors = errors
        HTTPException.__init__(self, status_code=422, detail=f"Schema validation failed: {errors}")

class EmptyCSV(HTTPException):
    def __init__(self, errors):
        self.errors = errors
        HTTPException.__init__(self, status_code=422, detail=f"CSV is empty")
