select split_part(evento,'+',6)
from gestor_historial_notificacion
where usuario = :usuario and fecha_hora::date >= (current_date - integer :tiempo);

