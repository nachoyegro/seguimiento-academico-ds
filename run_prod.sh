#!/usr/bin/env bash

echo Matando procesos viejos
docker-compose rm -fs

echo Creando containers nuevos
docker-compose -f docker-compose.prod.yml up --build -d
