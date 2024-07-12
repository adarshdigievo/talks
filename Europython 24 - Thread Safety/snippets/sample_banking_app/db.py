from sqlalchemy import delete
from sqlmodel import Field, Session, SQLModel, create_engine


def setup_db(engine):
    with Session(engine) as session:
        statement = delete(Account)
        result = session.exec(statement)
        session.commit()

    acc_1 = Account(id=1, name="John", balance=100)
    acc_2 = Account(id=2, name="Jane", balance=100)
    acc_3 = Account(id=3, name="Alice", balance=100)

    with Session(engine) as session:
        session.add(acc_1)
        session.add(acc_2)
        session.add(acc_3)
        session.commit()


class Account(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    balance: float


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)

    setup_db(engine)
