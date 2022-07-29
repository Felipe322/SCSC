function eliminaAreaModal(url, nombre, siglas){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar el area ${nombre} (${siglas})?`;
}