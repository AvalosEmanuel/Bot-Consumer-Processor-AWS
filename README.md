# Bot-Consumer - Processor.. AWS

**La funcionalidad de este bot se basa en integra una serie de servicios AWS, la tarea consiste en *"consumir"* información de un 'Topic', luego *"procesarla"*, obteniendo los valores de interés, en este caso en particular precisiones sobre transacciones realizadas, para finalmente *"almacenar"* estos datos para su futuro análisis y completar de esta forma el circuito propuesto.**

Servicios AWS que se integran en el proceso:
1. **'Simple Notification Service' (SNS)** Proporciona la infraestructura para la entrega masiva de mensajes, brindando además la posibilidad de *"suscribirse"* solo a datos de interés para el proyecto en particular. Esto sucede a través de otro servicio que se acopla a continuación.
2. **'Simple Queue Service' (SQS)** es un servicio de cola de mensajes, lo cual nos permite disponer de la información a medida que se va recibiendo y procesarla. Posterior a esta etapa y para completar el circuito entra en escena un tercer servicio.
3. **'Simple Storage Service' (S3)** proporciona almacenamiento de objetos a través de una interfaz de servicio web, en este caso en paticular lo empleamos para almacenar toda la información procesada y tener de esta forma un registro de la misma para su análisis.
 
El lenguaje de codificación es **'Python'** y todo el proceso se encuentra corriendo dentro de un **'Docker'** containers para brindar una capa de abstracción, siguiendo con el modelo de micro-servicio.
