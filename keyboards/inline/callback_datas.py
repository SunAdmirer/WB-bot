from aiogram.utils.callback_data import CallbackData

# CallbackData для кнопки Назад, главного меню и тд
back_btn_cd = CallbackData('back_btn', 'nav_btn')

# CallbackData для главного меню
main_menu_cd = CallbackData('main_menu', 'nav_btn')

# CallbackData для настройки уведомлений
notifications_cd = CallbackData("notifications", "status")

# CallbackData для меню создания заказа
create_order_menu_cd = CallbackData('create_order_menu', 'nav_btn')
