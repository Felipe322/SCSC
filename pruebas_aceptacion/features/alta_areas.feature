Característica: Agregar una area
    Como usuario del sistema
    Quiero entrar al sistema para realizar mis actividaes en areas
    Para tener control de las áreas que hay.

    Escenario: Agregar la primera area
    Dado que ingreso al sistema en el dominio "http://localhost:8000/"
    Y escribo mi usuario "admin" y contraseña "admin"
    Cuando presiono el boton ingresar
    Y seleciono la pestaña "Administración de areas"
    Y seleciono la opcion "Agregar area"
    Cuando ingreso el nombre de un area "Escuela Secundaria" y sus siglas "ESC.188"
    Cuando selecciono el boton "Agregar"