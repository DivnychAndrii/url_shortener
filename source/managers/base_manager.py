from abc import abstractmethod

from sqlalchemy.orm import Session


class BaseManager:

    def __init__(self,  session: Session):  # No types
        self.session = session

    @property
    @abstractmethod
    def model(self):  # No types
        raise NotImplementedError

    def get_model_object(self, filters, method: str = 'first'):  # No types
        return getattr(self.session.query(self.model).filter_by(**filters), method)()
