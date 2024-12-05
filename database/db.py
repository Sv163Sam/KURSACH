from datetime import datetime

import sqlalchemy as db
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, text
from sqlalchemy import insert, delete, select
from sqlalchemy.orm import sessionmaker

# Создание соединения и метаданных
engine = db.create_engine('sqlite:///myDatabase.db')
metadata = db.MetaData()

BASE_STRING_SIZE = 255
HASH_SIZE = 16

Users = db.Table('User', metadata,
                 Column("id", Integer, primary_key=True),
                 Column("login", String(BASE_STRING_SIZE)),
                 Column("password", String(HASH_SIZE)),
                 Column("email", String(BASE_STRING_SIZE)),
                 Column("wallet", Integer, default=10))

Action_types = db.Table('Action_type', metadata,
                        Column("id", Integer, primary_key=True),
                        Column("type", String(BASE_STRING_SIZE)))

Transactions = db.Table('Transaction', metadata,
                        Column("id", Integer, primary_key=True),
                        Column("cost", Float))

Actions = db.Table('Action', metadata,
                   Column("id", Integer, primary_key=True),
                   Column("type_id", Integer, ForeignKey(Action_types.c.id)),
                   Column("date",  DateTime(), default=datetime.now),
                   Column("token_cost", Integer, nullable=True, default=None),
                   Column("transaction_id", Integer, ForeignKey(Transactions.c.id), nullable=True, default=None),
                   Column("user_id", Integer, ForeignKey(Users.c.id)))

if not engine.dialect.has_table(engine.connect(), 'User'):
    metadata.create_all(engine)

if not engine.dialect.has_table(engine.connect(), 'Action_type'):
    metadata.create_all(engine)

if not engine.dialect.has_table(engine.connect(), 'Transaction'):
    metadata.create_all(engine)

if not engine.dialect.has_table(engine.connect(), 'Action'):
    metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


#### Вставка пользователя
def insert_user(login: str, password: str, email: str):
    insert_user = insert(Users).values(login=login, password=password, email=email)
    with engine.connect() as connection:
        connection.execute(insert_user)
        connection.commit()


#### Вставка типа действия
def insert_action_type(id : int, type : str):
    insert_action_type = insert(Action_types).values(id=id, type=type)
    with engine.connect() as connection:
        connection.execute(insert_action_type)
        connection.commit()


#### Вставка транзакции
def insert_transaction(cost):
    insert_transaction = insert(Transactions).values(cost=cost)
    with engine.connect() as connection:
        result = connection.execute(insert_transaction)
        connection.commit()


#### Вставка действия
def insert_action(user_id, type_id, token_cost):
    insert_action = insert(Actions).values(type_id=type_id, token_cost=token_cost, user_id=user_id)
    with engine.connect() as connection:
        connection.execute(insert_action)
        connection.commit()


#### Выбор всех пользователей
def select_users(name: str):
    select_user = select(Users).where(Users.c.login == name)
    with engine.connect() as connection:
        result = connection.execute(select_user)
        connection.commit()
    return result.all()

#### Выбор всех типов действий
def select_action_types(id: int):
    select_action_type = select(Action_types).where(Action_types.c.id == id)
    with engine.connect() as connection:
        result = connection.execute(select_action_type)
        connection.commit()
    return result.all()


#### Выбор всех транзакций
def select_transactions(id: int):
    select_transaction = select(Transactions).where(Transactions.c.id == id)
    with engine.connect() as connection:
        result = connection.execute(select_transaction)
        connection.commit()
    return result.all()


#### Выбор всех действий для конкретного пользователя
def select_actions(id: int):
    select_action = select(Actions).where(Actions.c.user_id == id)
    with engine.connect() as connection:
        result = connection.execute(select_action)
        connection.commit()
    return select_action


#### Удаление пользователя
def delete_users(id: int):
    delete_user = delete(Users).where(Users.c.id == id)
    with engine.connect() as connection:
        connection.execute(delete_user)
        connection.commit()
    return delete_user


#### Удаление типа действия
def delete_action_types(id : int):
    delete_action_type = delete(Action_types).where(Action_types.c.id == id)
    with engine.connect() as connection:
        connection.execute(delete_action_type)
        connection.commit()
    return delete_action_type


#### Удаление транзакции
def delete_transactions(id: int):
    delete_transaction = delete(Transactions).where(Transactions.c.id == id)
    with engine.connect() as connection:
        connection.execute(delete_transaction)
        connection.commit()
    return delete_transaction

#### Удаление действия
def delete_actions(id: int):
    delete_action = delete(Actions).where(Actions.c.id == id)
    with engine.connect() as connection:
        connection.execute(delete_action)
        connection.commit()
    return delete_action

"""
insert_action_type(1,"video")
insert_action_type(2,"image")
insert_action_type(3,"transaction")

#print(select_action_types(3)[0])

# Create the trigger
"""
cond = """DROP TRIGGER IF EXISTS update_wallet_after_insert;"""
trigger_sql = """
CREATE TRIGGER update_wallet_after_insert
AFTER INSERT ON Action
FOR EACH ROW
BEGIN
    UPDATE User
    SET wallet =
        CASE
            WHEN NEW.type_id = 1 THEN wallet - 2
            WHEN NEW.type_id = 2 THEN wallet - 1
            WHEN NEW.type_id = 3 THEN wallet + 3
            ELSE wallet
        END
    WHERE id = NEW.user_id;
END;
"""
# Execute the trigger creation

with engine.connect() as conn:
    conn.execute(text(cond))
    conn.execute(text(trigger_sql))
    conn.commit()
"""
insert_user("abvgd", "dksdk", "sacsd@mail")

insert_action(1, 1, 2)
print(select_users("abvgd")[0])"""