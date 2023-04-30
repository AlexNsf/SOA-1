import avro.schema


AVRO_SCHEMA = avro.schema.parse('''
    {
        "namespace": "struct.avro",
        "type": "record",
        "name": "RootedStruct",
        "fields": [
            {"name": "root", "type":
            {"type": "record", "name": "Struct", "fields": [
                {"name": "string_field", "type": "string"},
                {"name": "array_field", "type": {
                    "type": "array", "items":
                    [{
                        "name": "array_item", "type": "string"
                    }]
                    }
                },
                {
                    "name": "dictionary_field",
                    "type": {
                        "type": "map",
                        "values": "string"
                    }
                },
                {"name": "integer_field", "type": "int"},
                {"name": "float_field", "type": "float"}
            ]
        }}]
    }''')
