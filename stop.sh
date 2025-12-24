cd auth_service
docker compose down
echo "Auth service stopped."
cd ../wallet_service
docker compose down
echo "Wallet service stopped."
cd ../orchestrator_service
docker compose down
echo "Orchestrator service stopped."

docker network rm microservices_network
echo "microservices_network removed."
echo "All services have been stopped and network removed."
