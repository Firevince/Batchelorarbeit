import os

from dotenv import load_dotenv
from milvus import MilvusServer, debug_server, default_server
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    db,
    utility,
)

load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH")
DATA_PATH = os.getenv("DATA_PATH")


def run_milvius():
    debug_server.run()


def set_settings():
    with default_server:
        default_server.set_base_dir(os.path.join(DATA_PATH, "milvius"))
        default_server.config.set("system_Log_level", "info")
        default_server.config.set("proxy_port", 19531)
        default_server.config.set("dataCoord.segment.maxSize", 1024)


def test_server():
    default_server.start()
    connections.connect(host="127.0.0.1", port=default_server.listen_port)
    print(utility.get_server_version())
    default_server.stop()


def connect_db():
    conn = connections.connect(host="127.0.0.1", port=19530, db_name="default")


def create_db():
    conn = connections.connect(host="127.0.0.1", port=19530, db_name="default")

    database = db.create_database("embeddings")


def create_collection():

    sentence_id = FieldSchema(
        name="sentence_id",
        dtype=DataType.INT64,
        is_primary=True,
    )
    filename = FieldSchema(
        name="filename",
        dtype=DataType.VARCHAR,
        max_length=200,
        # The default value will be used if this field is left empty during data inserts or upserts.
        # The data type of `default_value` must be the same as that specified in `dtype`.
        default_value="Unknown",
    )
    sentence_text = FieldSchema(
        name="sentence_text",
        dtype=DataType.VARCHAR,
        max_length=200,
        # The default value will be used if this field is left empty during data inserts or upserts.
        # The data type of `default_value` must be the same as that specified in `dtype`.
        default_value="Unknown",
    )
    sentence_tf_idf_embed = FieldSchema(
        name="sentence_tf_idf_embed",
        dtype=DataType.FLOAT_VECTOR,
        dim=2,
        # The default value will be used if this field is left empty during data inserts or upserts.
        # The data type of `default_value` must be the same as that specified in `dtype`.
        default_value=9999,
    )
    schema = CollectionSchema(
        fields=[filename, sentence_id, sentence_text, sentence_tf_idf_embed],
        description="Test book search",
        enable_dynamic_field=True,
    )
    collection_name = "sentence_embeddings_tf_idf"
    collection = Collection(name=collection_name, schema=schema, using="default", shards_num=2)
    return collection


# set_settings()
# test_server()
