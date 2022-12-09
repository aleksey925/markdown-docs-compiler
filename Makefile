build_img:
	docker build -t ghcr.io/aleksey925/markdown-docs-compiler:latest .

lint:
	pre-commit run --all
