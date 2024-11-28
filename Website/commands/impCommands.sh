#awsicons
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
#llm
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
#generateawstemplate
uvicorn app:app --host 0.0.0.0 --port 8002 --reload

docker buildx create --use

docker buildx build --platform linux/amd64,linux/arm64 -t capthestone/frontend:latest --push .
docker buildx build --platform linux/amd64,linux/arm64 -t capthestone/website-awsicons:latest --push .
docker buildx build --platform linux/amd64,linux/arm64 -t capthestone/website-awsicons:latest --push .