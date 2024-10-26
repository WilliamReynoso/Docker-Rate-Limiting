# Rate Limiting y Control de Tráfico y Acceso a endpoints

Este proyecto de Docker crea una base de datos con informacion falsa en PostgreSQL a la cual se accede mediante endpoints que configuramos usando flask, posteriormente se instalo Flask-Limiter.
Se configurar límites de tasa globales (por ejemplo, limitar las peticiones a 10 por hora/dia o minuto). Se aplicaron límites de tasa a rutas específicas (por ejemplo, limitar el acceso al login o consulta o rutas de borrado de informacion o creacion de nuevos campos en la BD). Asi como la implementacion de lógica para manejar usuarios bloqueados temporalmente por exceder el límite de peticiones.

docker-compose.yml:
(Se agregaron variables de entorno siguiendo buenas practicas para entornos de produccion)

![imagen](https://github.com/user-attachments/assets/9210b35b-1e3b-4f89-9ff3-38a3310d446d)

![imagen](https://github.com/user-attachments/assets/c72f036c-219d-48fd-9c4a-12fd85048cfa)

en el script main.py se agrego la configuracion de flask limiter
![imagen](https://github.com/user-attachments/assets/ab01c937-2fb6-4570-97ba-bcedc4729f9c)

asi como el uso de variables de entorno y los limites por ruta
![imagen](https://github.com/user-attachments/assets/6fa7884c-8eac-42b7-abbc-2e57f8cbf52c)

y el manejo de usuarios bloqueados por exceder el limite
![imagen](https://github.com/user-attachments/assets/7b86dadb-2f26-42d9-acbe-76761990c5e1)


## Resultados:
si realizamos mas de 2 solicitudes a localhost/usuarios recibiremos el mensaje de que hemos alcanzo el limite de solicitudes
hacemos 1 solicitud simplemente entrando a la pagina:
![imagen](https://github.com/user-attachments/assets/9a5b8404-0234-4934-9308-6dde69a6ab73)

luego refrescamos la pagina:
![imagen](https://github.com/user-attachments/assets/a19a7334-5c6f-46de-af43-c00cb20ff781)

refrescamos otra vez y pum hemos sido bloqueados (por 1 minuto en este caso):
![imagen](https://github.com/user-attachments/assets/417546db-c598-4029-a7d0-5b87bc117545)

Resultados en consola:
*Podemos observar que GET /usuarios se recibe 2 veces correctamente y a la 3era ya obtenemos el error 429*
![imagen](https://github.com/user-attachments/assets/6dd8f85a-e678-4ad7-b263-237c6d986da7)


### Se repite lo mismo dependiendo del endpoint y los limites de este, en caso de que el endpoint no tenga un limite especifico, se aplicara el limite global de 10 peticiones por hora que establecimos.
![imagen](https://github.com/user-attachments/assets/5b09158e-7c67-40c6-89fe-84d68d7f365d)
