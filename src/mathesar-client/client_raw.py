from typing import Optional
from requests import post
from os import environ
from urllib.parse import urljoin
from random import randint


class MathesarClientError(Exception):
    pass


class MathesarClientRaw:
    def __init__(self, base_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        self.__base_url = base_url or environ['MATHESAR_BASE_URL']
        self.__username = username or environ['MATHESAR_USERNAME']
        self.__password = password or environ['MATHESAR_PASSWORD']
        self.__api_url = urljoin(self.__base_url, "api/rpc/v0/")

    def records_list(self, database_id: int, table_id: int):
        data = {
            "database_id": database_id,
            "table_oid": table_id
        }
        return self._post("records.list", data)


    def _post(self, method, data):
        response = post(
            self.__api_url,
            json={
                "id": randint(1, 1000),
                "jsonrpc": "2.0",
                "method": method,
                "params": data
            },
            auth=(self.__username, self.__password)
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise MathesarClientError(data["error"])

        return data["result"]


if __name__ == "__main__":
    def _test():
        client = MathesarClientRaw()
        print(client.records_list(database_id=2, table_id=18087))

    _test()
