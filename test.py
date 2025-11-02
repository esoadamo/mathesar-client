from src.mathesar_client.client_raw import MathesarClientRaw


if __name__ == "__main__":
    def _test():
        client = MathesarClientRaw()
        print(client.records_list(database_id=2, table_id=18087))

    _test()
