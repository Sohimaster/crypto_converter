from quote_consumer.services.storage import StorageFactory


def get_quotes_storage():
    return StorageFactory.get_storage()
