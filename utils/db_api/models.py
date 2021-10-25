import sqlalchemy as sa

from utils.db_api.database import db


# Время добавление/обновления данных
class TimedBaseModel(db.Model):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(True), server_default=db.func.now())
    updated_at = sa.Column(sa.DateTime(True),
                           default=db.func.now(),
                           onupdate=db.func.now(),
                           server_default=db.func.now())


# Таблица цен на услуги
class PriceList(db.Model):
    __tablename__ = "price_list"

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    name = sa.Column(sa.String(50), nullable=False, unique=True, index=True)
    price = sa.Column(sa.Numeric(precision=6, scale=2), nullable=False)


# Таблица юзеров
class Users(TimedBaseModel):
    __tablename__ = 'users'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    telegram_id = sa.Column(sa.BigInteger, unique=True, nullable=False, index=True)
    username = sa.Column(sa.String(32), nullable=False, index=True)
    balance = sa.Column(sa.Numeric(precision=10, scale=2), default=0, nullable=False)
    balance_from_ref = sa.Column(sa.Numeric(precision=10, scale=2), default=0, nullable=False)
    notifications = sa.Column(sa.Boolean, default=True, nullable=False)
    restricted = sa.Column(sa.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"{self.telegram_id}"


# Таблица рекрутеров и рекрутов
class Referrals(TimedBaseModel):
    __tablename__ = 'referrals'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    recruiter_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)
    recruit_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)
    bonus = sa.Column(sa.Boolean, default=True)

    def __repr__(self):
        return f"{self.id}"


# Таблица типов заданий
class TypeOrders(TimedBaseModel):
    __tablename__ = 'type_orders'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    type_task = sa.Column(sa.String(50), nullable=False, index=True)

    def __repr__(self):
        return f"{self.id}"


# Таблица заказов. На выполнении|Ожидают оплаты|Выполнены
class Orders(TimedBaseModel):
    __tablename__ = 'orders'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    order_name = sa.Column(sa.String(30), nullable=False, index=True)  # Название задания 20.04 - 12:05
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)
    type_task_id = sa.Column(sa.Integer, sa.ForeignKey('type_orders.id', ondelete="CASCADE", onupdate="CASCADE"),
                             nullable=False, index=True)
    goal_amount = sa.Column(sa.Integer, nullable=False)  # Сколько нужно выполнений
    total_amount = sa.Column(sa.Integer, nullable=False)  # Сколько уже выполнили
    goods_name = sa.Column(sa.String(40), nullable=False)  # Название товара
    goods_description = sa.Column(sa.String(200), nullable=False)  # Описание товара
    order_description = sa.Column(sa.String(400), nullable=False)  # Описание задания
    goods_link = sa.Column(sa.String(255), nullable=False)  # Ссылка на товар
    contacts = sa.Column(sa.String(255), nullable=False)  # Контакт (для связи с админом)
    goods_cost = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False)  # Стоимость товара
    order_cost = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False)  # Стоимость задания
    paid_for = sa.Column(sa.Boolean, default=False, nullable=False)  # Оплачен ли заказ
    performed = sa.Column(sa.Boolean, default=False, nullable=False)  # Выполнен ли заказ

    def __repr__(self):
        return f"{self.id}"


# Таблица зарезервированных заказов
class ReservedOrders(TimedBaseModel):
    __tablename__ = 'reserved_orders'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)  # Задание, которое зарезервировали
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)  # Пользователь, который зарезервировал задание

    def __repr__(self):
        return f"{self.id}"


# Таблица заказов, что проходят модерацию
class ModerateOrders(TimedBaseModel):
    __tablename__ = 'moderate_orders'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)  # Задание, которое проходят модерацию
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)  # Пользователь, который "Выполнил" задание

    def __repr__(self):
        return f"{self.id}"
