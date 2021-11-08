from aiogram.utils.callback_data import CallbackData

# CallbackData для кнопки Назад, главного меню и тд
back_btn_cd = CallbackData('back_btn', 'nav_btn')

balance_menu_cd = CallbackData('balance_menu', 'order_id')

# CallbackData для главного меню
main_menu_cd = CallbackData('main_menu', 'nav_btn')

# CallbackData для списка заданий
list_orders_cd = CallbackData('list_orders', 'nav_btn', 'order_id')

# CallbackData для настройки уведомлений
notifications_cd = CallbackData("notifications", "status")

# CallbackData для меню создания заказа
create_order_menu_cd = CallbackData('create_order_menu', 'nav_btn')

# CallbackData кол-во выполнений заказа типа 🔥 Выкуп + отзыв + ❤
fire_order_cd = CallbackData('fire_order', 'nav_btn')

# CallbackData подтверждение заказа типа 🔥 Выкуп + отзыв + ❤
confirm_fire_order_cd = CallbackData('confirm_fire_order', 'nav_btn')

# CallbackData кол-во выполнений заказа типа 💰 Выкуп
redemption_order_cd = CallbackData('redemption_order', 'nav_btn')

# CallbackData подтверждение заказа типа 💰 Выкуп
confirm_redemption_order_cd = CallbackData('confirm_redemption_order_cd', 'nav_btn')

# CallbackData кол-во выполнений заказа типа ❤ Избранное
favorites_order_cd = CallbackData('favorites_order', 'nav_btn')

# CallbackData подтверждение заказа типа ❤ Избранное
confirm_favorites_order_cd = CallbackData('confirm_favorites_order', 'nav_btn')

# CallbackData для выбора ✅ Выполненные/⏳ В процессе выполнения
customers_with_orders_cd = CallbackData('customers_with_orders', 'nav_btn')

# CallbackData для выбора задания в Мои заказы (Для заказчика)
choose_customers_orders_cd = CallbackData('choose_customers_orders', 'order')

# CallbackData для для пагинации выбора задания в Мои заказы (Для заказчика)
paginator_customers_cd = CallbackData('paginator_customers', 'type_order', 'page')

# CallbackData для выбора ✅ Выполненные/Ожидают выполнения/⏳ Модерация
performers_with_orders_cd = CallbackData('performers_with_orders', 'nav_btn')

# CallbackData для выбора задания в Мои заказы (Для исполнителя)
choose_performers_orders_cd = CallbackData('choose_performers_orders', 'order', 'type_order')

# CallbackData выбранного задания категории В процессе выполнения Исполнитель
chosen_performers_reserved_order_cd = CallbackData('chosen_performers_reserved_order', 'order', 'type_order')

# CallbackData Кнопка Выполнено. Заполнение формы на проверку
check_for_execution_cd = CallbackData('check_for_execution', 'order', 'type_order')

# CallbackData для для пагинации выбора задания в Мои заказы (Для исполнителя)
paginator_performers_cd = CallbackData('paginator_performers', 'type_order', 'page')
