from aiogram import Bot, Dispatcher, executor, types
from config import telegram_token
import database

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

database.init_db()
async def on_startup(_):
    print('Я запустился')

@dp.message_handler(commands='start')
async def start_command(message: types.Message): #Задаем ассихронную функцию start_command,
# где у нас будет передаваться message с типом данных Message
    await message.answer(text='Привет! Я бот To-Do list, созданный помочь тебе организовать свои дела и оставаться продуктивным. Давай начнём с добавления твоих первых задач. Просто отправь мне сообщение с текстом «Добавить задачу» и опиши, что нужно сделать. Я также могу помочь установить срок выполнения и напоминание.')

@dp.message_handler(commands='add')
async def add_command(message: types.Message):
    task = message.get_args()
    if task:
        user_id = message.from_user.id
        username = message.from_user.username
        database.add_task(user_id, username, task)
        await message.answer(f"Задача {task} добавлена")
    else:
        await message.answer('Пожалуйста, укажите задачу через предоставленную комманду /add')

@dp.message_handler(commands='list')
async def list_command(message: types.Message):
    tasks = database.get_task()
    if tasks:
        tasks_list = "\n".join([f"{task[0]}. {task[3]} (Добавлена пользователем @{task[2]})" for task in tasks])
        await message.answer(f"Ваши задачи: \n{tasks_list}")
    else:
        await message.answer('У вас нету задач')

@dp.message_handler(commands='delete')
async def delete_command(message: types.Message):
    task_id = message.get_args()
    if task_id.isdigit():
        database.delete_task(int(task_id))
        await message.answer(f"Задача {task_id} удалена")
    else:
        await message.answer('Укажите корректный id задачи')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)