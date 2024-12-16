
# Telegram Message Archiver

Telegram Message Archiver is a tool to archive messages from Telegram dialogs into a database.

## Features

- Connects to Telegram using Telethon
- Archives messages from Telegram dialogs
- Stores messages in a database using SQLAlchemy
- Provides CLI commands for initializing the database and running the archiver

## Requirements

- Python 3.8+
- MySQL (or any other SQLAlchemy-supported database)
- Telethon
- SQLAlchemy
- Click

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/telegram_messages_archiver.git
    cd telegram_messages_archiver
    ```

2. Install Poetry:
    ```sh
    pip install poetry
    ```

3. Install the required packages:
    ```sh
    poetry install
    ```

4. Get Telegram API credentials:
   - Go to [my.telegram.org](https://my.telegram.org) and log in with your phone number.
   - Navigate to **API development tools** and create a new application.
   - Copy the **API ID** and **API Hash**.

5. Create a `.env` file:
   - In the root of your project directory, create a file named `.env`.
   - Fill settings according to Configuration section below.
   - Fill Database settings for creating Docker container.

6. Create docker container with Database:
   ```sh
   docker-compose up -d
   ```

## Configuration

- API_ID: Your Telegram API ID 
- API_HASH: Your Telegram API Hash
- PHONE: Your Telegram phone number
- MYSQL_DATABASE: Name of Database (you can leave default name). Using for Docker container
- MYSQL_USER: User name for Database (default is "user"). Using for Docker container
- MYSQL_PASSWORD: Password for Mysql User. Using for Docker container
- MYSQL_ROOT_PASSWORD: Password for Mysql Root User. Using for Docker container
- DB_PORT: This is local port for connection to Database. !!! Don't change it if you use Docker !!!
- DB_DOCKER_PORT: Port for connection to Docker container (default is 33006)
- MESSAGE_LIMIT: Limit of messages to fetch per dialog
- DSN: Data Source Name for the database (you may leave as is)
- DEBUG: Enable debug messages (true/false)

### Example configuration for PostgreSQL Database and Docker
   example file .envdbsampleforpostgres
- POSTGRES_DB: Name of Database. Using for Docker container
- POSTGRES_PASSWORD: Password for Postgres User. Using for Docker container
- DB_PORT: This is local port for connection to Database. !!! Don't change it if you use Docker !!! 
- DB_DOCKER_PORT: Port for connection to Docker container (default 54320)
- DSN: Data Source Name for the database (you may leave as is)

## Usage

```sh
poetry shell
```

1. Initialize the Database

   To initialize the database, run:
   ```sh
   python . initdb
   ```

2. Run the script:
   ```sh
   python .
   ```

## Troubleshooting

- **Session errors**: If you're prompted for 2FA, enter the password to complete the login.
- **Connection issues**: Ensure you have an active internet connection and correct API credentials.
- If you run docker compose without filled env credentials, you can get error with connection to database. 
Please fill .env file with correct credentials. And run `docker-compose up -d --build`.

## Acknowledgment
This project was started by [@MiguelTracelon] (https://www.github.com/MiguelTracelon)

Special thank to:
- Tacelon (https://tracelon.com) for initial realease
- People from SEAL (https://securityalliance.org/) for ideological support
## Notes

- **Privacy and Permissions**: Ensure you have permission to fetch and store messages, especially from groups and channels.
- **Rate Limits**: Avoid running the script too frequently to prevent triggering Telegram's rate limits.

## License

This project is open-source and available under the GPL v3 License.
