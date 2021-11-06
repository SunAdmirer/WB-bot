from datetime import datetime
from typing import List

from utils.db_api.models import Orders, ReservedOrders, PerformedOrders, ModerateOrders
from loguru import logger


# Добавить заказ в модерацию
async def add_moderate_order(order_id: int, user_id: int):
    try:
        await ModerateOrders(order_id=order_id, user_id=user_id).create()
    except Exception as ex:
        logger.info(ex)


# Добавление заказа
async def add_order(user_id: int, type_order: str) -> Orders:
    try:
        # Получение даты и время
        date = datetime.now()

        # Имя для заказа
        order_name = f"{date.day}.{date.month} - {date.hour}:{date.minute}"

        return await Orders(order_name=order_name, user_id=user_id, type_order=type_order).create()
    except Exception as ex:
        logger.info(ex)


# Получение заказа по id
async def get_order_by_id(order_id: int) -> Orders:
    try:
        return await Orders.query.where(Orders.id == order_id).gino.first()
    except Exception as ex:
        logger.info(ex)


# Получаем все задания, которые подтвердили и оплатили, но еще не выполненные
async def get_confirmed_paid_for_orders() -> List[Orders]:
    try:
        return await Orders.query.where(
            (Orders.confirmed == True) & (Orders.paid_for == True) &
            (Orders.performed == False) & (Orders.goal_amount != Orders.total_amount)
        ).gino.all()
    except Exception as ex:
        logger.info(ex)


# Получаем все неоплаченные заказы пользователя
async def get_unpaid_orders(user_id: int) -> List[Orders]:
    try:
        return await Orders.query.where(
            (Orders.user_id == user_id) & (Orders.confirmed == True) & (Orders.paid_for == False)
        ).gino.all()
    except Exception as ex:
        logger.info(ex)


# Получаем выполненные задания исполнителя
async def get_performed_performers_orders(user_id: int) -> List[PerformedOrders]:
    try:
        return await PerformedOrders.query.where(
            (PerformedOrders.user_id == user_id)
        ).gino.all()
    except Exception as ex:
        logger.info(ex)


# Получаем задания что ожидают выполнения исполнителя
async def get_reserved_performers_orders(user_id: int) -> List[ReservedOrders]:
    try:
        reserved = await ReservedOrders.query.where(
            (ReservedOrders.user_id == user_id)
        ).gino.all()

        moderate = await ModerateOrders.query.where(
            (ModerateOrders.user_id == user_id)
        ).gino.all()

        # orders = [order for order in reserved if order not in moderate]
        orders = []

        for order_res in reserved:
            fl = False
            for order_mod in moderate:
                if order_res.order_id == order_mod.order_id:
                    fl = True

            if fl is False:
                orders.append(order_res)

        return orders
    except Exception as ex:
        logger.info(ex)


# Получаем задания на модерации исполнителя
async def get_moderate_performers_orders(user_id: int) -> List[ModerateOrders]:
    try:
        return await ModerateOrders.query.where(
            (Orders.user_id == user_id)
        ).gino.all()
    except Exception as ex:
        logger.info(ex)


# Получаем выполненные задания заказчика
async def get_performed_customers_orders(user_id: int) -> List[Orders]:
    try:
        return await Orders.query.where(
            (Orders.user_id == user_id) & (Orders.performed == True)
        ).gino.all()
    except Exception as ex:
        logger.info(ex)


# Получаем задания в процессе заказчика
async def get_in_process_customers_orders(user_id: int) -> List[Orders]:
    try:
        return await Orders.query.where(
            (Orders.user_id == user_id) & (Orders.performed == False)
            & (Orders.confirmed == True) & (Orders.paid_for == True)
        ).gino.all()
    except Exception as ex:
        logger.info(ex)


# Проверяем есть ли у заказчика заказы
async def check_is_customers_orders(user_id: int) -> bool:
    try:
        check = await Orders.query.where(Orders.user_id == user_id).gino.first()

        if check:
            return True
        else:
            return False
    except Exception as ex:
        logger.info(ex)


# Проверяем есть ли у исполнителя Выполненные/В процессе модерации/Ожидают выполнения заказы
async def check_is_performers_orders(user_id: int) -> bool:
    try:
        check_1 = await ReservedOrders.query.where(ReservedOrders.user_id == user_id).gino.first()
        check_2 = await PerformedOrders.query.where(PerformedOrders.user_id == user_id).gino.first()
        check_3 = await ModerateOrders.query.where(ModerateOrders.user_id == user_id).gino.first()

        if check_1 or check_2 or check_3:
            return True
        else:
            return False
    except Exception as ex:
        logger.info(ex)


# Получаем кол-во выполненных заказов заказчика
async def get_count_performed_orders(user_id: int) -> int:
    try:
        orders = await Orders.query.where(
            (Orders.user_id == user_id) & (Orders.performed == True)
        ).gino.all()

        return len(orders)
    except Exception as ex:
        logger.info(ex)


# Получаем кол-во заказов в процессе заказчика
async def get_count_in_process_orders(user_id: int) -> int:
    try:
        orders = await Orders.query.where(
            (Orders.user_id == user_id) & (Orders.performed == False)
            & (Orders.confirmed == True) & (Orders.paid_for == True)
        ).gino.all()

        return len(orders)
    except Exception as ex:
        logger.info(ex)


# Получаем кол-во выполненных заказов исполнителя
async def get_count_performed_orders_performer(user_id: int) -> int:
    try:
        orders = await PerformedOrders.query.where(
            (PerformedOrders.user_id == user_id)
        ).gino.all()

        return len(orders)
    except Exception as ex:
        logger.info(ex)


# Получаем кол-во заказов на модерации исполнителя
async def get_count_moderate_orders(user_id: int) -> int:
    try:
        orders = await ModerateOrders.query.where(
            (ModerateOrders.user_id == user_id)
        ).gino.all()

        return len(orders)
    except Exception as ex:
        logger.info(ex)


# Получаем кол-во заказов что ожидают выполнения исполнителя
async def get_count_reserved_orders(user_id: int) -> int:
    try:
        reserved = await ReservedOrders.query.where(
            (ReservedOrders.user_id == user_id)
        ).gino.all()

        moderate = await ModerateOrders.query.where(
            (ModerateOrders.user_id == user_id)
        ).gino.all()

        # orders = [order for order in reserved if order not in moderate]
        orders = []

        for order_res in reserved:
            fl = False
            for order_mod in moderate:
                if order_res.order_id == order_mod.order_id:
                    fl = True

            if fl is False:
                orders.append(order_res)

        return len(orders)

    except Exception as ex:
        logger.info(ex)


# Обновляем goal_amount заказа
async def update_order_goal_amount_order_cost_by_id(order_id: int, goal_amount: int, order_cost: float):
    try:
        await Orders.update.values(goal_amount=goal_amount,
                                   order_cost=order_cost).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Обновляем goods_name заказа
async def update_order_goods_name_by_id(order_id: int, goods_name: str):
    try:
        await Orders.update.values(goods_name=goods_name).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Обновляем order_description заказа
async def update_order_description_by_id(order_id: int, order_description: str):
    try:
        await Orders.update.values(order_description=order_description).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Обновляем order_description заказа
async def update_order_goods_cost_by_id(order_id: int, goods_cost: float):
    try:
        await Orders.update.values(goods_cost=goods_cost).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Обновляем cashback заказа
async def update_order_cashback_by_id(order_id: int, cashback: int):
    try:
        await Orders.update.values(cashback=cashback).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Обновляем goods_link заказа
async def update_order_goods_link_by_id(order_id: int, goods_link: str):
    try:
        await Orders.update.values(goods_link=goods_link).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Обновляем contacts заказа
async def update_order_contacts_by_id(order_id: int, contacts: str):
    try:
        await Orders.update.values(contacts=contacts).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Обновляем confirmed заказа
async def update_order_confirmed_by_id(order_id: int, confirmed: bool):
    try:
        await Orders.update.values(confirmed=confirmed).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Обновляем paid_for заказа
async def update_order_paid_for_by_id(order_id: int, paid_for: bool):
    try:
        await Orders.update.values(paid_for=paid_for).where(Orders.id == order_id).gino.status()
    except Exception as ex:
        logger.info(ex)
