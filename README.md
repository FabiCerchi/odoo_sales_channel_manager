# Gestión de Canales de Venta y Grupos de Crédito

## Canales de Venta

En la empresa XXXXX se necesita gestionar diferentes canales de venta para poder
controlar las ventas realizadas, así como la entrega de los productos y las facturas
asociadas a dichas ventas. Además de controlar por canal un límite de crédito para sus
clientes, por lo cual cada cliente debe tener asignado un grupo de crédito. Cada vez que
se realice una venta se debe validar que si el cliente pertenece a un grupo de crédito, y que
el monto total de la venta no supere el crédito disponible.

Para cumplir esta necesidad del cliente se de implementar las siguientes funcionales:

### 1. Gestionar Canales de Venta

Gestionar los canales de venta para que se pueda definir un almacén de entrega y un
diario de facturación. A esta funcionalidad se debe acceder desde el menú
“Venta/Configuración/Canales de Venta”. Los datos a registrar son

- **Nombre:** Nombre identificativo del canal (Dato obligatorio).
- **Código:** Secuencia CH000001 que crece con cada cliente ingresado (solo lectura).
- **Depósito:** Almacén de entrada de la mercadería del canal.
- **Diario de Factura:** Punto de venta para la factura asociada a la orden.

El formulario deberá tener un chatter para auditar cambios en el nombre.

### 2. Ordenes de Venta

Para poder controlar la venta por canales se debe modificar las funcionalidades
asociadas a las órdenes de venta de la siguiente forma:
En la orden de venta el usuario debe poder seleccionar el canal de venta y este
canal debe ser un dato obligatorio.

- Cada vez que se realice una venta el usuario debe seleccionar el canal y de acuerdo
al canal seleccionado se debe modificar el almacén de entrega de la
mercadería en la orden de venta, por lo cual las órdenes de entrega generadas
desde la orden de venta deben realizarse del depósito asignado al canal.
- Las facturas emitidas desde la orden de venta deben estar asociadas al diario de
facturación asignado en el canal de la orden de venta
- El canal de venta se debe trasladar a la órdenes de entrega y a la facturas
emitidas de esa orden de venta. Para que el usuario pueda filtrar o agrupar tanto las
órdenes de venta, como órdenes de entrega y factura por canal

### 3. Gestionar Grupos de Crédito

Gestionar en el sistema los grupos de crédito para asociar a diferentes clientes. A esta
funcionalidad se debe acceder desde el menú “Venta/Configuración/Grupos de credito”. Los
datos a registrar son:

- **Nombre:** Nombre identificativo del grupo (Dato obligatorio).
- **Código:** Código identificativo del grupo, no debe repetirse el código en el sistema. El
código puede ser cualquier texto pero con la restricción de que no debe poder
contener la secuencia “026”. Dato obligatorio
- **Canal de Venta:** Relación a los canales de venta (Campo Obligatorio).
- **Crédito Global:** Credito de venta disponible para todo el grupo. Siempre se
define el la moneda de la compañía. Campo obligatorio.
- **Crédito Utilizado:** Crédito consumido a partir de las órdenes de venta ya
confirmadas y facturas realizadas. Campo calculado, donde el valor se obtiene a
partir de la sumatoria del total de ventas confirmadas sin facturar, más el total de
facturas impagas asociadas a los clientes del grupo de crédito. Tener en cuenta que
este valor siempre es en la moneda de la compañía por lo que si las órdenes de
venta o factura se realizan en otra moneda el sistema debe hacer la conversión
- **Crédito Disponible:** Campo calculado donde el valor se calcula restando al
crédito global el crédito utilizado.

### 4. Límite de Crédito

Para cumplir con el requerimiento de límite de crédito se debe modificar las
funcionalidades asociadas a las órdenes de venta de la siguiente forma:

- En el cliente se debe asignar un campo que permita definir si el cliente tiene
control de crédito o no. En caso de que se seleccione que tiene control de crédito se
debe habilitar un campo para que se seleccione los grupos de crédito al cual está
asignado, y donde al menos debe seleccionar un grupo de crédito.
- En la venta debe existir un campo Crédito que tenga los valores (Sin límite de
crédito, Crédito Disponible, Crédito bloqueado), por defecto siempre va a tener
valor “Sin límite de crédito”. Cuando se selecciona un cliente y un canal de venta el
sistema debe buscar si existe un grupo de crédito dónde está asociado el cliente
para ese canal. Si no encuentra ningún grupo el valor del campo seguirá siendo Sin
límite de crédito. Si lo encuentra debe comparar el importe total de la orden de venta
con el crédito disponible del grupo, si el importe total de la venta supera el crédito
disponible el valor del campo debe ser Crédito bloqueado, sino lo supera debe ser
Crédito disponible. Este campo no debe ser editado por el usuario, debe tener color
gris cuando el valor es Sin límite de crédito, verde cuando el valor es Crédito
disponible y rojo cuando el valor es Crédito bloqueado. Debe estar visible en la
vista formulario y en la vista lista.
- No se debe poder confirmar la venta si el valor del campo Crédito es Crédito
bloqueado.

### 5. Reporte de Crédito Utilizado

Se debe implementar un reporte donde se pueda imprimir de un grupo de crédito cuales
son las órdenes de venta y facturas que se tienen en cuenta para calcular el crédito
utilizado. Los campos a mostrar en el reporte serían.

- Nombre del grupo.
- Código del grupo.
- Canal de venta.
- Clientes asociados al grupo. Listado de clientes de los cuales se debe mostrar
nombre, número de documento, teléfono y correo electrónico
- Órdenes de venta que se tienen en cuenta para calcular el crédito utilizado.
Listado de las órdenes de venta donde se debe mostrar el número, la fecha y el
importe total.
- Facturas de venta que se tienen en cuenta para calcular el crédito utilizado.
Listado de las facturas donde se debe mostrar el número, la fecha y el importe
adeudado.

### 6. Endpoint para Crear Grupo de Crédito

Se debe habilitar un endpoint donde se pueda desde una aplicación de tercero crear un
grupo de crédito, al mismo se debe poder enviar un json con el siguiente formato

```json
{
    "grupo_creditos": [
      {
        "name": "Grupo 300 - write",
        "codigo": "03232",
        "canal": "CH000000",
        "credito_global": 1000000
      },
      {
        "name": "Grupo 400 - Create",
        "codigo": "03233",
        "canal": "CH000000",
        "credito_global": 1000000
      }
    ]
  }
```


El sistema debe buscar para cada grupo de crédito del json si existe, la búsqueda la debe
hacer por el código. En caso de que exista debe actualizar los campos nombre, canal y
crédito global. En caso de que no exista lo debe crear. Además debe validar que exista un
canal con ese código sino no existe debe devolver un json con el siguiente formato:


```json
{
    "status": 400,
    "message": "No se encontró el canal CH000000"
}
```

Si después actualizar los grupos el sistema no devuelve ningún error se debe devolver un
json con el siguiente formato

```json
{
    "status": 200,
    "message": "OK"
}
```
