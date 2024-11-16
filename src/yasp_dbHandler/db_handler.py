"""
Storing Stock informations, received from an API provider in a local
SQLite DB for analysis and presentation
"""
import os
import sqlite3
import json
import logging
from typing import Optional, Dict, Any, List
import requests


# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DbHandler:
    """
    A handler for managing database operations related to stock entries.

    Attributes:
        _dbFile (str): Path to the SQLite database file.
        _apiKey (str): API key for external services.
        _dbConfig (Dict): Database configuration loaded from a JSON file.
        _fieldMapping (Dict): API field mappings loaded from a JSON file.
        _connection (sqlite3.Connection): SQLite database connection.
    """

    def __init__(
        self,
        db_file: str,
        db_config_file: str = "db_config.json",
        mapping_config_file: str = "api_field_mapping.json",
    ):
        """
        Initializes the DbHandler with database and API configurations.

        Args:
            dbFile (str): Path to the SQLite database file.
            dbConfigFile (str, optional): Path to the database configuration JSON file.
                Defaults to "db_config.json".
            mappingConfigFile (str, optional): Path to the API field mapping JSON file.
                Defaults to "api_field_mapping.json".
        """

        self._db_config = self._load_config(db_config_file)
        self._field_mapping = self._load_config(mapping_config_file)
        self._connection = self._connect_db(db_file)
        try:
            self._check_config()
        except KeyError as e:
            logger.error("Error in mapping file: %s - %s",
                         mapping_config_file, str(e))
            raise
        self._initialize_db()
        logger.info("DbHandler initialized with dbFile: %s", db_file)
        self._api_key = os.getenv("FMP_API")
        if not self._api_key:
            raise EnvironmentError(
                "Environment variable FMP_API for API Key not defined")

    def _load_config(self, config_file: str) -> Dict:
        """
        Loads a JSON configuration file.

        Args:
            configFile (str): Path to the JSON configuration file.

        Returns:
            Dict: Parsed JSON configuration as a dictionary.
        """
        try:
            with open(config_file, 'r', encoding="utf-8") as f:
                config = json.load(f)
                logger.info("Loaded configuration from %s", config_file)
                return config
        except FileNotFoundError:
            logger.error("Configuration file not found: %s", config_file)
            raise
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON from file %s: %s",
                         config_file, str(e))
            raise

    def _connect_db(self, db_file) -> sqlite3.Connection:
        """
        Establishes a connection to the SQLite database.

        Returns:
            sqlite3.Connection: SQLite database connection object.
        """
        try:
            connection = sqlite3.connect(db_file)
            logger.info("Database connection established")
            return connection
        except sqlite3.Error as e:
            logger.error(
                "Database connection error from file %s: %s", db_file, str(e))
            raise

    def _initialize_db(self) -> None:
        """
        Initializes the database tables based on the database configuration.

        Creates tables if they do not already exist, using the specifications
        provided in the configuration file.
        """
        with self._connection:
            cursor = self._connection.cursor()
            # Execute a query to check if the table exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='stocks';")
            result = cursor.fetchone()  # Fetch one result, if exists

        if result:
            with self._connection:
                cursor = self._connection.cursor()
                # Query the table's schema
                cursor.execute("PRAGMA table_info('stocks');")
                columns = cursor.fetchall()
                for entry in self._db_config:
                    entry_exists = 0
                    for column in columns:
                        if entry == column[1]:
                            entry_exists = 1
                    if 0 == entry_exists:
                        add_sql = f"alter table stocks add column {
                            entry} {self._db_config[entry]}"
                        cursor.execute(add_sql)
                        logger.info(
                            'create new db entry for: %s with type %s', entry, self._db_config[entry])
        else:
            field_definitions = ""
            for entry in self._db_config:
                field_definitions += entry + ' ' + \
                    str(self._db_config[entry]) + ','
            field_definitions = field_definitions[:-1]

            with self._connection:
                create_table_query = f"create table if not exists stocks ({
                    field_definitions})"
                self._connection.execute(create_table_query)
                logger.info(
                    "Table stocks initialized with fields: %s", field_definitions)

    def _check_config(self):
        """
        Check consistance of configurations from database config and field mapping

        Raises:
            Exception: If DB field, assigned to API return value is not in DB config
        """
        for api in self._field_mapping:
            for api_field in self._field_mapping[api]['mapping']:
                logger.debug(
                    "Check Config: %s", self._field_mapping[api]['mapping'][api_field])
                if self._field_mapping[api]['mapping'][api_field] not in self._db_config:
                    logger.error(
                        "No database field found for api mapping: %s - %s : %s",
                        api, api_field, str(self._field_mapping[api]['mapping'][api_field]))
                    raise KeyError(
                        "Content of DB configuration and API Mapping inconsistnent")

    def _map_api_data_to_db_fields(self, api_name: str, search_value: str) -> Dict[str, Any]:

        # setup request url and parameters, depending if the search parameter is a parameter or part of url
        if self._field_mapping[api_name]["search_param"]:
            request_url = self._field_mapping[api_name]["base_url"]
            request_params = self._field_mapping[api_name]["default_params"]
            request_params[self._field_mapping[api_name]
                           ["search_param"]] = search_value
        else:
            request_url = self._field_mapping[api_name]["base_url"] + search_value
            request_params = self._field_mapping[api_name]["default_params"]

        logger.debug("API Request: %s with params: %s",
                     request_url, request_params)

        request_params["apikey"] = self._api_key
        response = requests.get(
            request_url, params=request_params, timeout=30).content
        json_data = json.loads(response)

        # Check mapping config and try to assign response values to maped field
        mapped_data = {}
        for api_field in self._field_mapping[api_name]['mapping']:
            mapped_data[self._field_mapping[api_name]['mapping'][api_field]] = \
                json_data[self._field_mapping[api_name]
                          ["first_entry"]][api_field]
        print(mapped_data)

        return mapped_data

    def _insert_dict_into_table(self, table_name: str, data_dict: Dict[str, Any]) -> None:
        """
        Insert the provided dictionary into the database

        Args:
            table_name (str): Name of the table where the data should be inserted
            data_dict (Dict[str, Any]): Dictionary to insert into DB
        Raises:
            DatabaseError: Exception during database handling
            Exception: General exception
        """
        try:
            # Connect to the SQLite database
            with self._connection:
                cursor = self._connection.cursor()

                # Prepare the column names and placeholders for the SQL query
                columns = ', '.join(data_dict.keys())
                placeholders = ', '.join('?' for _ in data_dict)
                values = tuple(data_dict.values())

                # Construct and execute the SQL query
                sql_query = f"INSERT INTO {
                    table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql_query, values)
                self._connection.commit()

                logger.debug(
                    "Insert data to table: %s with query: %s, values: %s", table_name, sql_query, values)
        except sqlite3.DatabaseError as e:
            logger.error("Database error: %s", str(e))
            raise
        except Exception as e:
            logger.error("Error during DB insert operation: %s", str(e))
            raise

    def add_isin(self, isin: str) -> None:
        """
        Adds an ISIN entry with its symbol to the database.

        Args:
            isin (str): The International Securities Identification Number.
            symbol (str): The stock symbol associated with the ISIN.
        """
        # stock_data = {"isin": "DE0007164600", "company": "SAP", "symbol": "SAP"}
        stock_data = self._map_api_data_to_db_fields("search_isin", isin)
        self._insert_dict_into_table("stocks", stock_data)

    def get_all(
        self, filter_str: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves all entries from the database, optionally applying filters.

        Args:
            filter (Optional[Dict[str, str]], optional): A dictionary of column-value pairs to filter the results.
                Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the database entries.
        """

    def get_watchlist(
        self, filter_str: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves all entries that are currently in the watchlist, optionally applying filters.

        Args:
            filter (Optional[Dict[str, str]], optional): A dictionary of column-value pairs to filter the
                watchlist entries. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the watchlist entries.
        """

    def get_entry(
        self, isin: str, filter_str: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves a specific entry based on the provided ISIN, optionally applying additional filters.

        Args:
            isin (str): The International Securities Identification Number to search for.
            filter_str (Optional[Dict[str, str]], optional): A dictionary of additional column-value pairs to
                filter the result .Defaults to None.

        Returns:
            Optional[Dict[str, Any]]: A dictionary representing the entry if found, else None.
        """

    def update_entry(
        self, isin: str, api_data: Dict[str, Any], api_name: str
    ) -> None:
        """
        Updates a single database entry specified by its ISIN using data from a specified API.

        Args:
            isin (str): The International Securities Identification Number of the entry to update.
            api_data (Dict[str, Any]): The JSON data received from the API.
            api_name (str): The name of the API providing the data, used to determine field mappings.
        """

    def update_all(
        self, api_data_list: List[Dict[str, Any]], api_name: str
    ) -> None:
        """
        Updates all database entries based on a list of API data from a specified API.

        Args:
            api_data_list (List[Dict[str, Any]]): A list of JSON data dictionaries received from the API.
            api_name (str): The name of the API providing the data, used to determine field mappings.
        """

    def update_watchlist(
        self, api_data_list: List[Dict[str, Any]], api_name: str
    ) -> None:
        """
        Updates only the entries in the watchlist using data from a specified API.

        Args:
            api_data_list (List[Dict[str, Any]]): A list of JSON data dictionaries received from the API.
            api_name (str): The name of the API providing the data, used to determine field mappings.
        """

    def set_watchlist(self, isin: str, state: bool) -> None:
        """
        Adds or removes an entry from the watchlist based on the provided state.

        Args:
            isin (str): The International Securities Identification Number of the entry.
            state (bool): True to add to the watchlist, False to remove.
        """
        with self._connection:
            self._connection.execute(
                "UPDATE entries SET watchlist = ? WHERE isin = ?",
                (state, isin),
            )

    def __del__(self):
        """
        Ensures the database connection is closed when the DbHandler instance is deleted.
        """
        if self._connection:
            self._connection.close()
            logger.info("Database connection closed")
