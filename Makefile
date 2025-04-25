build-docker:
	docker build -t bangquoc9/n8n:latest -f Dockerfile.n8n .

init:
# Execute build-ngrok target
	./scripts/build-ngrok.sh

run-dev:
# Get the public URL
	$(eval ngrok_url := $(shell ./scripts/get-ngrok-url.sh))
	@echo "Ngrok started successfully. Public URL: $(ngrok_url)"

# Start Docker Compose
	docker-compose -f docker-compose.yaml down && N8N_PUBLIC_API_URL=$(ngrok_url) docker-compose -f docker-compose.yaml up -d

reload-cookies:
# down and up downloader service
	docker-compose -f docker-compose.yaml down downloader && docker-compose -f docker-compose.yaml up --build -d downloader
	@echo "Reload cookies successfully"