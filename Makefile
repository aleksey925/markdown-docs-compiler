build_img:
	docker build -t markdown-docs-compiler:latest .

lint:
	pre-commit run --all
