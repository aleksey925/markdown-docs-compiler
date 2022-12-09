build_img:
	docker build -t knowledge-base-generator:latest .

lint:
	pre-commit run --all
