#!/bin/bash

direccion=$1
username=$2
email=$3
tiempo=$4
# tiempo = 1 --> diariamente - 1 dia
# tiempo = 7 --> semanalmente - 7 dias
# tiempo = 30 --> mensualmente - 30 dias

#usamos crontab -l para listar las tareas pendientes y redireccionamos a un archivo
crontab -l > $direccion/notificaciones/fic-tareas

if [ $tiempo -eq 1 ]
then
	# introducimos la tarea que queremos planificar en el archivo generado en el paso anterior
	echo "@daily sh $direccion/notificaciones/enviar.sh $direccion $username $tiempo | mail -s "Eventos" $email" >>$direccion/notificaciones/fic-tareas
elif [ $tiempo -eq 7 ]
then
	# introducimos la tarea que queremos planificar en el archivo generado en el paso anterior
	echo "@weekly sh $direccion/notificaciones/enviar.sh $direccion $username $tiempo | mail -s "Eventos" $email" >>$direccion/notificaciones/fic-tareas

else
	# introducimos la tarea que queremos planificar en el archivo generado en el paso anterior
	echo "@monthly sh $direccion/notificaciones/enviar.sh $direccion $username $tiempo | mail -s "Eventos" $email" >>$direccion/notificaciones/fic-tareas
fi

#instala las tareas del fichero en cron
crontab $direccion/notificaciones/fic-tareas
