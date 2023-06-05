docker build -t pedalboard-backend -f ./dockerfiles/backend.dockerfile .
docker tag pedalboard-backend c1204545/pedalboard-backend:latest
docker push c1204545/pedalboard-backend:latest

docker build -t pedalboard-frontend -f ./dockerfiles/frontend.dockerfile .
docker tag pedalboard-frontend c1204545/pedalboard-frontend:latest
docker push c1204545/pedalboard-frontend:latest