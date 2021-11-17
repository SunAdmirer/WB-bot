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


class Transaction(TimedBaseModel):
    __tablename__ = 'transactions'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)
    amount = sa.Column(sa.Numeric(precision=10, scale=2), default=0, nullable=False)  # Сумма пополнения

    def __repr__(self):
        return f"{self.id}"


# Таблица рекрутеров и рекрутов
class Referrals(TimedBaseModel):
    __tablename__ = 'referrals'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    recruiter_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"),
                             index=True)  # Кто привел
    recruit_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"),
                           index=True)  # Кого привели
    bonus = sa.Column(sa.Boolean, default=True)  # True - бонус еще не получен

    def __repr__(self):
        return f"{self.id}"


# Таблица заказов. На выполнении|Ожидают оплаты|Выполнены
class Orders(TimedBaseModel):
    __tablename__ = 'orders'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    order_name = sa.Column(sa.String(30), nullable=False, index=True)  # Название задания 20.04 - 12:05
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), index=True)
    type_order = sa.Column(sa.String(10), nullable=False, index=True)
    goal_amount = sa.Column(sa.Integer, default=0, nullable=False)  # Сколько нужно выполнений
    total_amount = sa.Column(sa.Integer, default=0, nullable=False)  # Сколько уже выполнили
    goods_name = sa.Column(sa.String(40), default='-', nullable=False)  # Название товара
    order_description = sa.Column(sa.String(400), default='-', nullable=False)  # Описание задания
    goods_link = sa.Column(sa.String(255), default='-', nullable=False)  # Ссылка на товар
    contacts = sa.Column(sa.String(255), default='-', nullable=False)  # Контакт (для связи с админом)
    goods_cost = sa.Column(sa.Numeric(precision=10, scale=2), default=0, nullable=False)  # Стоимость товара
    cashback = sa.Column(sa.Integer, default=0, nullable=False)  # Кэшбек/скидка
    order_cost = sa.Column(sa.Numeric(precision=10, scale=2), default=0, nullable=False)  # Стоимость задания
    confirmed = sa.Column(sa.Boolean, default=False, nullable=False)  # Подтвержден ли заказ
    paid_for = sa.Column(sa.Boolean, default=False, nullable=False)  # Оплачен ли заказ
    performed = sa.Column(sa.Boolean, default=False, nullable=False)  # Выполнен ли заказ

    def __repr__(self):
        return f"{self.id}"


# Таблица зарезервированных заказов
class ReservedOrders(TimedBaseModel):
    __tablename__ = 'reserved_orders'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id', ondelete="CASCADE", onupdate="CASCADE"),
                         index=True)  # Задание, которое зарезервировали
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"),
                        index=True)  # Пользователь, который зарезервировал задание

    def __repr__(self):
        return f"{self.order_id}"


# Таблица выполненных заданий исполнителя
class PerformedOrders(TimedBaseModel):
    __tablename__ = 'performed_orders'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id', ondelete="CASCADE", onupdate="CASCADE"),
                         index=True)  # Задание, которое выполнили
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"),
                        index=True)  # Пользователь, который выполнил задание

    def __repr__(self):
        return f"{self.id}"


# Таблица заказов, что проходят модерацию
class ModerateOrders(TimedBaseModel):
    __tablename__ = 'moderate_orders'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id', ondelete="CASCADE", onupdate="CASCADE"),
                         index=True)  # Задание, которое проходят модерацию
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"),
                        index=True)  # Пользователь, который "Выполнил" задание
    confirmed_by_admin = sa.Column(sa.Boolean, default=False, nullable=False)  # Админ подтвердил выполнение

    def __repr__(self):
        return f"{self.order_id}"


# Таблица скриншотов под выполненными заказами
class MediaContent(TimedBaseModel):
    __tablename__ = 'media_content'

    query: sa.sql.Select

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)
    moderate_order_id = sa.Column(sa.Integer,
                                  sa.ForeignKey('moderate_orders.id', ondelete="CASCADE", onupdate="CASCADE"),
                                  index=True)  # Задание, которое проходят модерацию
    file_id = sa.Column(sa.String)  # File id фото
