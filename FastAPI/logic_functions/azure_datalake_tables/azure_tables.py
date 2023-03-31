# pip install --pre azure-data-tables
# pip install python-dotenv

from dotenv import find_dotenv, load_dotenv
from azure.data.tables import TableClient
from azure.core.exceptions import HttpResponseError
import json, base64
from time import sleep

# Author: Lidor Eliyahu Shelef

class TableEntityDatalake(object):
    """
        A class representing the tables in the Azure datalake (deltalake - Databricks) (In Tables)
    """
    
    def __init__(self) -> None:
        # Init method to activate the env functions that Azure requires
        # Set default variables to the self object
        load_dotenv(find_dotenv())
        self.connection_string = "<INSERT YOUR CONNECTION STRING HERE>"
        self.table_names = {
            "UserRequests": "AutoScraperUserRequestsTable",
            "Parameters": "AutoScraperParametersTable",
            "Destinations": "AutoScraperDestinationsTable",
            "Services": "AutoScraperServicesTable"
        }
        self.maya_vars = [
            "service_type",
            "eng_report",
            "heb_report",
            "start_date",
            "end_date",
            "inner_format"
        ]
        self.pdf_vars = [
            "data_type",
            "from_text",
            "to_text",
            "_file"
        ]
        self.request_status = [
            'pending',
            'created',
            'update',
            'disabled'
        ]
        self.service_by_code = {
            "1": "RAW",
            "2": "MAYA",
            "3": "API",
            "4": "QUERIES",
            "5": "PDF",
        }

    def get_default_entities(self, table_key) -> list:
        """
            Returns a list of default entities (for Services and Destinations)
        """
        if table_key == "Services":
            service_entity_1 = {"PartitionKey": "ServicesTable", "RowKey": "1", "serviceID": "1", "scriptName": "script_raw_service", "serviceLink": "https://boirndextautoscrapper.azurewebsites.net/post_autoscraper", "serviceName": "raw", "scriptPath": "raw_path"}
            service_entity_2 = {"PartitionKey": "ServicesTable", "RowKey": "2", "serviceID": "2", "scriptName": "script_maya_service", "serviceLink": "http://boirndextautoscrapper.azurewebsites.net/get_maya", "serviceName": "maya", "scriptPath": "maya_path"}
            service_entity_3 = {"PartitionKey": "ServicesTable", "RowKey": "3", "serviceID": "3", "scriptName": "script_api_service", "serviceLink": "http://boirndextautoscrapper.azurewebsites.net/post_file", "serviceName": "api", "scriptPath": "api_path"}
            service_entity_4 = {"PartitionKey": "ServicesTable", "RowKey": "4", "serviceID": "4", "scriptName": "script_queries_service", "serviceLink": "http://boirndextautoscrapper.azurewebsites.net/post_queries", "serviceName": "queries", "scriptPath": "queries_path"}
            service_entity_5 = {"PartitionKey": "ServicesTable", "RowKey": "5", "serviceID": "5", "scriptName": "script_pdf_service", "serviceLink": "http://boirndextautoscrapper.azurewebsites.net/post_pdf_file", "serviceName": "pdf", "scriptPath": "pdf_path"}
            return [service_entity_1, service_entity_2, service_entity_3, service_entity_4, service_entity_5]
        elif table_key == "Destinations":
            destination_entity_1 = {"PartitionKey": "DestinationsTable", "RowKey": "1", "DestinationID": "1", "name": "cloud", "path": "cloud_path"}
            destination_entity_2 = {"PartitionKey": "DestinationsTable", "RowKey": "2", "DestinationID": "2", "name": "boi", "path": "boi_safe_path"}
            return [destination_entity_1, destination_entity_2]

    def create_table(self, table_key) -> str:
        """
            Creating a table based on the table key and self connection string
        """
        with TableClient.from_connection_string(self.connection_string, table_name=self.table_names[table_key]) as table_creation:
            if table_key == "Destinations" or table_key == "Services":
                while True:
                    try:
                        # Create a table
                        table_creation.create_table()
                    except HttpResponseError as e:
                        error_type = e.args[0].split('\n')[-1].split(':')[-1]
                        if error_type == "TableAlreadyExists":
                            # print(error_type)
                            break
                    except Exception as e:
                        print("Diff Exception: \n\t\t", str(type(e).__name__), '\n',str(e.args))
                        break
                entity_lst = self.get_default_entities(table_key)
                try:
                    for _entity_ in entity_lst:
                        self.create_entity(_entity=_entity_, table_name=self.table_names[table_key])
                except Exception as e: # This entities already exists there
                    print("EXCEPTION:\t", str(e))
                    pass
            else:
                while True:
                    try:
                        # Create a table
                        table_creation.create_table()
                    except HttpResponseError as e:
                        error_type = e.args[0].split('\n')[-1].split(':')[-1]
                        if error_type == "TableAlreadyExists":
                            # print(error_type)
                            break
                    except:
                        return "Exception In Creating Table"
        return "Success"

    def create_tables(self) -> list:
        """
            Creating all the tables based on the table names in self and it's connection string
        """
        statuses = []
        for _key_ in self.table_names.keys():
            status = self.create_table(table_key=_key_)
            statuses.append((status, _key_))
        return statuses

    def delete_table(self, _name_) -> None:
        """
            Deleting a specific table
        """
        with TableClient.from_connection_string(self.connection_string, table_name=_name_) as table_deletion:
            # Delete a table
                table_deletion.delete_table()

    def delete_tables(self, print_flag: bool = False) -> bool:
        """
            Deleting all the tables
        """
        try:
            for _key_ in self.table_names:
                self.delete_table(self.table_names[_key_])
                if print_flag:
                    print(f"Table {self.table_names[_key_]} got deleted!")
            return True
        except:
            return False

    def restart_tables(self) -> bool:
        """
            Getting the tables to a starting default version by deleting them all and recreating them as empty
        """
        try:
            self.delete_tables()
            while True:
                try:
                    self.create_tables()
                    break
                except:
                    sleep(0.25)
            return True
        except Exception as e:
            return False

    def check_keys(self, _dict: dict) -> bool:
        """
            Validates the given dictionary for the PartitionKey and RowKey
            -> Will raise a ValueError if any of them are not there
        """
        if any(x not in _dict for x in ('PartitionKey', 'RowKey')): # The Best 'if' Statement EVER!
            raise ValueError("Please supply both 'PartitionKey' and 'RowKey' in order to create a new entity. . .")

    def create_entity(self, _entity: dict, table_name: str) -> None:
        """
            Creating a new entity in the table defined by the inner self table_name
            :param _entity: A dictionary that have a 2 keys that are a must:
                :attr partitionKey: A partition key for the azure tables
                :attr rowKey: A row key for the azure tables
              both attributes helps with the azure table queries
              -> if any of them are not specified it will raise a ValueError
        """
        self.check_keys(_entity)
        try:
            with TableClient.from_connection_string(self.connection_string, table_name=table_name) as table_create_entity:
                table_create_entity.create_entity(entity=_entity)
        except HttpResponseError as he: # Entity already exists
            # print(str(he))
            pass

    def delete_entity(self, table_name: str, entity_partition_key: str, entity_row_key: str, disable_flag: bool = False, termination_flag: bool = False) -> str:
        """
            Deleting a desired entity using it's partitionKey and rowKey properties
        """
        if disable_flag and not termination_flag:
            _entity_ = self.get_entity(table_name=table_name, partition_key=entity_partition_key, row_key=entity_row_key)
            _entity_['status'] = self.request_status[-1]
            return self.update_entity(table_name=table_name, _entity=_entity_, creation_flag=False)
        try:
            with TableClient.from_connection_string(self.connection_string, table_name=self.table_names[table_name]) as table_entity_deletion:
                # Delete an entity
                table_entity_deletion.delete_entity(partition_key=entity_partition_key, row_key=entity_row_key)
            return "Success!"
        except Exception as e:
            return f"ERROR: \n\t {str(e)}"

    def update_entity(self, table_name: str, _entity: dict, creation_flag: bool = True) -> dict:
        """
            Updating an entity, if the creation_flag is supplied it will create it as well (in case it's not in the table)
            :param _entity: A dictionary that have a 2 keys that are a must:
                :attr partitionKey: A partition key for the azure tables
                :attr rowKey: A row key for the azure tables
              both attributes helps with the azure table queries
              -> if any of them are not specified it will raise a ValueError
        """
        self.check_keys(_entity)
        with TableClient.from_connection_string(self.connection_string, table_name=self.table_names[table_name]) as table_update_entity:
            if creation_flag:
                return table_update_entity.upsert_entity(_entity)
            else:
                return table_update_entity.update_entity(_entity)

    def get_all_entities(self, table_name: str, print_flag: bool = False) -> list:
        """
            Query for an entity without partition and row keys
            Returns a list of all the entities
            - If provided the 'print_flag' it will print the entities as well
        """
        entities_lst = []
        with TableClient.from_connection_string(self.connection_string, table_name=table_name) as table_entities:
            # List all of the entities without requiring a partitionKey or rowKey
            entities_lst_tmp = list(table_entities.list_entities())
            for i, lst in enumerate(entities_lst_tmp):
                entities_lst.append(dict(lst))
        if print_flag:
            for item in entities_lst:
                print(item)
        return entities_lst

    def get_next_key(self, table_name: str, key_name: str) -> str:
        """
            Returns the next PartitionKey or RowKey that should be applied in this table
        """
        row_keys = [0]
        row_keys = [int(row_key) for row_key in [row[key_name] for row in self.get_all_entities(table_name=table_name)]]
        row_keys.insert(0, 0)
        max_row = max(row_keys) + 1
        if str(max_row) == '0':
            return '0'
        return str(max_row)

    def get_all_entitis_by_column_value(self, table_name: str, column_name: str, column_values: list) -> list:
        """
            Returns a list of all the entities with the values specified in the column specified
        """
        all_entities = self.get_all_entities(table_name=table_name, print_flag=False)
        filtered_entities = []
        for col_val in column_values:
            for entity in all_entities:
                if str(entity[column_name]) == str(col_val): # The Magic Condition!
                    filtered_entities.append(entity)
        return filtered_entities

    def get_entity(self, table_name: str, partition_key: str, row_key: str) -> dict:
        """
            Returns an entity that match the PartitionKey and RowKey provided
        """
        entities = self.get_all_entities(table_name=self.table_names[table_name])
        entity = {}
        for _entity in entities:
            if _entity['PartitionKey'] == partition_key and _entity['RowKey'] == row_key:
                entity = _entity
                break
        return entity

    def get_param_order(self, param_name: str) -> int:
        """
            Returns the order number of a given parameter
        """
        # Maya Related
        if param_name == self.maya_vars[0]:
            return 1
        elif param_name == self.maya_vars[1]:
            return 2
        elif param_name == self.maya_vars[2]:
            return 3
        elif param_name == self.maya_vars[3]:
            return 4
        elif param_name == self.maya_vars[4]:
            return 5
        elif param_name == self.maya_vars[5]:
            return 6
        # PDF Related
        if param_name == self.pdf_vars[0]:
            return 1
        elif param_name == self.pdf_vars[1]:
            return 2
        elif param_name == self.pdf_vars[2]:
            return 3
        elif param_name == self.pdf_vars[3]:
            return 4
        # Default
        return 0

    def createUserRequestEntity(self, user_data: dict):
        """
            Constructs and returns an entity for the UserRequests table
        """
        PartitionKey = self.get_next_key(table_name=self.table_names["UserRequests"], key_name="PartitionKey")
        RowKey = self.get_next_key(table_name=self.table_names["UserRequests"], key_name="RowKey")
        all_services = self.get_all_entities(table_name=self.table_names["Services"])
        service_name = next(item for item in all_services if item["serviceID"] == user_data["serviceID"])["serviceName"]
        DAG_Name = f"DAG_{service_name}_{PartitionKey}_{RowKey}"
        return {
            "PartitionKey": PartitionKey,
            "RowKey": RowKey,
            "DestinationID": user_data["DestinationID"],
            "DAG_Name": DAG_Name,
            "cron": user_data["cron"],
            "end_date": user_data["end_date"],
            "start_date": user_data["start_date"],
            "serviceID": user_data["serviceID"],
            "description": user_data["description"],
            "user": user_data["user"],
            "output_name": user_data["output_name"],
            "status": user_data['status'],
        }

    def createParametersEntity(self, user_data: dict, parameter_name: str, user_reqs_row_key: str) -> dict:
        """
            Constructs and returns an entity for the Parameters table
        """
        PartitionKey = self.get_next_key(table_name=self.table_names["Parameters"], key_name="PartitionKey")
        RowKey = self.get_next_key(table_name=self.table_names["Parameters"], key_name="RowKey")
        param_value = json.dumps(user_data["parameters"][parameter_name], ensure_ascii=False)
        return {
            "PartitionKey": PartitionKey,
            "RowKey": RowKey,
            "serviceID": user_data["serviceID"],
            "parameterValue": param_value,
            "parameterName": parameter_name,
            "parameterOrder": self.get_param_order(param_name=parameter_name),
            "UserReqsRowKey": user_reqs_row_key
        }

    def update_datalake_storage_with_request(self, request_data: dict):
        """
            >>> Main Function For The GUI <<<<
            Goal:
                Accepting a request from the user and constructing the suitable entities for the tables (UserRequests, Parameters) 
                and updating the tables accordingly.
            Parameters:
                :param request_data: A Dictionary holding all of the data regarding the request as follows:
                    - DestinationID
                    - cron
                    - end_date
                    - start_date
                    - serviceID
                    - description
                    - user
                    - output_name
                    - parameters
                    - status
                >>> For datails about the parameters please refer to the models.py file
        """
        try:
            self.create_tables()
        except Exception as e:
            error_type = e.args[0].split('\n')[-1].split(':')[-1]
            if error_type != "TableAlreadyExists":
                # Need to send us an alert about this exception some how
                return -1
        params = list(request_data["parameters"].keys())
        num_of_params = len(params)
        if request_data['serviceID'] == "2":
            if num_of_params != len(self.maya_vars):
                return -17
        userRequestEntity = self.createUserRequestEntity(user_data=request_data)
        self.create_entity(_entity=userRequestEntity, table_name=self.table_names['UserRequests'])
        for i in range(num_of_params):
            parametersEntity = self.createParametersEntity(user_data=request_data, parameter_name=params[i], user_reqs_row_key=userRequestEntity["RowKey"])
            self.create_entity(_entity=parametersEntity, table_name=self.table_names['Parameters'])
        return "Success!"

    def get_json_encoded_parameters(self, partition_key: str, row_key: str) -> str:
        req_entity = self.get_entity(table_name="UserRequests", partition_key=partition_key, row_key=row_key)
        service_id_ = req_entity["serviceID"]
        param_entities = self.get_all_entities(table_name=self.table_names["Parameters"])
        req_param_entities = {} # I AM GROOT!
        for entity in param_entities:
            if entity["serviceID"] == service_id_ and entity["UserReqsRowKey"] == row_key:
                req_param_entities[entity["parameterName"]] = entity["parameterValue"]
        req_param_entities = base64.b64encode(str(json.dumps(req_param_entities)).encode("utf-8")).decode("ascii")
        return req_param_entities
