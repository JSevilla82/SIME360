const botonesTabs = document.querySelectorAll('.boton-tab');
const botonExportar = document.querySelector('.acciones-independientes .boton-opcion');
const actualizacionOutlook = document.getElementById("actualizacionOutlook");
const actualizacionOneDrive = document.getElementById("actualizacionOneDrive");
const actualizacionTeams = document.getElementById("actualizacionTeams");
const actualizacionSharePoint = document.getElementById("actualizacionSharePoint");
const selectPeriodo = document.querySelector(".filtroPeriodoInformes");

let BD_InformesOutlook = [];
let BD_InformesOneDrive = [];
let BD_InformesTeams = [];
let BD_InformeSharePoint = [];
let BD_InformesUso = [];

const cacheInformes = {};
async function informesUso() {
    toggleBotones('.btn-ExportarInformeXML', true);
    if (
        BD_InformesOutlook.length > 0 &&
        BD_InformesOneDrive.length > 0 &&
        BD_InformesTeams.length > 0 &&
        BD_InformeSharePoint.length > 0
    ) {
        return;
    }
    try {
        await descargarInformes();
        const periodo = document.querySelector('.filtroPeriodoInformes').value;
        const datosFinales = cacheInformes[periodo]?.datos || procesarInformesUso(
            BD_UsuariosEntraID,
            BD_InformesOutlook,
            BD_InformesOneDrive,
            BD_InformesTeams,
            BD_InformeSharePoint
        );
        renderizarTablaInformesUso(datosFinales);
        actualizarEstiloSelectCache();
        document.getElementById('contenidoPrincipal_informesUso').style.display = 'block';
        setTimeout(() => {
            controlarColumnas([...Array(25).keys()]);
        }, 300);

    } catch (error) {
        console.error("Error al procesar informes de uso:", error);
    }
}

function toggleBotones(selector, deshabilitar = true) {
    const botones = document.querySelectorAll(selector);

    botones.forEach(btn => {
        if (!btn) return;
        btn.disabled = deshabilitar;
        btn.classList.toggle('btn-inactivo', deshabilitar);
    });
}

function mostrarBarraProgreso() {
    document.getElementById('barraProgreso').style.display = 'block';
}

function ocultarBarraProgreso() {
    document.getElementById('barraProgreso').style.display = 'none';
}

function actualizarEstiloSelectCache() {
    const select = document.querySelector('.filtroPeriodoInformes');
    if (!select) return;

    for (const option of select.options) {
        const periodo = option.value;

        if (cacheInformes[periodo]) {
            option.style.color = '#006400'; // verde
            option.style.fontWeight = 'bold';
        } else {
            option.style.color = '';
            option.style.fontWeight = '';
        }
    }
}

function controlarColumnas(columnasVisibles) {
    const tabla = $('#tablaInformesUso');
    const dataTable = tabla.DataTable();

    dataTable.columns().every(function () {
        this.visible(false);
        const th = $(this.header());
        th.removeClass('outlook-col onedrive-col teams-col sharepoint-col');
    });

    columnasVisibles.forEach(index => {
        const th = $(dataTable.column(index).header());

        dataTable.column(index).visible(true);

        if (index >= 4 && index <= 10) {
            th.addClass('outlook-col');
        } else if (index >= 11 && index <= 16) {
            th.addClass('onedrive-col'); 
        } else if (index >= 17 && index <= 20) {
            th.addClass('teams-col'); 
        } else if (index >= 21 && index <= 24) {
            th.addClass('sharepoint-col');
        }
    });
}

function validarRespuestaApi(...respuestas) {
    return respuestas.every(res => res && Array.isArray(res));
}

function combinarActividadConUso(actividad, uso, claveBusqueda, combinador) {
    return actividad.reduce((resultado, itemActividad) => {
        const clave = itemActividad[claveBusqueda];
        const itemUso = uso.find(u => u[claveBusqueda] === clave);
        if (itemUso) {
            resultado.push(combinador(itemActividad, itemUso));
        }
        return resultado;
    }, []);
}


function procesarInformesUso(BD_UsuariosEntraID, BD_InformesOutlook, BD_InformesOneDrive, BD_InformesTeams, BD_InformeSharePoint) {
    const datosProcesados = [];

    BD_UsuariosEntraID.forEach(usuario => {
        if (!usuario.skuIds) return;
        const correo = usuario.mail;
        const nombre = usuario.displayName;
        const fechaCreacion = usuario.createdDateTime
            ? moment(usuario.createdDateTime).utcOffset(-5).format("DD-MM-YYYY")
            : "No Disponible";
        const assignedLicenses = usuario.assignedLicenses || "";
        const licencias = assignedLicenses.split(",").map(licencia => licencia.trim());

        const licenciasProcesadas = licencias
            .map(licencia => {
                if (licencia.includes("F3")) return "F3";
                if (licencia.includes("E3")) return "E3";
                return null;
            })
            .filter(Boolean)
            .join(" - ");

        const licenciaPrincipal = licenciasProcesadas.length > 0
            ? licenciasProcesadas
            : "Sin Licencia";
        const datosOutlook = BD_InformesOutlook.find(item => item["Usuario Principal (User Principal Name)"] === correo) || {};
        const datosOneDrive = BD_InformesOneDrive.find(item => item["Usuario Principal (User Principal Name)"] === correo) || {};
        const datosTeams = BD_InformesTeams.find(item => item["Usuario (User Principal Name)"] === correo) || {};
        const datosSharePoint = BD_InformeSharePoint.find(item => item["Nombre de Usuario (User Principal Name)"] === correo) || {};
        const outlookUsado = parseFloat((datosOutlook["Almacenamiento usado (Storage Used)"] || "0").replace(",", "."));
        const outlookCuota = parseFloat((datosOutlook["Cuota para enviar prohibido (Prohibit Send Quota)"] || "0").replace(",", "."));
        const outlookPorcentajeUso = outlookCuota > 0 ? Math.round((outlookUsado / outlookCuota) * 100) : 0;
        const onedriveUsado = parseFloat((datosOneDrive["Almacenamiento usado (Storage Used)"] || "0").replace(",", "."));
        const onedriveAsignado = parseFloat((datosOneDrive["Almacenamiento asignado (Storage Allocated)"] || "0").replace(",", "."));
        const onedrivePorcentajeUso = onedriveAsignado > 0 ? Math.round((onedriveUsado / onedriveAsignado) * 100) : 0;
        datosProcesados.push({
            nombre,
            correo,
            fechaCreacion,
            licenciaPrincipal,
            outlook_actividad: datosOutlook["Última actividad (Last Activity Date)"] || "Sin Actividad",
            outlook_almacenamiento: `${outlookUsado} / ${outlookCuota}`,
            outlook_uso_porcentaje: `${outlookPorcentajeUso}%`,
            outlook_recibidos: datosOutlook["Correos recibidos (Receive Count)"] || "0",
            outlook_enviados: datosOutlook["Correos enviados (Send Count)"] || "0",
            outlook_items: datosOutlook["Cantidad de elementos (Item Count)"] || "0",
            outlook_archivo: datosOutlook["¿Tiene archivo en línea? (Has Archive)"] === "True" ? "Sí" : "No",
            onedrive_actividad: datosOneDrive["Última actividad (Last Activity Date)"] || "Sin Actividad",
            onedrive_almacenamiento: `${onedriveUsado} / ${onedriveAsignado}`,
            onedrive_uso_porcentaje: `${onedrivePorcentajeUso}%`,
            onedrive_sincronizados: datosOneDrive["Archivos sincronizados (Synced File Count)"] || "0",
            onedrive_archivos: datosOneDrive["Cantidad de archivos (File Count)"] || "0",
            onedrive_activos: datosOneDrive["Archivos activos (Active File Count)"] || "0",
            teams_actividad: datosTeams["Última actividad Teams (Last Activity Date)"] || "Sin Actividad",
            teams_llamadas: datosTeams["Llamadas Realizadas (Call Count)"] || "0",
            teams_reuniones: datosTeams["Reuniones (Meeting Count)"] || "0",
            teams_mensajes: datosTeams["Mensajes en Chats Privados (Private Chat Message Count)"] || "0",
            sharepoint_actividad: datosSharePoint["Última Actividad (Last Activity Date)"] || "Sin Actividad",
            sharepoint_archivos_vistos: datosSharePoint["Archivos Vistos o Editados (Viewed Or Edited File Count)"] || "0",
            sharepoint_archivos_sincronizados: datosSharePoint["Archivos Sincronizados (Synced File Count)"] || "0",
            sharepoint_paginas_visitadas: datosSharePoint["Páginas Visitadas (Visited Page Count)"] || "0"
        });
    });

    BD_InformesUso = datosProcesados;
    return BD_InformesUso;
}
async function procesarInformesTeams(periodoSeleccionado) {
    try {
        const resultado = await consultarRecurso("informeTeams", { periodo: periodoSeleccionado });

        if (resultado.error || !Array.isArray(resultado.datos)) {
            console.error("No se pudieron obtener los informes de Teams:", resultado.error);
            return;
        }
        BD_InformesTeams = resultado.datos;

    } catch (error) {
        console.error("Error al procesar los informes de Teams:", error);
    }
}

async function procesarInformesOneDrive(periodoSeleccionado) {
    try {
        const resultado = await consultarRecurso("informeOneDrive", { periodo: periodoSeleccionado });
        if (resultado.error || !Array.isArray(resultado.datos)) {
            console.error("No se pudieron obtener los informes de OneDrive:", resultado.error);
            return;
        }
        BD_InformesOneDrive = resultado.datos;

    } catch (error) {
        console.error("Error al procesar los informes de OneDrive:", error);
    }
}
async function procesarInformesOutlook(periodoSeleccionado) {
    try {
        const resultado = await consultarRecurso("informeOutlook", { periodo: periodoSeleccionado });

        if (resultado.error || !Array.isArray(resultado.datos)) {
            console.error("No se pudieron obtener los informes de Outlook:", resultado.error);
            return;
        }
        BD_InformesOutlook = resultado.datos;
    } catch (error) {
        console.error("Error al procesar los informes de Outlook:", error);
    }
}
async function procesarInformesSharePoint(periodoSeleccionado) {
    try {
        const resultado = await consultarRecurso("informeSharePointActividad", { periodo: periodoSeleccionado });

        if (resultado.error || !Array.isArray(resultado.datos)) {
            console.error("No se pudieron obtener los informes de SharePoint:", resultado.error);
            return;
        }

        BD_InformeSharePoint = resultado.datos;

    } catch (error) {
        console.error("Error al procesar los informes de SharePoint:", error);
    }
}
async function descargarInformes() {
    const periodoSeleccionado = document.querySelector('.filtroPeriodoInformes').value;

    if (cacheInformes[periodoSeleccionado]) {
        actualizarTablaInformesUso(cacheInformes[periodoSeleccionado].datos);
        return;
    }

    await mostrarCargaProceso([
        {
            titulo: "Obteniendo datos del servidor",
            icono: "/static/img/servidor.png",
            funcion: () => cargarDatosLicenciamiento(false)
        },
        {
            titulo: `Recopilando informes de Outlook`,
            icono: '/static/img/Outlook_Logo.png',
            funcion: () => procesarInformesOutlook(periodoSeleccionado)
        },
        {
            titulo: `Recopilando informes de OneDrive`,
            icono: '/static/img/OneDrive_Logo.png',
            funcion: () => procesarInformesOneDrive(periodoSeleccionado)
        },
        {
            titulo: `Recopilando informes de Teams`,
            icono: '/static/img/MicrosoftTeams_Logo.png',
            funcion: () => procesarInformesTeams(periodoSeleccionado)
        },
        {
            titulo: `Recopilando informes de SharePoint`,
            icono: '/static/img/SharePoint_Logo.png',
            funcion: () => procesarInformesSharePoint(periodoSeleccionado)
        }
    ], periodoSeleccionado);

    actualizarFechasInformes();

    const datosFinales = procesarInformesUso(
        BD_UsuariosEntraID,
        BD_InformesOutlook,
        BD_InformesOneDrive,
        BD_InformesTeams,
        BD_InformeSharePoint
    );

    cacheInformes[periodoSeleccionado] = {
        datos: datosFinales,
        fecha: new Date()
    };

    actualizarTablaInformesUso(datosFinales);
    actualizarEstiloSelectCache();
}

function actualizarTablaInformesUso(datos) {
    const tabla = $('#tablaInformesUso').DataTable();
    tabla.clear();
    tabla.rows.add(datos);
    tabla.draw();
}

function actualizarFechasInformes() {
    const fechaOutlook = BD_InformesOutlook[0]?.["Fecha de Informe (Report Refresh Date)"];
    const fechaOneDrive = BD_InformesOneDrive[0]?.["Fecha de Informe (Report Refresh Date)"];
    const fechaTeams = BD_InformesTeams[0]?.["Fecha de Informe (Report Refresh Date)"];
    const fechaSharePoint = BD_InformeSharePoint[0]?.["Fecha de Informe (Report Refresh Date)"];

    actualizacionOutlook.textContent = fechaOutlook ? moment(fechaOutlook, "YYYY-MM-DD").format("DD-MM-YYYY") : "-";
    actualizacionOneDrive.textContent = fechaOneDrive ? moment(fechaOneDrive, "YYYY-MM-DD").format("DD-MM-YYYY") : "-";
    actualizacionTeams.textContent = fechaTeams ? moment(fechaTeams, "YYYY-MM-DD").format("DD-MM-YYYY") : "-";
    actualizacionSharePoint.textContent = fechaSharePoint ? moment(fechaSharePoint, "YYYY-MM-DD").format("DD-MM-YYYY") : "-";
}
function renderizarTablaInformesUso(datos) {
    const tabla = $('#tablaInformesUso');

    if ($.fn.DataTable.isDataTable(tabla)) {
        tabla.DataTable().destroy();
        tabla.find('tbody').empty();
    }
    const columnasRaw = [
        { title: "Nombre", data: "nombre" },
        { title: "Correo", data: "correo" },
        {
            title: "Fecha Creación",
            data: "fechaCreacion"
        },
        {
            title: "Licencia Principal",
            data: "licenciaPrincipal",
            render: function (data) {
                return formatearLicenciaPrincipal(data);
            }
        },
        {
            title: "Últ. act. Outlook",
            data: "outlook_actividad",
            render: function (data) {
                return formatearFechaDDMMYYYY(data);
            }
        },
        {
            title: "Almacenam. Outlook",
            data: "outlook_almacenamiento",
            render: function (data) {
                return formatearAlmacenamiento(data);
            }
        },
        {
            title: "Uso %",
            data: "outlook_uso_porcentaje",
            render: function (data) {
                return formatearUsoPorcentaje(data);
            }
        },
        {
            title: "Rec.",
            data: "outlook_recibidos",
            render: function (data, type, row) {
                return formatearCorreos(data, 'rec', row.outlook_recibidos, row.outlook_enviados);
            }
        },
        {
            title: "Env.",
            data: "outlook_enviados",
            render: function (data, type, row) {
                return formatearCorreos(data, 'env', row.outlook_recibidos, row.outlook_enviados);
            }
        },
        {
            title: "Elementos",
            data: "outlook_items"
        },
        {
            title: "Arch. en línea",
            data: "outlook_archivo",
            render: function (data) {
                return formatearArchivadoEnLinea(data);
            }
        },
        {
            title: "Últ. act. OneDrive",
            data: "onedrive_actividad",
            render: function (data) {
                return formatearFechaDDMMYYYY(data);
            }
        },
        {
            title: "Almacenam. OneDrive",
            data: "onedrive_almacenamiento",
            render: function (data) {
                return formatearAlmacenamiento(data);
            }
        },
        {
            title: "Uso %",
            data: "onedrive_uso_porcentaje",
            render: function (data) {
                return formatearUsoPorcentaje(data);
            }
        },
        {
            title: "Arch. sinc.",
            data: "onedrive_sincronizados"
        },
        {
            title: "Total arch.",
            data: "onedrive_archivos"
        },
        {
            title: "Arch. activos",
            data: "onedrive_activos"
        },
        {
            title: "Últ. act. Teams",
            data: "teams_actividad",
            render: function (data) {
                return formatearFechaDDMMYYYY(data);
            }
        },
        {
            title: "Llamadas",
            data: "teams_llamadas"
        },
        {
            title: "Reuniones",
            data: "teams_reuniones"
        },
        {
            title: "Msjs. privados",
            data: "teams_mensajes"
        },
        {
            title: "Últ. act. SharePoint",
            data: "sharepoint_actividad",
            render: function (data) {
                return formatearFechaDDMMYYYY(data);
            }
        },
        {
            title: "Arch. vistos",
            data: "sharepoint_archivos_vistos"
        },
        {
            title: "Arch. sinc.",
            data: "sharepoint_archivos_sincronizados"
        },
        {
            title: "Páginas visitadas",
            data: "sharepoint_paginas_visitadas"
        }
    ];

    const columnas = columnasRaw.map(col => ({
        ...col,
        className: "text-center"
    }));

    tabla.DataTable({
        data: datos,
        columns: columnas,
        scrollX: true,
        scrollCollapse: true,
        fixedColumns: {
            leftColumns: 2
        },
        responsive: false,
        pageLength: 10,
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.0.2/i18n/es-ES.json'
        },
        initComplete: function () {
            $('input[type="search"]').attr('autocomplete', 'off');
        }
    });
    setupTableInteractionsInformesUso();
}
function formatearLicenciaPrincipal(valor) {
    if (!valor) return "";

    const licencias = valor.split("-").map(v => v.trim());
    const fragmentos = licencias.map(licencia => {
        let colorFondo = "", colorTexto = "", colorBorde = "", icono = "";

        if (licencia === "E3") {
            icono = `<i class="fas fa-briefcase"></i>`;
            colorFondo = "#ffe6cc";
            colorTexto = "#b45309";
            colorBorde = "#b45309";
        } else if (licencia === "F3") {
            icono = `<i class="fas fa-check-circle"></i>`;
            colorFondo = "#e0ecff";
            colorTexto = "#3b82f6";
            colorBorde = "#3b82f6";
        } else {
            icono = `<i class="fas fa-ban"></i>`;
            colorFondo = "#f0f0f0";
            colorTexto = "#6c757d";
            colorBorde = "#6c757d";
            licencia = "Sin Licencia";
        }

        return `
            <div style="
                display: inline-flex; /* Asegura que los elementos estén en una sola fila */
                align-items: center;
                gap: 6px;
                background-color: ${colorFondo};
                color: ${colorTexto};
                padding: 4px 12px;
                border-radius: 999px;
                border: 1px solid ${colorBorde};
                font-size: 0.85rem;
                white-space: nowrap;
                margin-right: 6px; /* Espacio entre los elementos */
                margin-bottom: 5px; /* Espacio para evitar superposiciones */
            ">
                ${icono}
                <span>${licencia}</span>
            </div>
        `;
    });

    return `<div style="display: flex; flex-wrap: nowrap;">${fragmentos.join("")}</div>`;
}

function formatearArchivadoEnLinea(valor) {
    let colorFondo = "", colorTexto = "", colorBorde = "", texto = "";

    const valorNormalizado = (valor || "")
        .toString()
        .normalize("NFD") // Elimina tildes
        .replace(/[\u0300-\u036f]/g, "")
        .trim()
        .toLowerCase();

    if (valorNormalizado === "si") {
        colorFondo = "#d4edda";  
        colorTexto = "#155724";  
        colorBorde = "#155724";  
        texto = "Sí";
    } else {
        colorFondo = "#e2e3e5"; 
        colorTexto = "#6c757d";  
        colorBorde = "#6c757d";  
        texto = "No";
    }

    return `
        <div style="
            display: inline-block;
            background-color: ${colorFondo};
            color: ${colorTexto};
            padding: 4px 12px;
            border-radius: 999px;
            border: 1px solid ${colorBorde};
            font-size: 0.85rem;
            text-align: center;
            min-width: 48px;
        ">
            ${texto}
        </div>
    `;
}
function formatearCorreos(valor, tipo, recibidos, enviados) {
    const cantidad = parseInt(valor.trim());
    const rec = parseInt(recibidos);
    const env = parseInt(enviados);

    let colorTexto = "", icono = "";
    if (rec === 0 && env === 0) {
        colorTexto = "#6c757d"; 
    } else if (rec === 0 || env === 0) {
        colorTexto = "#cc5200";
    } else {
        colorTexto = "#0b5d1e";
    }
    icono = tipo === 'rec'
        ? `<i class="fas fa-inbox"></i>`
        : `<i class="fas fa-paper-plane"></i>`;

    return `
        <div style="text-align: center; color: ${colorTexto}; font-size: 14px;">
            ${icono} ${cantidad}
        </div>
    `;
}
function setupTableInteractionsInformesUso() {
    const table = $('#tablaInformesUso').DataTable();

    $('#tablaInformesUso tbody').on('click', 'tr', function (event) {
    });

    $('#tablaInformesUso tbody').on('dblclick', 'tr', function (event) {
        mostrarRegistroEnModalInformes(table, this);
    });
}

function seleccionarRegistroInformes(table, row) {
    table.$('tr.selected').removeClass('selected');
    $(row).addClass('selected');
}

function mostrarRegistroEnModalInformes(table, row) {
    const data = table.row(row).data();
    const modalContent = formatearParaModalInformes(data);

    Swal.fire({
        html: modalContent,
        width: '1000px',
        showCloseButton: true,
        showConfirmButton: false,
        focusConfirm: false,
        customClass: {
            container: 'user-usage-modal'
        }
    });
}

function formatearParaModalInformes(data) {
    const fechaCreacion = formatearFechaDDMMYYYY(data.fechaCreacion);
    const licenciaPrincipal = formatearLicenciaPrincipal(data.licenciaPrincipal);

    return `
    <div class="user-usage-modal-container">
        <!-- Encabezado con estilo azul -->
        <div class="user-header-blue">
            <h2 class="user-name">${data.nombre || 'Nombre no disponible'}</h2>
            <p class="user-email">${data.correo || 'No disponible'}</p>
            <div class="user-meta">
                <span class="user-creation-date">Creado: ${fechaCreacion}</span>
                <span class="user-license">${licenciaPrincipal}</span>
            </div>
        </div>

        <div class="usage-sections">
            <!-- Sección Outlook -->
            <div class="usage-section outlook-section">
                <h3 class="section-title"><i class="fas fa-envelope"></i> Outlook</h3>
                <div class="section-grid">
                    <div class="info-item">
                        <div class="info-label">Última actividad:</div>
                        <div class="info-value">${formatearFechaDDMMYYYY(data.outlook_actividad)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Almacenamiento:</div>
                        <div class="info-value">${formatearAlmacenamiento(data.outlook_almacenamiento)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Uso:</div>
                        <div class="info-value">${formatearUsoPorcentaje(data.outlook_uso_porcentaje)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Correos recibidos:</div>
                        <div class="info-value">${formatearCorreos(data.outlook_recibidos, 'rec', data.outlook_recibidos, data.outlook_enviados)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Correos enviados:</div>
                        <div class="info-value">${formatearCorreos(data.outlook_enviados, 'env', data.outlook_recibidos, data.outlook_enviados)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Elementos:</div>
                        <div class="info-value">${data.outlook_items || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Archivado en línea:</div>
                        <div class="info-value">${formatearArchivadoEnLinea(data.outlook_archivo)}</div>
                    </div>
                </div>
            </div>

            <!-- Sección OneDrive -->
            <div class="usage-section onedrive-section">
                <h3 class="section-title"><i class="fas fa-cloud"></i> OneDrive</h3>
                <div class="section-grid">
                    <div class="info-item">
                        <div class="info-label">Última actividad:</div>
                        <div class="info-value">${formatearFechaDDMMYYYY(data.onedrive_actividad)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Almacenamiento:</div>
                        <div class="info-value">${formatearAlmacenamiento(data.onedrive_almacenamiento)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Uso:</div>
                        <div class="info-value">${formatearUsoPorcentaje(data.onedrive_uso_porcentaje)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Archivos sincronizados:</div>
                        <div class="info-value">${data.onedrive_sincronizados || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Total archivos:</div>
                        <div class="info-value">${data.onedrive_archivos || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Archivos activos:</div>
                        <div class="info-value">${data.onedrive_activos || 'N/A'}</div>
                    </div>
                </div>
            </div>

            <!-- Sección Teams -->
            <div class="usage-section teams-section">
                <h3 class="section-title"><i class="fas fa-users"></i> Teams</h3>
                <div class="section-grid">
                    <div class="info-item">
                        <div class="info-label">Última actividad:</div>
                        <div class="info-value">${formatearFechaDDMMYYYY(data.teams_actividad)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Llamadas:</div>
                        <div class="info-value">${data.teams_llamadas || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Reuniones:</div>
                        <div class="info-value">${data.teams_reuniones || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Mensajes privados:</div>
                        <div class="info-value">${data.teams_mensajes || 'N/A'}</div>
                    </div>
                </div>
            </div>

            <!-- Sección SharePoint -->
            <div class="usage-section sharepoint-section">
                <h3 class="section-title"><i class="fas fa-share-alt"></i> SharePoint</h3>
                <div class="section-grid">
                    <div class="info-item">
                        <div class="info-label">Última actividad:</div>
                        <div class="info-value">${formatearFechaDDMMYYYY(data.sharepoint_actividad)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Archivos vistos:</div>
                        <div class="info-value">${data.sharepoint_archivos_vistos || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Archivos sincronizados:</div>
                        <div class="info-value">${data.sharepoint_archivos_sincronizados || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Páginas visitadas:</div>
                        <div class="info-value">${data.sharepoint_paginas_visitadas || 'N/A'}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;
}
if (selectPeriodo) {
    selectPeriodo.addEventListener("change", async () => {
        const periodo = selectPeriodo.value;

        if (cacheInformes[periodo]) {
            actualizarTablaInformesUso(cacheInformes[periodo].datos);
            return;
        }

        await descargarInformes();

        const datosFinales = procesarInformesUso(
            BD_UsuariosEntraID,
            BD_InformesOutlook,
            BD_InformesOneDrive,
            BD_InformesTeams,
            BD_InformeSharePoint
        );

        cacheInformes[periodo] = {
            datos: datosFinales,
            fecha: new Date()
        };

        actualizarTablaInformesUso(datosFinales);
    });
}

botonesTabs.forEach(boton => {
    boton.addEventListener('click', function () {
        botonesTabs.forEach(b => b.classList.remove('activo'));
        this.classList.add('activo');

        const textoBoton = this.innerText.trim();

        if (textoBoton === 'Todos los Informes') {
            controlarColumnas([...Array(25).keys()]);
        }
        else if (textoBoton.includes('Outlook')) {
            controlarColumnas([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
        }
        else if (textoBoton.includes('OneDrive')) {
            controlarColumnas([0, 1, 2, 3, 11, 12, 13, 14, 15, 16]);
        }
        else if (textoBoton.includes('Teams')) {
            controlarColumnas([0, 1, 2, 3, 17, 18, 19, 20]);
        }
        else if (textoBoton.includes('SharePoint')) {
            controlarColumnas([0, 1, 2, 3, 21, 22, 23, 24]);
        }
    });
});

if (botonExportar) {
    botonExportar.addEventListener('click', function () {
    });
}
document.querySelector('.btn-ExportarInformeExcel').addEventListener('click', function () {
    const periodo = document.querySelector('.filtroPeriodoInformes').value;

    const datosFinales = cacheInformes[periodo]?.datos || procesarInformesUso(
        BD_UsuariosEntraID,
        BD_InformesOutlook,
        BD_InformesOneDrive,
        BD_InformesTeams,
        BD_InformeSharePoint
    );

    Swal.fire({
        title: 'Exportando informe',
        html: 'Por favor espere...',
        timerProgressBar: true,
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading()
    });

    setTimeout(() => {
        try {
            exportarAExcelInformesUso(datosFinales);
            Swal.fire({
                title: 'Exportación completada',
                text: 'El archivo Excel se ha generado correctamente',
                icon: 'success',
                timer: 2000,
                showConfirmButton: false
            });
        } catch (error) {
            Swal.fire({
                title: 'Error',
                text: error.message,
                icon: 'error'
            });
        }
    }, 2000);
});

function exportarAExcelInformesUso(datos) {
    const filas = datos.map(usuario => {
        return `
            <tr>
                <!-- Datos de Usuario -->
                <td>${usuario.nombre || ''}</td>
                <td>${usuario.correo || ''}</td>
                <td>${formatearFechaDDMMYYYY(usuario.fechaCreacion)}</td>
                <td>${formatearLicenciaPrincipal(usuario.licenciaPrincipal)}</td>
                
                <!-- Outlook -->
                <td>${formatearFechaDDMMYYYY(usuario.outlook_actividad)}</td>
                <td>${formatearAlmacenamiento(usuario.outlook_almacenamiento)}</td>
                <td>${formatearUsoPorcentaje(usuario.outlook_uso_porcentaje)}</td>
                <td>${formatearCorreos(usuario.outlook_recibidos, 'rec', usuario.outlook_recibidos, usuario.outlook_enviados)}</td>
                <td>${formatearCorreos(usuario.outlook_enviados, 'env', usuario.outlook_recibidos, usuario.outlook_enviados)}</td>
                <td>${usuario.outlook_items || '0'}</td>
                <td>${formatearArchivadoEnLinea(usuario.outlook_archivo)}</td>

                <!-- OneDrive -->
                <td>${formatearFechaDDMMYYYY(usuario.onedrive_actividad)}</td>
                <td>${formatearAlmacenamiento(usuario.onedrive_almacenamiento)}</td>
                <td>${formatearUsoPorcentaje(usuario.onedrive_uso_porcentaje)}</td>
                <td>${usuario.onedrive_sincronizados || '0'}</td>
                <td>${usuario.onedrive_archivos || '0'}</td>
                <td>${usuario.onedrive_activos || '0'}</td>

                <!-- Teams -->
                <td>${formatearFechaDDMMYYYY(usuario.teams_actividad)}</td>
                <td>${usuario.teams_llamadas || '0'}</td>
                <td>${usuario.teams_reuniones || '0'}</td>
                <td>${usuario.teams_mensajes || '0'}</td>

                <!-- SharePoint -->
                <td>${formatearFechaDDMMYYYY(usuario.sharepoint_actividad)}</td>
                <td>${usuario.sharepoint_archivos_vistos || '0'}</td>
                <td>${usuario.sharepoint_archivos_sincronizados || '0'}</td>
                <td>${usuario.sharepoint_paginas_visitadas || '0'}</td>
            </tr>
        `;
    }).join('');
    const encabezadoSecciones = `
        <tr>
            <th colspan="4" style="background-color: #005A9E; color: white;">Datos de Usuario</th>
            <th colspan="7" style="background-color: #0078d4; color: white;">Informes de Uso Outlook</th>
            <th colspan="6" style="background-color: #2c5282; color: white;">Informes de Uso OneDrive</th>
            <th colspan="4" style="background-color: #5a5b9f; color: white;">Informes de Uso Teams</th>
            <th colspan="4" style="background-color: #2e8b57; color: white;">Informes de Uso SharePoint</th>
        </tr>
    `;
    const encabezadoColumnas = `
        <tr>
            <!-- Datos de Usuario -->
            <th>Nombre</th>
            <th>Correo</th>
            <th>Fecha Creación</th>
            <th>Licencia Principal</th>

            <!-- Outlook -->
            <th>Últ. act.</th>
            <th>Almacenam.</th>
            <th>Uso %</th>
            <th>Rec.</th>
            <th>Env.</th>
            <th>Elementos</th>
            <th>Arch. en línea</th>

            <!-- OneDrive -->
            <th>Últ. act.</th>
            <th>Almacenam.</th>
            <th>Uso %</th>
            <th>Arch. sinc.</th>
            <th>Total arch.</th>
            <th>Arch. activos</th>

            <!-- Teams -->
            <th>Últ. act.</th>
            <th>Llamadas</th>
            <th>Reuniones</th>
            <th>Msjs. privados</th>

            <!-- SharePoint -->
            <th>Últ. act.</th>
            <th>Arch. vistos</th>
            <th>Arch. sinc.</th>
            <th>Páginas visitadas</th>
        </tr>
    `;

    const html = `
        <html xmlns:o="urn:schemas-microsoft-com:office:office"
              xmlns:x="urn:schemas-microsoft-com:office:excel"
              xmlns="http://www.w3.org/TR/REC-html40">
        <head>
            <meta charset="UTF-8">
            <style>
                table { border-collapse: collapse; font-size: 11px; font-family: Arial, sans-serif; }
                th, td { border: 1px solid #ccc; padding: 4px; text-align: center; }
                th { background-color: #00274D; color: white; }
                .section-header { background-color: #005A9E !important; }
            </style>
        </head>
        <body>
            <table>
                <thead>
                    ${encabezadoSecciones}
                    ${encabezadoColumnas}
                </thead>
                <tbody>${filas}</tbody>
            </table>
        </body>
        </html>
    `;

    const blob = new Blob([html], { type: "application/vnd.ms-excel" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `Informe_Uso_M365_${new Date().toISOString().slice(0, 10)}.xls`;
    document.body.appendChild(link);
    link.click();
    setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }, 1500);
}