/*------------------------------------------------- MODULO LICENCIAMIENTO MICROSOFT 365 ------------------------------------------*/

async function licenciamiento() {
  await cargarDatosLicenciamiento();
  inicializarTablasLicencias();
  document.getElementById('contenidoPrincipal_licenciamiento').style.display = 'block';
}

function inicializarTablasLicencias() {
    inicializarTablaLicencias('tablaLicenciasMicrosoft365', 'microsoft365');
    inicializarTablaLicencias('tablaLicenciasFreeTrial', 'freeTrial');
    inicializarTablaLicencias('tablaLicenciasSinCategorizar', 'sinCategorizar');
}

function inicializarTablaLicencias(idTabla, tipo) {
    const tabla = $(`#${idTabla}`);
    // Obtenemos el div que contiene la tabla y su título
    const contenedorTabla = tabla.closest('.contenedor-tabla-licencias');

    if ($.fn.DataTable.isDataTable(tabla)) {
        tabla.DataTable().destroy();
        tabla.find('tbody').empty();
    }
    const datos = obtenerDatosLicencias(tipo);

    if ((tipo === 'microsoft365' || tipo === 'freeTrial') && datos.length === 0) {
        contenedorTabla.hide();
        return; 
    } else {
        contenedorTabla.show(); 
    }

    const columnas = [
        {
            title: "Nombre Licencia",
            data: "nombreLicencia",
        },
        {
            title: "SKU Part Number",
            data: "skuPartNumber"
        },
        {
            title: "Nombre Comercial",
            data: "nombreComercial",
            render: function (data, type, row) {
                return formatearLicenciaConEstilo(data, row);
            }
        },
        {
            title: "Compradas",
            data: 'compradas',
            render: function (data, type, row) {
                return formatearValorLicencia(data, 'compradas');
            }
        },
        {
            title: "Vencidas",
            data: 'vencidas',
            render: function (data, type, row) {
                return formatearValorLicencia(data, 'vencidas');
            }
        },
        {
            title: "Asignadas",
            data: 'asignadas',
            render: function (data, type, row) {
                return formatearValorLicencia(data, 'asignadas');
            }
        },
        {
            title: "Disponibles",
            data: 'disponibles',
            render: function (data, type, row) {
                return formatearValorLicencia(data, 'disponibles');
            }
        }
    ];

    tabla.DataTable({
        data: datos,
        columns: columnas,
        paging: false,
        searching: false,
        infoCallback: function (settings, start, end, max, total, pre) {
            return `${total} Licencias`;
        },
        order: [[3, 'desc']],
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.0.2/i18n/es-ES.json'
        },
        initComplete: function () {
            $(`#${idTabla} tbody tr`).each(function () {
                $(this).find("td:nth-child(4), td:nth-child(5), td:nth-child(6), td:nth-child(7)").css("text-align", "center");
            });
        }
    });
}

function formatearValorLicencia(valor, tipo) {
    let colorFondo = "", colorTexto = "", colorBorde = "", icono = "";

    switch (tipo) {
        case "compradas":
            if (valor === 0) {
                icono = `<i class="fas fa-box-open"></i>`; // Gris
                colorFondo = "#e2e3e5";
                colorTexto = "#6c757d";
                colorBorde = "#6c757d";
            } else {
                icono = `<i class="fas fa-box-open"></i>`; // Verde
                colorFondo = "#c3e6cb";
                colorTexto = "#0b5d1e";
                colorBorde = "#0b5d1e";
            }
            break;

        case "vencidas":
            if (valor === 0) {
                icono = `<i class="fas fa-check-circle"></i>`; // Verde
                colorFondo = "#c3e6cb";
                colorTexto = "#0b5d1e";
                colorBorde = "#0b5d1e";
            } else {
                icono = `<i class="fas fa-times-circle"></i>`; // Rojo
                colorFondo = "#f8d7da";
                colorTexto = "#721c24";
                colorBorde = "#721c24";
            }
            break;

        case "asignadas":
            if (valor === 0) {
                icono = `<i class="fas fa-user-slash"></i>`;
                colorFondo = "#e2e3e5";
                colorTexto = "#6c757d";
                colorBorde = "#6c757d";
            } else {
                icono = `<i class="fas fa-user-check"></i>`;
                colorFondo = "#c3e6cb";
                colorTexto = "#0b5d1e";
                colorBorde = "#0b5d1e";
            }
            break;

        case "disponibles":
            if (valor === 0) {
                icono = `<i class="fas fa-ban"></i>`;
                colorFondo = "#f8d7da";
                colorTexto = "#721c24";
                colorBorde = "#721c24";
            } else if (valor === 1 || valor === 2) {
                icono = `<i class="fas fa-exclamation-triangle"></i>`;
                colorFondo = "#fff3cd";
                colorTexto = "#856404";
                colorBorde = "#856404";
            } else {
                icono = `<i class="fas fa-check-circle"></i>`;
                colorFondo = "#c3e6cb";
                colorTexto = "#0b5d1e";
                colorBorde = "#0b5d1e";
            }
            break;
    }
    return `
    <div style="
        width: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        margin: 0 auto;
        background-color: ${colorFondo};
        color: ${colorTexto};
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid ${colorBorde};
        font-size: 0.90rem;
        white-space: nowrap;
        text-align: center;
    ">
        ${icono}
        <span>${valor}</span>
    </div>
`;
}