up-build:
	docker-compose up --build

up:
	docker-compose up

up-s:
	docker-compose up memory_db_redis tool_runtime_docker vector_db_chroma

dev:
	./venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 9000 --host 0.0.0.0