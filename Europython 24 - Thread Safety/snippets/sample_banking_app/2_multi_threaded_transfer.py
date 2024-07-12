from concurrent.futures import ThreadPoolExecutor
from sqlmodel import Session, select

from db import init_db, engine, Account


def transfer_money(from_id, to_id, amount):
    with Session(engine) as session:
        from_user = select(Account).where(Account.id == from_id)
        to_user = select(Account).where(Account.id == to_id)
        from_user = session.exec(from_user).one()
        to_user = session.exec(to_user).one()
        from_user.balance -= amount
        to_user.balance += amount
        session.add(from_user)
        session.add(to_user)
        session.commit()


def display_balance():
    with Session(engine) as session:
        statement = select(Account)
        results = session.exec(statement)
        for result in results:
            print(result.balance)


if __name__ == '__main__':

    init_db()
    display_balance()

    print("doing transfers")
    to_transfer = [(1, 2, 10), (2, 3, 10), (1, 3, 10), (3, 1, 10)]
    with ThreadPoolExecutor(max_workers=10) as executor:
        for from_id, to_id, amount in to_transfer:
            executor.submit(transfer_money, from_id, to_id, amount)

    display_balance()
