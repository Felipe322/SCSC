function eliminaFichaModal(url, num_documento){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar la ficha (${num_documento})?`;
}

function eliminaAreaModal(url, nombre, siglas){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar el area ${nombre} (${siglas})?`;
}

function eliminaDependenciaModal(url, nombre, siglas){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar la dependencia ${nombre} (${siglas})?`;
}