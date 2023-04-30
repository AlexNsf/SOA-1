run:
	docker-compose up -d

prepare: down
	docker-compose pull
	docker-compose build

down:
	docker-compose down --remove-orphans

get_result:
	@read -p "Enter format name [NATIVE, JSON, XML, PROTO, AVRO, YAML, MSGPACK] with suffix _0 if you want structure with small data, '_1' if with big : " format_name; \
	echo $$format_name | nc -u localhost 2000