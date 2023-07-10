# Admin Panel Telegram Bot

Admin Panel Telegram Bot is a Python Django application that provides an admin panel to manage and control a Telegram bot. This admin panel offers various features to efficiently manage the bot and interact with its users.

## Features

1. **Sending Message to Specific User**: The admin can use the admin panel to send messages to specific users of the Telegram bot. This feature allows personalized communication and targeted messaging.

2. **Sending Announcement to All Users**: The admin panel enables the admin to send announcements to all users of the Telegram bot. This feature is useful for broadcasting important information or updates to a large audience.

3. **User Search**: The admin can easily search for a specific user using the admin panel. This feature allows quick access to user information and facilitates targeted actions or support.

4. **View Statistics of Users**: The admin panel provides statistical insights into the bot's user activity. It displays daily and monthly graphs/charts to visualize the usage trends and patterns. Additionally, it also provides the total number of users.

## Technologies Used

- Python
- Django
- Telegram Bot API

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/usmanf07/admin-panel-telegram-bot.git
   ```

2. Change into the project directory:
    ```
    cd admin-panel-telegram-bot
    ```
3. Create and activate a virtual environment (optional but recommended):
    ```
    python3 -m venv env
    source env/bin/activate
    ```
4. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Configure the Telegram bot token:

- Open the `authentication/telegram_utils.py` file.
- Replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual Telegram bot token in the `TOKEN` variable.
- Also open the `core/main.py` file.
- Replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual Telegram bot token in the `TOKEN` variable.

6. Create sqlite DB and Apply the database migrations:
    ```
    Create the database named 'admin.db'
    python manage.py migrate
    ```

7. Run the development server:
    ```
    python manage.py runserver
    ```

8. Run the bot server:

- Open the `core` folder.
```
python main.py
```

## Usage

1. Access the admin panel by logging in with your admin credentials.
![login](https://i.ibb.co/jM6ktGB/image.png)
2. Use the various features provided by the admin panel to manage your Telegram bot efficiently.
![home](https://i.ibb.co/nR6bvkf/image.png)
3. Explore user statistics, send messages or announcements, search for users, and more.
![stats](https://i.ibb.co/ygw6PGN/image.png)
![messages](https://i.ibb.co/GTBQhm6/image.png)
## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your contribution.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request explaining your changes.

## Acknowledgements

- This project was inspired by the need for an efficient admin panel to manage Telegram bots.
- We would like to thank the Python, Django, and Telegram Bot API communities for their excellent documentation and resources.


