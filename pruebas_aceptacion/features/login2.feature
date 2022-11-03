Característica: Login del sistema
    Como usuario del sistema
    Quiero entrar al sistema para realizar mis actividaes
    Para tener control de la correspondencia
    

        Escenario: Credenciales válidas
            Dado que ingreso al sistema en el dominio "http://localhost:8000/"
              Y escribo mi usuario "admin" y contraseña "admin123"
             Cuando presiono el botón Ingresar
             Entonces puedo ver la leyenda "Fichas de control y seguimiento de correspondencias" en la pagina principal

        Escenario: Credenciales invalida
            Dado que ingreso al sistema en el dominio "http://localhost:8000/"
              Y escribo mi usuario "admin" y contraseña "admin"
             Cuando presiono el botón Ingresar
             Entonces puedo ver el mensaje "Error:"

       