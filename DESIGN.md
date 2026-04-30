## DeliveryReport Class

Se implementó como una `dataclass` porque su propósito principal es representar
los resultados del envío de notificaciones, almacenando datos y proporcionando
métodos simples derivados como la tasa de éxito.

### Atributos
- channel: canal utilizado (email, SMS, etc.)
- attempted: número de mensajes intentados
- delivered: número de mensajes entregados
- delivered_messages: lista de mensajes entregados

### Métodos
- success_rate(): calcula la tasa de éxito
- failed(): número de mensajes fallidos