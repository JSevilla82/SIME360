const filtroUltimaActividad_SP = document.querySelector('.filtroUltimaActividad_SP');
const filtroVisitas_SP = document.querySelector('.filtroVisitas_SP');
const filtroArchivosActivos_SP = document.querySelector('.filtroArchivosActivos_SP');
const selectPeriodo_SP = document.querySelector(".filtroPeriodoInformes_SP");


const btnLimpiarUltimaActividad_SP = document.querySelector('.btn-limpiar-filtroUltimaActividad_SP');
const btnLimpiarfiltroVisitas_SP = document.querySelector('.btn-limpiar-filtroVisitas_SP');
const btnLimpiarfiltroArchivosActivos_SP = document.querySelector('.btn-limpiar-filtroArchivosActivos_SP');


let BD_InformeSitioSharePoint = [];
let BD_SitioSharePoint = [];
const cacheInformesSP = {};


async function sitiosSharePoint() {

  if (BD_InformeSitioSharePoint.length > 0) {
    return;
  }

  configurarSelectedFiltros_SP();
  configurarBotonExportar();

  try {
    await descargarInformeSitiosSharePoint();
    actualizarEstiloSelectCacheSP();

  } catch (error) {
    console.error("Error al procesar informes de uso:", error);
  }
  document.getElementById("contenidoPrincipal_sitiosSharepoint").style.display = "block";
}

function configurarSelectedFiltros_SP() {

  llenarFiltroUltimaActividad_SP();
  activarFiltroConLimpiar(".filtroUltimaActividad_SP");
  aplicarBordeSiTieneValor(filtroUltimaActividad_SP);

  llenarFiltroVisitasSP();
  activarFiltroConLimpiar(".filtroVisitas_SP");
  aplicarBordeSiTieneValor(filtroVisitas_SP);

  llenarFiltroArchivosActivosSP();
  activarFiltroConLimpiar(".filtroArchivosActivos_SP");
  aplicarBordeSiTieneValor(filtroArchivosActivos_SP);

  if (selectPeriodo_SP) {
    selectPeriodo_SP.addEventListener("change", async () => {
        await descargarInformeSitiosSharePoint();
        actualizarEstiloSelectCacheSP();
    });
  }
}

function configurarBotonExportar() {
    const btnExportar = document.querySelector('.btn-ExportarInformeExcel_SP');
    if (btnExportar) {
        btnExportar.addEventListener('click', function () {
            const tabla = $('#tablaSitiosSharePoint').DataTable();
            const datosParaExportar = tabla.rows({ search: 'applied' }).data().toArray();
            exportarAExcelSharePoint(datosParaExportar);
        });
    }
}


function llenarFiltroUltimaActividad_SP() {

    if (!filtroUltimaActividad_SP) return;

    filtroUltimaActividad_SP.innerHTML = '<option value="" selected hidden>🔎 Última actividad</option>';

    const groupOtros = document.createElement('optgroup');
    groupOtros.label = '☰ Opciones generales';

    const opcionConActividad = document.createElement('option');
    opcionConActividad.value = 'conActividad';
    opcionConActividad.textContent = '📈 Sitios con actividad';
    groupOtros.appendChild(opcionConActividad);

    const opcionSinSesion = document.createElement('option');
    opcionSinSesion.value = 'sinActividad';
    opcionSinSesion.textContent = '🚫 Sitios sin actividad';
    groupOtros.appendChild(opcionSinSesion);

    filtroUltimaActividad_SP.appendChild(groupOtros);

    const groupFechas = document.createElement('optgroup');
    groupFechas.label = '📅 Por rango de fecha';

    const rangos = [
        { value: 'menos7dias', text: 'Últimos 7 días' },
        { value: 'entre7y15', text: 'Entre 7 y 15 días' },
        { value: 'entre15y30', text: 'Entre 15 y 30 días' },
        { value: 'entre1y3meses', text: 'Entre 1 y 3 meses' },
        { value: 'entre3y6meses', text: 'Entre 3 y 6 meses' },
        { value: 'entre6y12meses', text: 'Entre 6 meses y 1 año' },
        { value: 'mas1ano', text: 'Más de 1 año' }
    ];

    rangos.forEach(r => {
        const option = document.createElement('option');
        option.value = r.value;
        option.textContent = r.text;
        groupFechas.appendChild(option);
    });

    filtroUltimaActividad_SP.appendChild(groupFechas);
}

function llenarFiltroVisitasSP() {

  if (!filtroVisitas_SP) return;

  filtroVisitas_SP.innerHTML = `
    <option value="" selected hidden>🔎 Visitas</option>
    <option value="con_visitas">📈 Con visitas</option>
    <option value="sin_visitas">🚫 Sin visitas</option>
    <option value="pocas_visitas">Pocas visitas (1–10)</option>
    <option value="visitas_moderadas">Visitas moderadas (11–50)</option>
    <option value="muchas_visitas">Muchas visitas (más de 50)</option>
  `;

}

function llenarFiltroArchivosActivosSP() {

  if (!filtroArchivosActivos_SP) return;

  filtroArchivosActivos_SP.innerHTML = `
                <option value="" selected hidden>🔎 Archivos activos</option>
                <option value="con_activos">📈 Con archivos activos</option>
                <option value="sin_activos">🚫 Sin archivos activos</option>
            `;
}



function procesarDatosSitiosSharePoint() {

  return BD_InformeSitioSharePoint.map((item) => {
    const sitioRelacionado = BD_SitioSharePoint.find(
      (sitio) => sitio["ID del sitio (Site Id)"] === item["ID del sitio (Site Id)"]
    );

    const ultimaActividad = item["Última actividad (Last Activity Date)"] || "Sin actividad";
    const cantidadArchivos = item["Cantidad de archivos (File Count)"] || "0";
    const archivosActivos = item["Archivos activos (Active File Count)"] || "0";
    const visitasPagina = item["Cantidad de visitas (Page View Count)"] || "0";

    const almacenamientoUsadoRaw = item["Almacenamiento usado (Storage Used GB)"] || "0";
    const almacenamientoAsignadoRaw = item["Almacenamiento asignado (Storage Allocated GB)"] || "0";

    const almacenamientoUsado = parseFloat(almacenamientoUsadoRaw);
    const almacenamientoAsignado = parseFloat(almacenamientoAsignadoRaw);

    const porcentajeUso = almacenamientoAsignado > 0 ? Math.round((almacenamientoUsado / almacenamientoAsignado) * 100) : 0;

    const almacenamiento = `${almacenamientoUsado} GB / ${almacenamientoAsignado} GB`;

    const fechaCreacion = sitioRelacionado?.["Fecha de creación"] || "Desconocida";
    const nombreSitio = sitioRelacionado?.["Nombre del sitio"] || "Nombre no disponible";
    const urlSitio = sitioRelacionado?.["URL del sitio (Site URL)"] || "URL no disponible";

    return {
      ultimaActividad: ultimaActividad,
      cantidadArchivos: cantidadArchivos,
      archivosActivos: archivosActivos,
      visitasPagina: visitasPagina,
      almacenamiento: almacenamiento,
      porcentajeUsoAlmacenamiento: `${porcentajeUso}%`,
      fechaCreacion: fechaCreacion,
      nombreSitio: nombreSitio,
      urlSitio: urlSitio,
    };
  }).filter(sitio => sitio.urlSitio !== "URL no disponible");

}

async function descargarInformeSitiosSharePoint() {
  const periodoSeleccionado = document.querySelector('.filtroPeriodoInformes_SP').value;

  if (cacheInformesSP[periodoSeleccionado]) {
      BD_InformeSitioSharePoint = cacheInformesSP[periodoSeleccionado].datos;
      const datosProcesados = procesarDatosSitiosSharePoint();
      actualizarEstadisticasSharePoint(datosProcesados);
      mostrarInformeSitiosSharePoint(datosProcesados);
      return;
  }

  await mostrarCargaProceso(
    [
      {
        titulo: "Obteniendo datos de los sitios de SharePoint",
        icono: "/static/img/SharePointSites_Logo.png",
        funcion: procesarSitiosSharePoint,
      },
      {
        titulo: "Recopilando informes de SharePoint",
        icono: "/static/img/SharePoint_Logo.png",
        funcion: () => procesarInformeSitiosSharePoint(periodoSeleccionado),
      },
    ],
    periodoSeleccionado
  );

  const datosProcesados = procesarDatosSitiosSharePoint();
  cacheInformesSP[periodoSeleccionado] = {
      datos: BD_InformeSitioSharePoint,
      fecha: new Date()
  };
  actualizarEstadisticasSharePoint(datosProcesados);
  mostrarInformeSitiosSharePoint(datosProcesados);
}

async function procesarSitiosSharePoint() {
  if (BD_SitioSharePoint.length > 0) return;
  try {
    const resultado = await consultarRecurso("sitiosSharePoint");

    if (resultado.error || !Array.isArray(resultado.datos)) {
      console.error("No se pudieron obtener los sitios de SharePoint:", resultado.error);
      return;
    }
    BD_SitioSharePoint = resultado.datos;
  } catch (error) {
    console.error("Error al procesar los sitios de SharePoint:", error);
  }
}

async function procesarInformeSitiosSharePoint(periodo) {
    try {
        const resultado = await consultarRecurso("informeSharePointSitios", { dias: periodo });
        if (resultado.error || !Array.isArray(resultado.datos)) {
            console.error("No se pudo obtener el informe de uso de SharePoint:", resultado.error);
            BD_InformeSitioSharePoint = [];
            return;
        }
        BD_InformeSitioSharePoint = resultado.datos;
    } catch (error) {
        console.error("Error al procesar el informe de SharePoint:", error);
        BD_InformeSitioSharePoint = [];
    }
}


function esFechaValida(fecha) {
  return moment(fecha, moment.ISO_8601, true).isValid();
}

async function mostrarInformeSitiosSharePoint(datos) {
  try {
    const tabla = $("#tablaSitiosSharePoint");

    if ($.fn.DataTable.isDataTable(tabla)) {
      tabla.DataTable().clear().rows.add(datos).draw();
      return;
    }
    
    const table = tabla.DataTable({
      data: datos,
      columns: [
        {
          data: "fechaCreacion",
          title: "Fecha de Creación",
          className: "text-center",
          render: function (data, type, row) {
            if (type === 'display') {
              return formatearFechaDDMMYYYY(data);
            }
            if (!data || !esFechaValida(data)) {
              return 0;
            }
            return new Date(data).getTime();
          },
        },
        { data: "nombreSitio", title: "Nombre del Sitio", width: "20%" },
        {
          data: "ultimaActividad",
          title: "Última actividad",
          className: "text-center",
          render: function (data, type, row) {
            if (type === 'display') {
              return formatearUltimaActividad(data);
            }
            if (!data || !esFechaValida(data)) {
              return 0;
            }
            return new Date(data).getTime();
          },
        },
        { data: "cantidadArchivos", title: "Archivos", className: "text-center" },
        { data: "archivosActivos", title: "Arch. activos", className: "text-center" },
        {
          data: "visitasPagina",
          title: "Visitas",
          className: "text-center",
        },
        {
          data: "almacenamiento",
          title: "Usado (GB)",
          className: "text-center",
          type: "num",
          render: function (data, type, row) {
            const usado = parseFloat(data.split("/")[0].trim().replace(" GB", ""));
            return type === "display" ? formatearEspacioGB(usado) : usado;
          },
        },
        {
          data: "almacenamiento",
          title: "Asignado (GB)",
          className: "text-center",
          type: "num",
          render: function (data, type, row) {
            const asignado = parseFloat(data.split("/")[1].trim().replace(" GB", ""));
            return type === "display" ? formatearEspacioGB(asignado) : asignado;
          },
        },

        {
          data: "almacenamiento",
          title: " Almacenamiento",
          render: function (data) {
            return formatearAlmacenamiento(data);
          },
        },
        {
          data: "porcentajeUsoAlmacenamiento",
          title: "Uso, asignado",
          className: "text-center",
          render: function (data) {
            return formatearUsoPorcentaje(data);
          },
        },
        {
          data: "urlSitio",
          title: "Url",
          render: function (data) {
            return formatearURLSitio(data);
          },
        },
      ],
      responsive: true,
      pageLength: 10,
      order: [[6, "desc"]],
      language: {
        url: "https://cdn.datatables.net/plug-ins/2.0.2/i18n/es-ES.json",
      },
    });

    // lógica del filtro de última actividad
    $.fn.dataTable.ext.search.push(
        function( settings, data, dataIndex ) {
            const filtro = filtroUltimaActividad_SP.value;
            if (!filtro) return true;

            const fechaTexto = table.row(dataIndex).data().ultimaActividad;

            if (filtro === 'conActividad') {
                return fechaTexto !== 'Sin actividad';
            }
            if (filtro === 'sinActividad') {
                return fechaTexto === 'Sin actividad';
            }

            if (fechaTexto === 'Sin actividad' || !moment(fechaTexto, 'YYYY-MM-DD').isValid()) {
                return false;
            }

            const fecha = moment(fechaTexto, "YYYY-MM-DD");
            const hoy = moment();
            const dias = hoy.diff(fecha, 'days');

            switch (filtro) {
                case 'menos7dias': return dias <= 7;
                case 'entre7y15': return dias > 7 && dias <= 15;
                case 'entre15y30': return dias > 15 && dias <= 30;
                case 'entre1y3meses': return hoy.diff(fecha, 'months') >= 1 && hoy.diff(fecha, 'months') < 3;
                case 'entre3y6meses': return hoy.diff(fecha, 'months') >= 3 && hoy.diff(fecha, 'months') < 6;
                case 'entre6y12meses': return hoy.diff(fecha, 'months') >= 6 && hoy.diff(fecha, 'months') < 12;
                case 'mas1ano': return hoy.diff(fecha, 'years') >= 1;
                default: return true;
            }
        }
    );

    filtroUltimaActividad_SP.addEventListener('change', function() {
        table.draw();
    });
    
    // Lógica del filtro de visitas
    $.fn.dataTable.ext.search.push(
        function(settings, data, dataIndex) {
            const filtro = filtroVisitas_SP.value;
            if (!filtro) return true;

            const visitas = parseInt(table.row(dataIndex).data().visitasPagina, 10);

            switch (filtro) {
                case 'con_visitas': return visitas > 0;
                case 'sin_visitas': return visitas === 0;
                case 'pocas_visitas': return visitas >= 1 && visitas <= 10;
                case 'visitas_moderadas': return visitas >= 11 && visitas <= 50;
                case 'muchas_visitas': return visitas > 50;
                default: return true;
            }
        }
    );

    filtroVisitas_SP.addEventListener('change', function() {
        table.draw();
    });

    // Lógica del filtro de archivos activos
    $.fn.dataTable.ext.search.push(
        function(settings, data, dataIndex) {
            const filtro = filtroArchivosActivos_SP.value;
            if (!filtro) return true;

            const archivosActivos = parseInt(table.row(dataIndex).data().archivosActivos, 10);

            switch (filtro) {
                case 'con_activos': return archivosActivos > 0;
                case 'sin_activos': return archivosActivos === 0;
                default: return true;
            }
        }
    );
    
    filtroArchivosActivos_SP.addEventListener('change', function() {
        table.draw();
    });


  } catch (error) {
    console.error("Error al mostrar el informe de sitios SharePoint:", error);
  }
}

function formatearURLSitio(url) {
  if (!url || url === "URL no disponible") {
    return `
            <div style="
                display: inline-flex;
                align-items: center;
                background-color: #f8d7da;
                color: #721c24;
                padding: 4px 12px;
                border-radius: 999px;
                border: 1px solid #721c24;
                font-size: 0.85rem;
                gap: 6px;
            ">
                <i class="fas fa-circle-exclamation"></i>
                N/D
            </div>
        `;
  }

  return `
        <a href="${url}" target="_blank" style="
            display: inline-flex;
            align-items: center;
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 4px 12px;
            border-radius: 999px;
            border: 1px solid #0c5460;
            font-size: 0.85rem;
            text-decoration: none;
            gap: 6px;
        ">
            <i class="fas fa-up-right-from-square"></i>
            Abrir
        </a>
    `;
}

function formatearUltimaActividad(fechaStr) {
  if (!fechaStr || fechaStr === "N/D" || fechaStr === "Sin actividad") {
    return `
            <div style="
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color:rgb(171, 171, 171);
                color:rgb(51, 51, 51);
                padding: 6px 12px;
                border-radius: 5px;
                border: 1px solidrgb(55, 55, 55);
                font-size: 0.85rem;
                gap: 8px;
                width: 90%;
                margin: auto;
            ">
                <i class="fas fa-clock"></i>
                Sin actividad
            </div>
        `;
  }

  const fechaActividad = moment(fechaStr);
  const hoy = moment();
  const diferenciaDias = hoy.diff(fechaActividad, "days");

  let colorFondo = "",
    colorTexto = "",
    colorBorde = "";

  if (diferenciaDias < 30) {
    // Verde
    colorFondo = "#c3e6cb";
    colorTexto = "#0b5d1e";
    colorBorde = "#0b5d1e";
  } else if (diferenciaDias >= 30 && diferenciaDias <= 90) {
    // Amarillo
    colorFondo = "#fff3cd";
    colorTexto = "#856404";
    colorBorde = "#856404";
  } else {
    // Rojo
    colorFondo = "#f8d7da";
    colorTexto = "#721c24";
    colorBorde = "#721c24";
  }

  return `
        <div style="
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: ${colorFondo};
            color: ${colorTexto};
            padding: 6px 12px;
            border-radius: 5px;
            border: 1px solid ${colorBorde};
            font-size: 0.85rem;
            gap: 8px;
            width: 90%;
            margin: auto;
        ">
            <i class="fas fa-calendar-alt"></i>
            ${fechaActividad.format("DD-MM-YYYY")}
        </div>
    `;
}

function actualizarEstiloSelectCacheSP() {
    const select = document.querySelector('.filtroPeriodoInformes_SP');
    if (!select) return;

    for (const option of select.options) {
        const periodo = option.value;

        if (cacheInformesSP[periodo]) {
            option.style.color = '#006400'; 
            option.style.fontWeight = 'bold';
        } else {
            option.style.color = '';
            option.style.fontWeight = '';
        }
    }
}

function actualizarEstadisticasSharePoint(datos) {
    const actualizacionInformesSharePoint = document.getElementById("actualizacionInformesSharePoint");
    const totalSitiosSharePoint = document.getElementById("totalSitiosSharePoint");
    const almacenamientoOcupadoSharePoint = document.getElementById("almacenamientoOcupadoSharePoint");

    if (BD_InformeSitioSharePoint.length > 0) {
        const fechaInforme = BD_InformeSitioSharePoint[0]["Fecha de actualización del reporte"];
        actualizacionInformesSharePoint.textContent = fechaInforme ? moment(fechaInforme, "YYYY-MM-DD").format("DD-MM-YYYY") : "-";
    } else {
        actualizacionInformesSharePoint.textContent = "-";
    }

    totalSitiosSharePoint.textContent = datos.length;

    const almacenamientoTotalBytes = BD_InformeSitioSharePoint.reduce((total, sitio) => {
        const almacenamientoUsado = parseFloat(sitio["Almacenamiento usado (Storage Used GB)"].replace(" GB", ""));
        return total + (almacenamientoUsado * 1024 * 1024 * 1024);
    }, 0);

    almacenamientoOcupadoSharePoint.textContent = formatearBytes(almacenamientoTotalBytes);
}


function formatearBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}


function exportarAExcelSharePoint(datos) {
    const filas = datos.map(sitio => {
        return `
            <tr>
                <td>${formatearFechaDDMMYYYY(sitio.fechaCreacion)}</td>
                <td>${sitio.nombreSitio}</td>
                <td>${sitio.ultimaActividad}</td>
                <td>${sitio.cantidadArchivos}</td>
                <td>${sitio.archivosActivos}</td>
                <td>${sitio.visitasPagina}</td>
                <td>${sitio.almacenamiento.split('/')[0].trim()}</td>
                <td>${sitio.almacenamiento.split('/')[1].trim()}</td>
                <td>${sitio.porcentajeUsoAlmacenamiento}</td>
                <td>${sitio.urlSitio}</td>
            </tr>
        `;
    }).join('');

    const encabezado = `
        <tr>
            <th>Fecha de Creación</th>
            <th>Nombre del Sitio</th>
            <th>Última actividad</th>
            <th>Archivos</th>
            <th>Arch. activos</th>
            <th>Visitas</th>
            <th>Usado (GB)</th>
            <th>Asignado (GB)</th>
            <th>Uso, asignado</th>
            <th>Url</th>
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
                th, td { border: 1px solid #ccc; padding: 4px; text-align: left; }
                th { background-color: #005A9E; color: white; }
            </style>
        </head>
        <body>
            <table>
                <thead>${encabezado}</thead>
                <tbody>${filas}</tbody>
            </table>
        </body>
        </html>
    `;

    const blob = new Blob([html], { type: "application/vnd.ms-excel" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `Sitios_SharePoint_${new Date().toISOString().slice(0, 10)}.xls`;
    document.body.appendChild(link);
    link.click();
    setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }, 1500);
}