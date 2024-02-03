.PHONY: down build run prod drop_db auto_backup backup restore prune frontend_build frontend_export

BACKUP_COMMAND := "0 0 * * * cd \"$(PWD)\" && python3 scripts/backup.py"

prod: down build

down:
	docker compose down

build:
	docker compose up -d --build

run: down 
	docker compose up postgres redis -d
	chmod +x scripts/wait-for-it.sh
	scripts/wait-for-it.sh localhost:5432 -- echo "PostgreSQL is up"
	scripts/wait-for-it.sh localhost:6379 -- echo "Redis is up"
	alembic upgrade head
	uvicorn src.main:app --reload
	
start:
	uvicorn vercel:app --reload

open-redis:
	docker exec -it fastapi-redis redis-cli

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf

auto_backup:
	@if crontab -l ; then \
		crontab -l > mycron ; \
	else \
		touch mycron ; \
	fi
	@echo $(BACKUP_COMMAND) >> mycron
	@crontab mycron
	@rm mycron
	@echo "Backup script added to cron"

backup:
	python3 scripts/backup.py
	@echo "Backup complete"
	
stop_backup:
	crontab -l | grep -v -F $(BACKUP_COMMAND) | crontab -

restore:
	python3 scripts/restore.py

frontend_build:
	if [ -d dist.tar.xz ]; then \
		sudo rm -rf dist.tar.xz; \
	fi
	tar -cJvf dist.tar.xz dist

frontend_export:
	if [ -d /var/www/school/dist ]; then \
		sudo rm -rf /var/www/school/dist; \
	fi
	sudo mkdir -p /var/www/school/
	sudo tar -xJvf dist.tar.xz -C /var/www/school/


drop_db: down
	if docker volume ls -q | grep -q $$(basename "$$(pwd)")_postgres_data; then \
		docker volume rm $$(basename "$$(pwd)")_postgres_data; \
		echo "successfully drop_db command";\
	fi
	sudo rm -rf ./static/media

prune: down
	docker system prune -a
	docker volume prune -a