from abc import ABC, abstractmethod
from dataclasses import dataclass
import random
import string
from typing import Any
import pickle
import json
import xmltodict
from struct_pb2 import RootedStruct
from avro_schema import AVRO_SCHEMA
from google.protobuf.json_format import ParseDict, MessageToDict
from avro.io import BinaryEncoder, BinaryDecoder, DatumReader, DatumWriter
from io import BytesIO
import yaml
import msgpack


RANDOM_SEED = 100


@dataclass
class Struct:
    string_field: str
    array_field: list
    dictionary_field: dict
    integer_field: int
    float_field: float

    @classmethod
    def create_small(cls) -> "Struct":
        random.seed(RANDOM_SEED)
        string_field = cls.generate_random_string(10)
        array_field = cls.generate_random_array(10)
        dictionary_field = cls.generate_random_dictionary(10)
        integer_field = random.randint(0, 1000)
        float_field = random.uniform(0, 1000)
        return cls(string_field, array_field, dictionary_field, integer_field, float_field)

    @classmethod
    def create_big(cls) -> "Struct":
        random.seed(RANDOM_SEED)
        string_field = cls.generate_random_string(100)
        array_field = cls.generate_random_array(100)
        dictionary_field = cls.generate_random_dictionary(100)
        integer_field = random.randint(0, 1000000)
        float_field = random.uniform(0, 1000000)
        return cls(string_field, array_field, dictionary_field, integer_field, float_field)

    @staticmethod
    def generate_random_string(string_length: int) -> str:
        return "".join(random.choices(string.ascii_letters, k=string_length))

    @classmethod
    def generate_random_array(cls, array_length: int) -> list[str]:
        return [cls.generate_random_string(10) for _ in range(array_length)]

    @classmethod
    def generate_random_dictionary(cls, dictionary_length: int) -> dict[str, str]:
        return {cls.generate_random_string(10): cls.generate_random_string(10) for _ in range(dictionary_length)}

    def as_dict(self):
        return {"root": self.__dict__}


class BaseSerializer(ABC):
    def __init__(self, struct: dict, *args, **kwargs):
        self.struct = struct
        self.serialized_struct = self.serialize()

    @abstractmethod
    def serialize(self) -> Any:
        pass

    @abstractmethod
    def deserialize(self) -> dict:
        pass


class NATIVESerializer(BaseSerializer):
    def serialize(self) -> bytes:
        return pickle.dumps(self.struct)

    def deserialize(self) -> dict:
        return pickle.loads(self.serialized_struct)


class JSONSerializer(BaseSerializer):
    def serialize(self) -> str:
        return json.dumps(self.struct)

    def deserialize(self) -> dict:
        return json.loads(self.serialized_struct)


class XMLSerializer(BaseSerializer):
    def serialize(self) -> str:
        return xmltodict.unparse(self.struct)

    def deserialize(self) -> dict:
        return xmltodict.parse(self.serialized_struct)


class PROTOSerializer(BaseSerializer):
    def __init__(self, struct: dict):
        self.message_to_serialize = ParseDict(struct, RootedStruct())
        super().__init__(struct)
        self.message_to_deserialize = RootedStruct()
        self.message_to_deserialize.ParseFromString(self.serialized_struct)

    def serialize(self) -> str:
        return self.message_to_serialize.SerializeToString()

    def deserialize(self) -> dict:
        return MessageToDict(self.message_to_deserialize)


class AVROSerializer(BaseSerializer):
    def __init__(self, struct: dict):
        self.schema = AVRO_SCHEMA
        super().__init__(struct)

    def serialize(self) -> bytes:
        bytes_io = BytesIO()
        encoder = BinaryEncoder(bytes_io)
        writer = DatumWriter(self.schema)
        writer.write(self.struct, encoder)
        return bytes_io.getvalue()

    def deserialize(self) -> object:
        decoder = BinaryDecoder(BytesIO(self.serialized_struct))
        reader = DatumReader(self.schema)
        return reader.read(decoder)


class YAMLSerializer(BaseSerializer):
    def serialize(self) -> str:
        return yaml.dump(self.struct)

    def deserialize(self) -> dict:
        return yaml.load(self.serialized_struct, yaml.Loader)


class MSGPACKSerializer(BaseSerializer):
    def serialize(self) -> bytes:
        return msgpack.packb(self.struct)

    def deserialize(self) -> dict:
        return msgpack.unpackb(self.serialized_struct)
