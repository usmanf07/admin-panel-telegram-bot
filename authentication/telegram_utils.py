import telegram

TOKEN = 'ENTER BOT TOKEN HERE'

async def get_username_from_telegram(user_id):
    # Create a Telegram bot instance
    bot = telegram.Bot(token=TOKEN)

    try:
        # Get the user object from Telegram
        user = await bot.get_chat(user_id)
        username = user.username if user.username else 'N/A'

        return username

    except Exception as e:
        print('An error occurred while retrieving the username:', e)
        return None
    
async def send_message_to_telegram_user(user_id, message):
    # Create a Telegram bot instance
    bot = telegram.Bot(token=TOKEN)

    try:
        await bot.send_message(chat_id=user_id, text=message)

    except Exception as e:
        print('An error occurred while sending the message:', e)

async def send_message_to_telegram_user_with_image(user_id, message, image_data):
    # Create a Telegram bot instance
    bot = telegram.Bot(token=TOKEN)

    try:
        # Send the message with the image data
        await bot.send_photo(chat_id=user_id, photo=image_data, caption=message)

    except Exception as e:
        print('An error occurred while sending the message:', e)

async def broadcast_message_to_telegram_users(message, chat_ids):
    bot = telegram.Bot(token=TOKEN)

    try:
        for i, chat_id in enumerate(chat_ids):
            try:
                print('id', chat_id)
                await bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                print('An error occurred while sending the message:', e)
                # Handle the exception or log the error as per your requirements
                continue  # Skip this iteration and move to the next chat_id

    except Exception as e:
        print('An error occurred while sending the message:', e)

async def broadcast_message_to_telegram_users_with_image(message, chat_ids, image_data):
    # Create a Telegram bot instance
    bot = telegram.Bot(token=TOKEN)

    try:
        for i, chat_id in enumerate(chat_ids):
            try:
                print('id', chat_id)
                await bot.send_photo(chat_id=chat_id, photo=image_data, caption=message)
            except Exception as e:
                print('An error occurred while sending the message:', e)
                # Handle the exception or log the error as per your requirements
                continue  # Skip this iteration and move to the next chat_id

    except Exception as e:
        print('An error occurred while sending the message:', e)
