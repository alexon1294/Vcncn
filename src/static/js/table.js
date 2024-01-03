let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    scrollX: "1300px",
    dom: 'Blfrtip',
    buttons: [
        'colvis',
        {
            extend: 'excelHtml5',
            text: '<i class="fas fa-file-excel"></i>',
            titleAttr: 'Exportar Excel',
            className: 'btn btn-success'
        }
    ],
    lengthMenu: [5, 10, 15, 20, 100, 200],
    columnDefs: [
        { className: "centered", targets: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27] },
        { orderable: false, targets: [1,2,3,4,5,6,7,8,12,13,14,15,16,17,18,19,20,21] },
        { searchable: false, targets: [9,10,11] }
    ],
    pageLength: 10,
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ registros",
        zeroRecords: "Ningún usuario encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
        infoEmpty: "Ningún usuario encontrado",
        infoFiltered: "(filtrados desde _MAX_ registros totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    const defaultEndpoint = '/dataTable';
    await listUsers(defaultEndpoint);

    dataTable = $("#datatable_users").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listUsers = async (endpoint) => {
    try {
        const response = await fetch(endpoint);
        const users = await response.json();
        let content = ``;
        users.forEach((user) => {
            content += `
                <tr>
                    <td>${user.id}</td>
                    <td>
                        <button class="btn btn_print btn-sm btn-primary">${user.comprobante}<i class="fa-solid fa-print ms-1"></i>
                        </button>
                    </td>
                    <td>
                        <button class="btn btn_edit btn-sm btn-success centered editar"><i class="fa-solid fa-pencil"></i>
                        </button>
                    </td>
                    <td class="truncate-column">${user.fecha_hora_registro}</td>
                    <td class="truncate-column">${user.aplicaVacunaCovid}</td>
                    <td class="truncate-column">${user.aplicaVacunaInfluenza}</td>
                    <td class="truncate-column">${user.fecha_emision_comprobante}</td>
                    <td class="truncate-column">${user.nombre_aplicante}</td>
                    <td class="truncate-column">${user.lote}</td>
                    <td class="td-updateable">${user.nombre}</td>
                    <td class="td-updateable">${user.a_paterno}</td>
                    <td class="td-updateable">${user.a_materno}</td>
                    <td class="td-updateable">${user.f_nacimiento}</td>
                    <td class="td-updateable">${user.edad}</td>
                    <td class="td-updateable">${user.sexo}</td>
                    <td class="td-updateable">${user.alergias}</td>
                    <td class="td-updateable">${user.alergia_especifica}</td>
                    <td class="td-updateable">${user.fecha_ultima_vac_covid}</td>
                    <td class="td-updateable">${user.fecha_ultima_vac_influenza}</td>
                    <td class="td-updateable">${user.conformidad}</td>
                    <td class="td-updateable">${user.conformidad_vaxigrip}</td>
                    <td class="td-updateable">${user.telefono}</td>
                    <td class="td-updateable">${user.email}</td>
                    <td class="td-updateable">${user.calle}</td>
                    <td class="td-updateable">${user.num_ext}</td>
                    <td class="td-updateable">${user.colonia}</td>
                    <td class="td-updateable">${user.alcaldia}</td>
                    <td class="td-updateable">${user.cp}</td>
                </tr>`;
        });
        document.getElementById('tbody').innerHTML = content;
    } catch (ex) {
        alert('error al encontrar datos del servidor: ',ex);
    }
};

// // función  que manejará la edición de una fila cuando se hace clic en el botón

function editarFila(event) {
    const fila = event.target.closest('tr'); // Obtener la fila actual
    const celdas = fila.querySelectorAll('td'); // Obtener todas las celdas de la fila

    celdas.forEach((celda, index) => {
        if (index >= 9) {
            const valorAnterior = celda.textContent.trim(); // Obtener el valor anterior de la celda
            celda.innerHTML = `<input type="text" class="inputEdit" value="${valorAnterior}">`; // Reemplazar el contenido con un input
        }
    });

    const inputs = fila.querySelectorAll('.inputEdit'); // Obtener todos los inputs de la fila
    inputs[0].focus(); // Hacer foco en el primer input
    inputs.forEach(input => {
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                // Obtenemos los nuevos valores desde los inputs
                const nuevosValores = Array.from(inputs).map(input => input.value);

                // Obtenemos el valor de la celda 0
                const valorCelda0 = celdas[0].textContent.trim(); 

                nuevosValores.unshift(valorCelda0);
                

                const endpoint = '/update_cell';
                fetch(endpoint, {
                    method: 'POST',
                    body: JSON.stringify({ nuevosValores }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    return response.json()
                })
                .then(data => {
                    if (data && data.success === true && data.new_cells) {
                        // Obtener las celdas actualizables de esta fila
                        const celdasFila = fila.querySelectorAll('.td-updateable');

                        // Actualizar el contenido de las celdas con los datos recibidos del servidor
                        celdasFila.forEach((celda, index) => {
                            celda.textContent = data.new_cells[index];
                        });
                    } else {
                        console.error('Error en la respuesta del servidor o datos faltantes');
                    }
                })
                .catch(error => {
                    console.error('Error al enviar los datos a Flask:', error);
                });
            }
        });
    });
}

// // función  que manejará la emision de comprobante
function obtenerDatos(event) {
    const fila = event.target.closest('tr'); // Obtener la fila actual
    const celdas = fila.querySelectorAll('td'); // Obtener todas las celdas de la fila

    // Array para almacenar los valores de las celdas de nombre, a_paterno y a_materno
    const valores = [];
    // Obtenemos los valores de las celdas 0, 7, 8 y 9
    for (let i = 0; i <= 11; i++) {
        if (i === 0 || (i >= 9 && i <= 11)) {
            valores.push(celdas[i].textContent.trim());
        }
    }

    // Obtenemos el id del valor seleccionado
    const selectLote = document.getElementById('lote');
    const opcionSeleccionadaLote = selectLote.value;
    const textoSeleccionadoLote = selectLote.options[selectLote.selectedIndex]?.text;

    const selectNombreAplicante = document.getElementById('nombre-aplicante');
    const opcionSeleccionadaNombreAplicante = selectNombreAplicante.value;
    const textoSeleccionadoNombreAplicante = selectNombreAplicante.options[selectNombreAplicante.selectedIndex]?.text;

    // Verificamos si el texto está indefinido
    if (textoSeleccionadoLote === undefined || textoSeleccionadoNombreAplicante === undefined) {
        alert('Primero debes agregar un aplicante y un lote.');
        return;
    }

    // Agregamos el valor de las opciónes seleccionadas a los valores a enviar
    valores.push(opcionSeleccionadaLote, opcionSeleccionadaNombreAplicante, textoSeleccionadoLote, textoSeleccionadoNombreAplicante);

    const endpoint = '/comprobante';
    fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify({ valores: valores }), 
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('La solicitud no fue exitosa');
        }
    })
    .then(data => {
        const nextUrl = data.url;

        window.location.href = nextUrl;
    })
    .catch(error => {
        console.error('Error al enviar los datos al Servidor:', error);
    });
}

// Agregamos eventos a los botones para generar comprobante
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('btn_print')) {
        obtenerDatos(event);
    }
});

// Agregamos eventos a los botones de edición
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('btn_edit')) {
        editarFila(event);
    } 
});

function agregarOpcionLote() {
    const nuevaOpcionInput = document.getElementById("nuevo-lote");
    const nuevaOpcionValor = nuevaOpcionInput.value.trim();

    if (nuevaOpcionValor !== "") {
        const selectLote = document.getElementById("lote");

        fetch('/guardar_opcion/lote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ opcionLote: nuevaOpcionValor }),
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Error al guardar la opción de lote');
        })
        .then(data => {
            if (data.existe && data.existe !== false) {  // Si el lote no existía previamente
                const nuevaOpcionLote = document.createElement("option");
                nuevaOpcionLote.value = data.existe;
                nuevaOpcionLote.text = nuevaOpcionValor;

                if (selectLote.firstChild) {
                    selectLote.insertBefore(nuevaOpcionLote, selectLote.firstChild);
                } else {
                    selectLote.appendChild(nuevaOpcionLote);
                }

                nuevaOpcionInput.value = "";
            } else {
                alert('El lote ya existe.');
            }
        })
        .catch(error => {
            alert(`Error al guardar la opción de lote: ${error}`);
        });
    }
}

function agregarOpcionAplicante() {
    const nombreAplicanteInput = document.getElementById("nuevo-aplicante");
    const nombreAplicanteValor = nombreAplicanteInput.value.trim();

    if (nombreAplicanteValor !== "") {
        const selectAplicante = document.getElementById("nombre-aplicante");

        fetch('/guardar_opcion/aplicante', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ opcionAplicante: nombreAplicanteValor }),
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Error al guardar la opción de aplicante');
        })
        .then(data => {
            if (data.existe && data.existe !== false) { 
                const nuevaOpcionAplicante = document.createElement("option");
                nuevaOpcionAplicante.value = data.existe;
                nuevaOpcionAplicante.text = nombreAplicanteValor;

                if (selectAplicante.firstChild) {
                    selectAplicante.insertBefore(nuevaOpcionAplicante, selectAplicante.firstChild);
                } else {
                    selectAplicante.appendChild(nuevaOpcionAplicante);
                }

                nombreAplicanteInput.value = "";
            } else {
                alert('El Aplicante ya existe.');
            }
        })
        .catch(error => {
            alert(`Error al guardar la opción de aplicante: ${error}`);
        });
    }
}

function borrarOpcionLote() {
    const selectLote = document.getElementById("lote");
    const indiceSeleccionadoLote = selectLote.selectedIndex;
    const valorLote = selectLote.value;

    if (indiceSeleccionadoLote !== -1) {

        fetch(`/borrar_opcion/lote/${valorLote}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Error al eliminar la opción de lote');
        })
        .then(data => {
            if (data.existe) {
                selectLote.remove(indiceSeleccionadoLote);
            } else {
                alert('El valor no existe o no se puede eliminar.');
            }
        })
        .catch(error => {
            alert(`Error al eliminar la opción de lote: ${error}`);
        });
    }
}

function borrarOpcionAplicante() {
    const selectAplicante = document.getElementById("nombre-aplicante");
    const indiceSeleccionadoAplicante = selectAplicante.selectedIndex;
    const valorAplicante = selectAplicante.value;

    if (indiceSeleccionadoAplicante !== -1) {

        fetch(`/borrar_opcion/aplicante/${valorAplicante}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Error al eliminar la opción de aplicante');
        })
        .then(data => {
            if (data.existe) {
                selectAplicante.remove(indiceSeleccionadoAplicante);
            } else {
                alert('El valor no existe o no se puede eliminar.');
            }
        })
        .catch(error => {
            alert(`Error al eliminar la opción de aplicante: ${error}`);
        });
    }
}



window.addEventListener("load", async () => {
    await initDataTable();
});
