from sqlalchemy.orm import Session


class BaseManager:

    def __init__(self,  session: Session):
        self.session = session
