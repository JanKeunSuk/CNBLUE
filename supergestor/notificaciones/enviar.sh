#!/bin/bash

direccion=$1
username=$2
tiempo=$3
export PGPASSWORD='seba2'
echo "Historial de cambios realizados en el Sistema"

psql -h localhost -U seba2 -f $direccion/notificaciones/obtenerReporte.sql prueba5 -v usuario="'$username'" -v tiempo="'$tiempo'"
#| ssmtp katherinevera94@gmail.com

