from src.mathesar_client import MathesarClient


if __name__ == "__main__":
    def _test():
        client = MathesarClient()
        print(client.database(database_id=2).table(table_oid=18087).records_list().results)

    _test()
