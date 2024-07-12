"""
Do not use this ( using Python locks to prevent DB race conditions) in production for DB operations.
Instead, use SQL locks to set locks at the database level to prevent race conditions.
"""

from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from sqlmodel import Session, select

from db import engine, Account, init_db

account_lock = Lock()


def transfer_money(from_id, to_id, amount):
    with Session(engine) as session:
        # building SQL queries
        from_user = select(Account).where(Account.id == from_id)
        to_user = select(Account).where(Account.id == to_id)

        with account_lock:
            # executing SQL queries
            from_user = session.exec(from_user).one()
            to_user = session.exec(to_user).one()

            # Update the balance
            from_user.balance -= amount
            to_user.balance += amount

            # Save updated balance to DB
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
