from typing import List

from utils.db_api.models import Orders, PerformedOrders, ReservedOrders


async def check_order_if_suitable(order: Orders, check_orders: List[PerformedOrders or ReservedOrders]) -> bool:
    for check_order in check_orders:
        if order.id == check_order.order_id:
            return False

    return True