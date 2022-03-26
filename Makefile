IMAGE_NAME = alex925/knowledge-base-generator:latest

build-img:
	docker build -t ${IMAGE_NAME} --build-arg MODE=prod .

push-img:
	docker push ${IMAGE_NAME}


generate-local-knowledge-base:
	MODE=dev python3 ./generator.py

generate-web-knowledge-base:
	MODE=prod python3 ./generator.py

manual-update-knowledge-base:
	bash tools/local_update_knowledge_base.sh
