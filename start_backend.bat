@echo off
echo [INFO] Zupyniaiu stari konteinery ta vydaliaiu smittia...
docker-compose down -v

echo [INFO] Zbyraiu ta zapuskaiu backend, bazu ta redis...
docker-compose up --build -d

echo [INFO] Gotovo! API krutitsia na http://localhost:8000
echo [INFO] Mozhesh kodyty svoyu Unity.
pause