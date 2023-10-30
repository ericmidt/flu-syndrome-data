## Description
This program consumes an API for notifications of influenza-like illness in Paraná and inserts the data into a local PostgreSQL database.


## Requirements

- Python 3.11.4 or higher
- Installed and configured PostgreSQL (and pgAdmin4 to test the local database if you prefer a GUI)


## Influenza Notifications in Paraná (Data Modeling and Processing):

The "flu_notifications.py" program in the "flu_syndrome_data" folder consumes the [Brazilian government's API for notifications of influenza-like illness](https://dados.gov.br/dados/conjuntos-dados/notificaes-de-sndrome-gripal---api-elasticsearch) and inserts the data into a local PostgreSQL database.


Follow these steps to run the program:
1. Clone the repository locally in the directory of your choice:
    ```bash
    git clone https://github.com/ericmidt/flu-syndrome-data.git
    ```

2. In the "flu-syndrome-data" directory, install the dependencies using the following command:

    ```bash
    pip install -r requirements.txt
    ```

3. Set your environment variables using the following commands in your terminal:

    Linux / macOS (Bash or Terminal):
    ```bash
    export DB_NAME="your_db_name"
    export DB_USER="your_user"
    export DB_PASSWORD="your_password"
    export DB_HOST="localhost"
    export DB_PORT="your_port"
    ```
    Windows PowerShell:
    ```bash 
    $env:DB_NAME="your_db_name"
    $env:DB_USER="your_user"
    $env:DB_PASSWORD="your_password"
    $env:DB_HOST="localhost"
    $env:DB_PORT="your_port"
    ```

    Windows Command Prompt:
    ```bash
    set DB_NAME=your_db_name
    set DB_USER=your_user
    set DB_PASSWORD=your_password
    set DB_HOST=localhost
    set DB_PORT=your_port
    ```

    Example:
    ```bash
    set DB_NAME=postgres
    set DB_USER=postgres
    set DB_PASSWORD=password
    set DB_HOST=localhost
    set DB_PORT=5432
    ```

4. Run the program with the following command:

    ```bash
    python flu_data_processor.py
    ```

## Tests
Open the pgAdmin4 program, right-click on the "Tables" section, and click "Refresh."
You should see a new table called "Flu_syndrome_data." Right-click in the "Tables" section,
click "Query Tool." Then, you can perform a query to
check the saved data, for example:


```sql
SELECT * FROM Flu_syndrome_data
```
