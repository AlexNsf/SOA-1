from serializers import BaseSerializer, Struct
from timeit import timeit


class Tester:
    def __init__(self, serializer_t: type[BaseSerializer]):
        self.type = serializer_t.__name__[:-10]
        self.serializer_t = serializer_t
        self.struct_small = Struct.create_small().as_dict()
        self.struct_big = Struct.create_big().as_dict()
        self.struct = self.struct_small
        self.serializer = serializer_t(self.struct)
        self.serialized_value = self.serializer.serialize()

    def get_serialize_time(self) -> float:
        return timeit(self.serializer.serialize, number=1000) * 1000

    def get_deserialize_time(self) -> float:
        return timeit(self.serializer.deserialize, number=1000) * 1000

    def get_size_in_bytes(self) -> int:
        if isinstance(self.serialized_value, bytes):
            return len(self.serialized_value)
        else:
            return len(self.serialized_value.encode())

    def get_result(self, is_big: int) -> str:
        if is_big and self.struct != self.struct_big:
            self.struct = self.struct_big
            self.serializer = self.serializer_t(self.struct)
            self.serialized_value = self.serializer.serialize()
        elif not is_big and self.struct != self.struct_small:
            self.struct = self.struct_small
            self.serializer = self.serializer_t(self.struct)
            self.serialized_value = self.serializer.serialize()
        return f"{self.type} - {self.get_size_in_bytes()} - " \
               f"{self.get_serialize_time()}ms - {self.get_deserialize_time()}ms\n"
