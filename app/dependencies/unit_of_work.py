from app.unit_of_work.unit_of_work import SQLAlchemyUnitOfWork


def get_unit_of_work() -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork()
