# Sistema de Seguimiento Académico - Estadísticas
[![Build Status](https://travis-ci.com/nachoyegro/seguimiento-academico-ds.svg?branch=master)](https://travis-ci.com/nachoyegro/seguimiento-academico-ds)
[![codecov](https://codecov.io/gh/nachoyegro/seguimiento-academico-ds/branch/master/graph/badge.svg)](https://codecov.io/gh/nachoyegro/seguimiento-academico-ds)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)


## Resumen

El objetivo principal de este módulo es de la obtención de los datos mediante una API Rest, la manipulación y el procesamiento de esos datos. Una vez terminado este proceso, sirve los resultados mediante una API Rest, que es consumida por un tercero para su visualización.


## Instalación con Docker

Docker

Si no se tiene instalado, correr el siguiente comando:

```
  $ apt install docker.io
```

Docker-compose

Si no se tiene instalado, correr el siguiente comando:

```
  $ apt install docker-compose
```

Es necesario crear una red para que todas las instancias puedan comunicarse

```
  $ docker network create seguimiento-academico
```

Una vez que exista la red, se procede a crear y dejar corriendo la imagen de Docker dentro de un contenedor

```
  $ docker-compose -f docker-compose.yml up --build -d
```

## Levantar el proyecto

Por defecto, la aplicación quedará corriendo en http://localhost:5000
