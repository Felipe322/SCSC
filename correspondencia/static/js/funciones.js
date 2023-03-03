function eliminaFichaModal(url, num_documento){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar la ficha (${num_documento})?`;
}

function eliminaAreaModal(url, nombre, siglas){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar a ${nombre} (${siglas})?`;
}

function eliminaDependenciaModal(url, nombre, siglas){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar la dependencia ${nombre} (${siglas})?`;
}

// function eliminaUsuarioModal(url, correo, username){
//     document.getElementById('formEliminar').action = url;
//     document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar el usuario ${correo} (${username})?`;
// }

// function muestraFiltro() {
//     var x = document.getElementById("filtro");
//     if (x.style.display === "none") {
//         x.style.display = "block";
//     } else {
//         x.style.display = "none";
//     }
// }