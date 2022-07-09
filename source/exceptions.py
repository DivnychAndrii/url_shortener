from fastapi import status, HTTPException


class NotFoundHTTPException(HTTPException):

    def __init__(self, **kwargs):
        kwargs['status_code'] = status.HTTP_404_NOT_FOUND
        super(HTTPException, self).__init__(**kwargs)
