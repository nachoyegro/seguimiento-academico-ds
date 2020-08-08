# Sistema de Seguimiento Académico - Estadísticas
[![Build Status](https://travis-ci.org/nachoyegro/seguimiento-academico-ds.svg?branch=master)](https://travis-ci.org/nachoyegro/seguimiento-academico-ds)
[![codecov](https://codecov.io/gh/nachoyegro/seguimiento-academico-ds/branch/master/graph/badge.svg)](https://codecov.io/gh/nachoyegro/seguimiento-academico-ds)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)


## Resumen

El objetivo principal de este módulo es de la obtención de los datos mediante una API Rest, la manipulación y el procesamiento de esos datos. Una vez terminado este proceso, sirve los resultados mediante una API Rest, que es consumida por un tercero para su visualización.


## Tecnologías usadas

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

### Desarrollo

En el modo desarrollo, la aplicación corre gracias al Web Server de Flask, el cual no está optimizado para producción.

```
  $ docker-compose -f docker-compose.dev.yml up --build -d
```


### Producción

El deploy para producción tiene algunos aspectos extra, como correr la aplicación con Gunicorn y Nginx para resolver los requests.

```
  $ docker-compose -f docker-compose.prod.yml up --build -d
```