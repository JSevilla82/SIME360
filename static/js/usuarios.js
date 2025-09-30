const filtroInicioSesion = document.querySelector('.filtroInicioSesion');
const filtroLicencias = document.querySelector('.filtroLicencias');
const filtroUltimaConexion = document.querySelector('.filtroUltimaConexion');
const btnLimpiarInicioSesion = document.querySelector('.btn-limpiar-filtroInicioSesion');
const btnLimpiarLicencias = document.querySelector('.btn-limpiar-filtroLicencias');
const btnLimpiarUltimaConexion = document.querySelector('.btn-limpiar-filtroConexion');
const totalUsuariosEl = document.getElementById("totalUsuarios");
const usuariosConLicenciasEl = document.getElementById("usuariosConLicencias");
const usuariosBloqueadosConLicenciaEl = document.getElementById("usuariosBloqueadosConLicencia");
const usuariosORGConLicenciaEl = document.getElementById("usuariosORGConLicencia");
const usuariosNETConLicenciaEl = document.getElementById("usuariosNETConLicencia");
const usuariosOTRConLicenciaEl = document.getElementById("usuariosOTRConLicencia");
const usuariosSinInicioSesion = document.getElementById("usuariosSinInicioSesion");
const usuariosUltimos8Dias = document.getElementById("usuariosUltimos8Dias");
const usuariosEntre8y30Dias = document.getElementById("usuariosEntre8y30Dias");
const usuariosMasDe30Dias = document.getElementById("usuariosMasDe30Dias");
const btnActualizarUsuarios = document.querySelector('.btn-ActualizarUsuarios');
const btnDescargarUltimaSesion = document.querySelector('.btn-DescargarUltimaSesion');

async function usuarios() {
  configuracionesGenerales();
  await cargarDatosLicenciamiento();
  configurarSelectedFiltros();
  procesarEstadisticasUsuarios(BD_UsuariosEntraID);
  inicializarTablaUsuariosEntraID();
  document.getElementById('contenidoPrincipal_usuarios').style.display = 'block';

}
function configuracionesGenerales() {
  controlarSelectConexion(false);
}

function controlarSelectConexion(habilitar) {
  if (!filtroUltimaConexion) return;

  if (habilitar) {
    filtroUltimaConexion.disabled = false;
    filtroUltimaConexion.style.backgroundColor = '#00274d';
    filtroUltimaConexion.style.border = '2px solid #000000';
    filtroUltimaConexion.style.color = '#ffffff';
  } else {
    filtroUltimaConexion.disabled = true;
    filtroUltimaConexion.style.backgroundColor = '#e0e0e0';
    filtroUltimaConexion.style.border = '2px solid #666666';
    filtroUltimaConexion.style.color = '#666666';
  }
}

function configurarSelectedFiltros() {
  actualizarVistaFiltroLicencias(procesarDatosFiltroLicencias(BD_LicenciasDetallesUnificados));
  activarFiltroConLimpiar(".filtroLicencias");
  aplicarBordeSiTieneValor(filtroLicencias);

  llenarFiltroInicioSesion();
  activarFiltroConLimpiar(".filtroInicioSesion");
  aplicarBordeSiTieneValor(filtroInicioSesion);

  llenarFiltroUltimaConexion();
  activarFiltroConLimpiar(".filtroUltimaConexion");
  aplicarBordeSiTieneValor(filtroUltimaConexion);
}

function llenarFiltroInicioSesion() {
  if (!filtroInicioSesion) return;

  filtroInicioSesion.innerHTML = `
        <option value="" selected hidden>🔎 Inicio de sesión</option>
        <option value="Habilitado">✅ Habilitado</option>
        <option value="Bloqueado">🔒 Bloqueado</option>
    `;
}

function llenarFiltroUltimaConexion() {
  if (!filtroUltimaConexion) return;

  filtroUltimaConexion.innerHTML = '<option value="" selected hidden>🔎 Última conexión</option>';

  const groupOtros = document.createElement('optgroup');
  groupOtros.label = '☰ Opciones generales';

  const opcionConSesion = document.createElement('option');
  opcionConSesion.value = 'conSesion';
  opcionConSesion.textContent = 'Usuarios con inicio de sesión';
  groupOtros.appendChild(opcionConSesion);

  const opcionSinSesion = document.createElement('option');
  opcionSinSesion.value = 'sinSesion';
  opcionSinSesion.textContent = 'Sin inicio de sesión';
  groupOtros.appendChild(opcionSinSesion);
  filtroUltimaConexion.appendChild(groupOtros);

  const groupFechas = document.createElement('optgroup');
  groupFechas.label = '📅 Por rango de fecha';

  const rangos = [
    { value: 'menos7dias', text: 'Últimos 7 días' },
    { value: 'entre7y15', text: 'Entre 7 y 15 días' },
    { value: 'entre15y30', text: 'Entre 15 y 30 días' },
    { value: 'entre1y3meses', text: 'Entre 1 y 3 meses' },
    { value: 'entre3y6meses', text: 'Entre 3 y 6 meses' },
    { value: 'entre6y12meses', text: 'Entre 6 meses y 1 año' },
    { value: 'mas1ano', text: 'Más de 1 año' },
    { value: 'mas2anos', text: 'Más de 2 años' }
  ];

  rangos.forEach(r => {
    const option = document.createElement('option');
    option.value = r.value;
    option.textContent = r.text;
    groupFechas.appendChild(option);
  });

  filtroUltimaConexion.appendChild(groupFechas);
}


function procesarDatosFiltroLicencias(BD) {
  const licencias = {
    licenciasPago: [],
    licenciasGratis: [],
    licenciasSinCategorizar: []
  };

  BD.forEach(licencia => {
    const nombreId = licencia.BD_IdentificadorLicencias_NombreLicencia;
    const nombreDetalle = licencia.BD_DetallesLicencias_NombreLicencia;

    let nombreMostrar = nombreId || nombreDetalle;

    if (nombreMostrar && licencia.skuId) {
      const option = document.createElement('option');
      option.value = licencia.skuId;
      option.textContent = nombreMostrar;

      const esPago = licencia.BD_IdentificadorLicencias_LicenciaDePago === 1;
      const noIdentificada = nombreId === null;

      if (noIdentificada) {
        licencias.licenciasSinCategorizar.push(option);
      } else if (esPago) {
        licencias.licenciasPago.push(option);
      } else {
        licencias.licenciasGratis.push(option);
      }
    }
  });

  return licencias;
}

function actualizarVistaFiltroLicencias(BD) {

  if (!filtroLicencias) return;

  filtroLicencias.innerHTML = '<option value="" selected hidden>🔎 Licencias</option>';

  const estadoLicencia = document.createElement('optgroup');
  estadoLicencia.label = '☰  Opciones generales';

  const opcionConLicencia = document.createElement('option');
  opcionConLicencia.value = 'conLicencia';
  opcionConLicencia.textContent = '✅ Usuarios con licencia';

  const opcionSinLicencia = document.createElement('option');
  opcionSinLicencia.value = 'sinLicencia';
  opcionSinLicencia.textContent = '🚫 Usuarios sin licencia';

  estadoLicencia.appendChild(opcionConLicencia);
  estadoLicencia.appendChild(opcionSinLicencia);
  filtroLicencias.appendChild(estadoLicencia);

  const licenciasPago = document.createElement('optgroup');
  licenciasPago.label = '💲 Licencias de pago';

  const licenciasGratis = document.createElement('optgroup');
  licenciasGratis.label = '🆓 Licencias gratis o de prueba';

  const licenciasSinCategorizar = document.createElement('optgroup');
  licenciasSinCategorizar.label = '❓ Licencias sin categorizar';

  BD.licenciasPago.forEach(option => licenciasPago.appendChild(option));
  BD.licenciasGratis.forEach(option => licenciasGratis.appendChild(option));
  BD.licenciasSinCategorizar.forEach(option => licenciasSinCategorizar.appendChild(option));

  if (licenciasPago.children.length > 0) {
    filtroLicencias.appendChild(licenciasPago);
  }

  if (licenciasGratis.children.length > 0) {
    filtroLicencias.appendChild(licenciasGratis);
  }

  if (licenciasSinCategorizar.children.length > 0) {
    filtroLicencias.appendChild(licenciasSinCategorizar);
  }
}

function procesarEstadisticasUsuarios(BD) {
  const totalUsuarios = Object.keys(BD).length;

  let usuariosConLicencias = 0;
  let usuariosBloqueadosConLicencia = 0;
  let usuariosORGConLicencia = 0;
  let usuariosNETConLicencia = 0;
  let usuariosOTRConLicencia = 0;

  for (const key in BD) {
    const usuario = BD[key];
    const tieneLicencias = usuario.skuIds && usuario.skuIds.trim() !== '';
    const esDeshabilitado = usuario.accountEnabled === "Bloqueado";
    const correo = usuario.mail || '';

    if (tieneLicencias) {
      usuariosConLicencias++;

      if (esDeshabilitado) {
        usuariosBloqueadosConLicencia++;
      }

      if (correo.endsWith("@icontec.org")) {
        usuariosORGConLicencia++;
      } else if (correo.endsWith("@icontec.net")) {
        usuariosNETConLicencia++;
      } else {
        usuariosOTRConLicencia++;
      }
    }
  }

  actualizarVistaEstadisticas({
    totalUsuarios,
    usuariosConLicencias,
    usuariosBloqueadosConLicencia,
    usuariosORGConLicencia,
    usuariosNETConLicencia,
    usuariosOTRConLicencia
  });
}

function procesarEstadisticasUsuarios_UltimoInicioSesion(DB) {
  const resultados = {
    sinInicioDeSesion: [],
    menosDe8Dias: [],
    entre8y30Dias: [],
    masDe30Dias: []
  };

  DB.forEach(usuario => {
    if (usuario.skuIds && usuario.skuIds !== "" && (!usuario.lastSignInDateTime || usuario.lastSignInDateTime === "")) {
      resultados.sinInicioDeSesion.push(usuario);
    }
    if (usuario.skuIds && usuario.skuIds !== "" && usuario.lastSignInDateTime) {
      const fechaUltimoInicio = moment(usuario.lastSignInDateTime);
      const diasDesdeUltimoInicio = moment().diff(fechaUltimoInicio, 'days');

      if (diasDesdeUltimoInicio < 8) {
        resultados.menosDe8Dias.push(usuario);
      } else if (diasDesdeUltimoInicio >= 8 && diasDesdeUltimoInicio <= 30) {
        resultados.entre8y30Dias.push(usuario);
      } else if (diasDesdeUltimoInicio > 30) {
        resultados.masDe30Dias.push(usuario);
      }
    }
  });
  actualizarVistaEstadisticas_UltimoInicioSesion(resultados);
}

function actualizarVistaEstadisticas(estadisticas) {
  totalUsuariosEl.textContent = estadisticas.totalUsuarios;
  usuariosConLicenciasEl.textContent = estadisticas.usuariosConLicencias;
  usuariosBloqueadosConLicenciaEl.textContent = estadisticas.usuariosBloqueadosConLicencia;
  usuariosORGConLicenciaEl.textContent = estadisticas.usuariosORGConLicencia;
  usuariosNETConLicenciaEl.textContent = estadisticas.usuariosNETConLicencia;
  usuariosOTRConLicenciaEl.textContent = estadisticas.usuariosOTRConLicencia;
}

function actualizarVistaEstadisticas_UltimoInicioSesion(estadisticas) {
  if (usuariosSinInicioSesion) {
    usuariosSinInicioSesion.textContent = estadisticas.sinInicioDeSesion.length || 0;
  }
  if (usuariosUltimos8Dias) {
    usuariosUltimos8Dias.textContent = estadisticas.menosDe8Dias.length || 0;
  }
  if (usuariosEntre8y30Dias) {
    usuariosEntre8y30Dias.textContent = estadisticas.entre8y30Dias.length || 0;
  }
  if (usuariosMasDe30Dias) {
    usuariosMasDe30Dias.textContent = estadisticas.masDe30Dias.length || 0;
  }
}
function setupTableInteractions() {
  const table = $('#tablaUsuariosEntraID').DataTable();

  $('#tablaUsuariosEntraID tbody').on('click', 'tr', function (event) {
    if (!$(event.target).closest('.detalles-usuario').length &&
      !$(event.target).hasClass('dt-control') &&
      !$(event.target).parents('.dt-control').length) {
    }
  });

  $('#tablaUsuariosEntraID tbody').on('dblclick', 'tr', function (event) {
    if (!$(event.target).closest('.detalles-usuario').length &&
      !$(event.target).hasClass('dt-control') &&
      !$(event.target).parents('.dt-control').length) {
      mostrarRegistroEnModal(table, this);
    }
  });
}
function mostrarRegistroEnModal(table, row) {
  const data = table.row(row).data();
  const modalContent = formatearParaModal(data);

  Swal.fire({
    html: modalContent,
    width: '700px',
    showCloseButton: true,
    showConfirmButton: false,
    focusConfirm: false,
    customClass: {
      container: 'user-profile-modal'
    }
  });
}
function formatearParaModal(data) {
  const createdDate = data.createdDateTime ?
    moment.utc(data.createdDateTime).tz("America/Bogota").format('DD/MM/YYYY') : 'No disponible';
  const lastSignIn = formatearUltimaSesion(data.lastSignInDateTime);

  return `
    <div class="user-profile-modal-container">
        <div class="user-header">
            <h2 class="text-center">${data.displayName || 'Nombre no disponible'}</h2>
            <p class="text-center user-email">${data.mail || 'No disponible'}</p>
            <div class="user-meta text-center">
                <span class="user-id">ID: ${data.id || 'No disponible'}</span>
                <span class="user-creation-date"> Creado: ${createdDate}</span>
            </div>
        </div>

        <div class="user-info-grid">
            <div class="info-column">
                <div class="info-card">
                    <h3>Cargo</h3>
                    <p>${data.jobTitle || 'No especificado'}</p>
                </div>

                <div class="info-card">
                    <h3>Oficina</h3>
                    <p>${data.officeLocation || 'No especificado'}</p>
                </div>

                <div class="info-card">
                    <h3>Estado de cuenta</h3>
                    <p>${formatearEstado(data.accountEnabled)}</p>
                </div>
            </div>

            <div class="info-column">
                <div class="info-card">
                    <h3>Última conexión</h3>
                    <div class="last-signin-value">${lastSignIn}</div>
                </div>

                <div class="info-card">
                    <h3>Licencias asignadas</h3>
                    <div class="licenses-container">
                        ${data.assignedLicenses && data.assignedLicenses.length > 0 ?
      licenciaprincipalDestacar(data.assignedLicenses, 'display') :
      '<span class="text-muted">No hay licencias asignadas</span>'}
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;
}
function actualizarPanelUsuario(data) {
  $('.user-fullname').text(data.displayName || 'Nombre no disponible');
  $('.user-email').text(data.mail || 'Correo no disponible');
  $('.user-id').text(`ID: ${data.id || 'No disponible'}`);

  const createdDate = data.createdDateTime ? moment.utc(data.createdDateTime).tz("America/Bogota").format('DD/MM/YYYY') : 'N/A';
  $('.user-creation-date').text(`Creado: ${createdDate}`);

  $('.info-card:eq(0) .info-value').text(data.jobTitle || 'No especificado');
  $('.info-card:eq(1) .info-value').text(data.officeLocation || 'No especificado');
  $('.info-card:eq(2) .info-value').html(formatearEstado(data.accountEnabled));

  $('.info-card:has(h3.info-title:contains("Última conexión")) .info-value')
    .html(formatearUltimaSesion(data.lastSignInDateTime));

  const licensesContainer = $('.licenses-container');
  licensesContainer.empty();

  if (data.assignedLicenses && data.assignedLicenses.length > 0) {
    const licensesHtml = licenciaprincipalDestacar(data.assignedLicenses, 'display');
    licensesContainer.html(licensesHtml);
  } else {
    licensesContainer.html('<span class="text-muted">No hay licencias asignadas</span>');
  }
}
function formatearCorreoConBotonCopiar(correo) {
  return `
    <span class="correo">${correo}</span>
    <button class="btn-copiar" data-correo="${correo}" title="Copiar al portapapeles"
      style="background: none; border: none; cursor: pointer; margin-left: 8px; padding: 0;">
      <img src="static/img/icono_copy.png" class="icono-copiar-personal" alt="Copiar" style="width: 20px; height: 20px;">
    </button>
  `;
}

function inicializarTablaUsuariosEntraID() {
  $.fn.dataTable.moment('DD/MM/YYYY HH:mm:ss');

  if ($.fn.DataTable.isDataTable('#tablaUsuariosEntraID')) {
    $('#tablaUsuariosEntraID').DataTable().destroy();
    $('#tablaUsuariosEntraID tbody').empty();
  }

  let expandedRows = {};

  let columnas = [
    {
      className: 'dt-control',
      orderable: false,
      data: null,
      defaultContent: '<i class="fas fa-plus-circle"></i>',
      width: "3%"
    },
    {
      title: "Fecha de Creación",
      data: "createdDateTime",
      className: "text-center",
      type: "fecha-creacion",
      orderable: true,
      width: "8%",
      orderable: true,
      render: function (data, type, row) {
        if (type === 'display') {
          return formatearFechaCreacion(data);
        }
        if (!data || !esFechaValida(data)) {
          return 0;
        }
        return new Date(data).getTime();
      }
    },
    { title: "Nombre completo", data: "displayName", orderable: true },
    {
      title: "Correo electrónico",
      data: "mail",
      orderable: true,
      render: function (data, type, row) {
        return formatearCorreoConBotonCopiar(data);
      }
    },
    {
      title: "Licencias asignadas",
      data: "assignedLicenses",
      render: licenciaprincipalDestacar,
      orderable: true
    },
    {
      title: "Inicio sesión",
      data: "accountEnabled",
      className: "text-center",
      type: "estado-cuenta",
      render: formatearEstado,
      orderable: true,
      createdCell: function (td, cellData, rowData, row, col) {
        $(td).attr('data-order', cellData === "Habilitado" ? 1 : 0);
      }
    },
    {
      title: "Última Conexión",
      data: "lastSignInDateTime",
      className: "text-center",
      type: "ultima-conexion",
      orderable: true,
      width: "8%",
      render: function (data, type, row) {
        if (type === 'display') {
          return formatearUltimaSesion(data);
        }
        if (!data || !esFechaValida(data)) {
          return 0;
        }
        return new Date(data).getTime();
      }
    },
    {
      title: "Detalles Ocultos",
      data: null,
      render: function (data) {
        return `${data.jobTitle || ""} ${data.officeLocation || ""} ${data.id || ""} ${data.skuIds || ""} ${data.assignedLicenses || ""}`;
      },
      visible: false,
      orderable: false
    }
  ];

  let table = $('#tablaUsuariosEntraID').DataTable(
    ConfiguracionDataTable(BD_UsuariosEntraID, columnas, agregarBotonExpandirTodo)
  );

  $('#tablaUsuariosEntraID tbody').on('click', 'td.dt-control', function () {
    let row = table.row($(this).closest('tr'));
    let rowData = row.data();
    let rowId = rowData.mail;
    toggleDetalles(row, $(this), rowId);
  });

  table.on('draw', function () {
    $('#tablaUsuariosEntraID tbody tr').each(function () {
      let row = table.row(this);
      let rowData = row.data();
      let rowId = rowData ? rowData.mail : null;

      if (rowId && expandedRows[rowId]) {
        row.child(formatDetalles(rowData)).show();
        $(this).find('td.dt-control').html('<i class="fas fa-minus-circle"></i>');
      }
    });
  });

  $('#filtroTabla').on('keyup', function () {
    table.search(this.value).draw();
  });

  function toggleDetalles(row, controlElement, rowId) {
    if (row.child.isShown()) {
      row.child.hide();
      controlElement.html('<i class="fas fa-plus-circle"></i>');
      delete expandedRows[rowId];
    } else {
      row.child(formatDetalles(row.data())).show();
      controlElement.html('<i class="fas fa-minus-circle"></i>');
      expandedRows[rowId] = true;
    }
  }

  let filtroConexion = function (settings, data, dataIndex, rowData) {
    const filtro = filtroUltimaConexion.value;
    const fechaTexto = rowData.lastSignInDateTime;

    if (filtro === '') return true;
    
    if (filtro === 'conSesion') {
        return fechaTexto && fechaTexto !== 'Sin Descargar' && !fechaTexto.includes('No ha iniciado sesión');
    }

    if (filtro === 'sinSesion') {
      return !fechaTexto || fechaTexto === 'Sin Descargar' || fechaTexto.includes('No ha iniciado sesión');
    }

    if (fechaTexto === 'Sin Descargar' || !fechaTexto) {
      return false;
    }

    if (!moment(fechaTexto, moment.ISO_8601, true).isValid()) {
      return false;
    }

    const fecha = moment(fechaTexto);
    const hoy = moment();

    switch (filtro) {
      case 'menos7dias':
        return hoy.diff(fecha, 'days') <= 7;
      case 'entre7y15':
        const dias = hoy.diff(fecha, 'days');
        return dias > 7 && dias <= 15;
      case 'entre15y30':
        return hoy.diff(fecha, 'days') > 15 && hoy.diff(fecha, 'days') <= 30;
      case 'entre1y3meses':
        return hoy.diff(fecha, 'months') >= 1 && hoy.diff(fecha, 'months') < 3;
      case 'entre3y6meses':
        return hoy.diff(fecha, 'months') >= 3 && hoy.diff(fecha, 'months') < 6;
      case 'entre6y12meses':
        return hoy.diff(fecha, 'months') >= 6 && hoy.diff(fecha, 'months') < 12;
      case 'mas1ano':
        return hoy.diff(fecha, 'years') >= 1;
      case 'mas2anos':
        return hoy.diff(fecha, 'years') >= 2;
      default:
        return true;
    }
  };

  filtroConexion._esFiltroUltimaConexion = true;
  $.fn.dataTable.ext.search.push(filtroConexion);

  function agregarBotonExpandirTodo() {
    let header = $('#tablaUsuariosEntraID thead th.dt-control');
    if (!header.find('.expand-all').length) {
      header.html('<i class="fas fa-plus-square expand-all"></i>');

      $('.expand-all').on('click', async function () {
        let icono = $(this);
        let expandiendo = icono.hasClass('fa-plus-square');

        icono
          .removeClass('fa-plus-square fa-minus-square expanded')
          .addClass('fa-sync-alt fa-spin loading')
          .css('color', '#007bff');

        await new Promise(resolve => {
          setTimeout(() => {
            table.rows({ search: 'applied' }).every(function () {
              let row = this;
              let rowData = row.data();
              let rowId = rowData.mail;
              let controlCell = $(row.node()).find('td.dt-control');

              if (expandiendo && !row.child.isShown()) {
                row.child(formatDetalles(row.data())).show();
                controlCell.html('<i class="fas fa-minus-circle"></i>');
                expandedRows[rowId] = true;
              } else if (!expandiendo && row.child.isShown()) {
                row.child.hide();
                controlCell.html('<i class="fas fa-plus-circle"></i>');
                delete expandedRows[rowId];
              }
            });
            resolve();
          }, 100);
        });
        icono
          .removeClass('fa-sync-alt fa-spin loading')
          .addClass(expandiendo ? 'fa-minus-square expanded' : 'fa-plus-square')
          .css('color', expandiendo ? 'red' : '#007bff');
      });
    }
  }

  table.on('length.dt', function (e, settings, len) {
    let expandBtn = $('.expand-all');

    if (len === -1) {
      table.rows().every(function () {
        if (this.child.isShown()) {
          this.child.hide();
          let rowId = this.data().mail;
          let controlCell = $(this.node()).find('td.dt-control');
          controlCell.html('<i class="fas fa-plus-circle"></i>');
          delete expandedRows[rowId];
        }
      });
      expandBtn.addClass('disabled').css({
        'pointer-events': 'none',
        'opacity': '0.5',
        'color': 'gray'
      }).attr('title', 'Desactivado por rendimiento');
    } else {
      expandBtn.removeClass('disabled').css({
        'pointer-events': 'auto',
        'opacity': '1',
        'color': expandBtn.hasClass('expanded') ? 'red' : '#007bff'
      }).removeAttr('title');
    }
  });


$('#tablaUsuariosEntraID').on('click', '.btn-copiar', function (e) {
  e.stopPropagation();
  const $btn = $(this);
  const $img = $btn.find('img');
  const correo = $btn.data('correo');
  const originalSrc = 'static/img/icono_copy.png';
  const checkSrc = 'static/img/icono_check.png';
  const $tempInput = $('<input>');
  $('body').append($tempInput);
  $tempInput.val(correo).select();

  try {
    const successful = document.execCommand('copy');
    if (successful) {
      $img.attr('src', checkSrc);
      setTimeout(() => $img.attr('src', originalSrc), 2000);
    } else {
      console.error('Error al copiar con execCommand');
    }
  } catch (err) {
    console.error('Error al intentar copiar:', err);
  }
  $tempInput.remove();
});
  aplicarFiltroLicencias(table);
  aplicarFiltroInicioSesion(table);
  aplicarFiltroUltimaConexion(table);
  setupTableInteractions();
}

function ConfiguracionDataTable(data, columnas, initCompleteCallback) {
  return {
    data: data,
    columns: columnas,
    order: [[1, 'desc']],
    language: {
      url: 'https://cdn.datatables.net/plug-ins/2.0.2/i18n/es-ES.json'
    },
    initComplete: initCompleteCallback,
    lengthMenu: [[10, 30, 60, 80, 100, -1], ['10', '30', '60', '80', '100', 'Todos']]
  };
}
function formatDetalles(usuario) {
  return `
        <div class="detalles-usuario">
            <div class="detalle-item">
                <i class="icon-cargo fas fa-user-tie"></i>
                <p><strong>Cargo:</strong> <span>${usuario.jobTitle || "No disponible"}</span></p>
            </div>
            
            <div class="detalle-item">
                <i class="icon-oficina fas fa-map-marker-alt"></i>
                <p><strong>Oficina:</strong> <span>${usuario.officeLocation || "No disponible"}</span></p>
            </div>

            <div class="detalle-item">
                <i class="icon-id fas fa-id-card"></i>
                <p><strong>Id del usuario:</strong> <span>${usuario.id || "No disponible"}</span></p>
            </div>

            <div class="detalle-item">
                <i class="icon-id fas fa-toolbox"></i>
                <p><strong>SkuIds licencias:</strong> <span>${usuario.skuIds || "No disponible"}</span></p>
            </div>

        </div>`;
}
function aplicarFiltroLicencias(table) {
  filtroLicencias.addEventListener("change", function () {
    const valorSeleccionado = this.value;

    if (valorSeleccionado === "conLicencia") {
      table.column(7)
        .search("^(?!.*\\bSin Licencia\\b).+", true, false)
        .draw();
    } else if (valorSeleccionado === "sinLicencia") {
      table.column(7)
        .search("\\bSin Licencia\\b", true, false)
        .draw();
    } else {
      table.column(7).search(valorSeleccionado, false, true).draw();
    }
  });

  btnLimpiarLicencias.addEventListener("click", function () {
    filtroLicencias.value = "";
    table.column(7).search("").draw();
  });
}

function aplicarFiltroInicioSesion(table) {
  filtroInicioSesion.addEventListener("change", function () {
    const valorSeleccionado = this.value;
    table.column(5).search(valorSeleccionado).draw();
  });

  btnLimpiarInicioSesion.addEventListener("click", function () {
    filtroInicioSesion.value = "";
    table.column(5).search("").draw();
  });
}

function aplicarFiltroUltimaConexion(table) {
  filtroUltimaConexion.addEventListener('change', function () {
    table.draw();
  });
}

function actualizarDatosUsuarios() {
  let table = $('#tablaUsuariosEntraID').DataTable();
  let expandedRows = [];
  table.rows().every(function () {
    if (this.child.isShown()) {
      expandedRows.push(this.data().mail);
    }
  });

  table.clear().rows.add(BD_UsuariosEntraID).draw(false);
  table.rows().every(function () {
    let row = this;
    if (expandedRows.includes(row.data().mail)) {
      row.child(formatDetalles(row.data())).show();
      $(row.node()).find('td.dt-control').html('<i class="fas fa-minus-circle"></i>');
    }
  });
}
function formatearFechaCreacion(fecha) {
  const estiloBase = `display: inline-flex; align-items: center; justify-content: center; gap: 6px; 
        padding: 4px 4px; border-radius: 4px; font-weight: bold; font-size: 12px; border: 0.3px solid; text-align: center; width: 100%;`;
  if (!fecha || !esFechaValida(fecha)) {
    return `<span style="${estiloBase} background-color: #e2e3e5; color: #6c757d; border-color: #6c757d;">
            <i class="fas fa-ban"></i> No disponible</span>`;
  }
  const fechaCreacion = moment.utc(fecha).tz("America/Bogota");
  const fechaHoraFormateada = fechaCreacion.format("DD/MM/YYYY HH:mm:ss");

  return `<span style="${estiloBase} background-color: #c3e6cb; color: #0b5d1e; border-color: #0b5d1e;">
            <i class="fas fa-calendar-check"></i> ${fechaHoraFormateada}
          </span>`;
}
function formatearUltimaSesion(fecha) {
  const estiloBase = `display: inline-flex; align-items: center; justify-content: center; gap: 6px; 
        padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; border: 0.3px solid; text-align: center; width: 100%;`;
  if (fecha === "Sin Descargar") {
    return `<span style="${estiloBase} background-color: #e2e3e5; color: #6c757d; border-color: #6c757d;">
            <i class="fas fa-download"></i> Sin descargar</span>`;
  }
  if (!fecha || !esFechaValida(fecha)) {
    return `<span style="${estiloBase} background-color: #e2e3e5; color: #6c757d; border-color: #6c757d;">
            <i class="fas fa-user-slash"></i> No ha iniciado sesión</span>`;
  }

  let fechaSesion = moment.utc(fecha).tz("America/Bogota");
  let fechaHoraFormateada = fechaSesion.format('DD/MM/YYYY HH:mm:ss');
  let diasDesdeSesion = moment().tz("America/Bogota").diff(fechaSesion, 'days');

  let icono = "";
  let colorFondo = "";
  let colorTexto = "";
  let colorBorde = "";

  if (diasDesdeSesion < 8) {
    icono = `<i class="fas fa-check-circle"></i>`;
    colorFondo = "#c3e6cb";
    colorTexto = "#0b5d1e";
    colorBorde = "#0b5d1e";
  } else if (diasDesdeSesion <= 30) {
    icono = `<i class="fas fa-exclamation-circle"></i>`;
    colorFondo = "#ffeeba";
    colorTexto = "#856404";
    colorBorde = "#856404";
  } else {
    icono = `<i class="fas fa-times-circle"></i>`;
    colorFondo = "#f8d7da";
    colorTexto = "#721c24";
    colorBorde = "#721c24";
  }

  return `<span style="${estiloBase} background-color: ${colorFondo}; color: ${colorTexto}; border-color: ${colorBorde};">
        ${icono} ${fechaHoraFormateada}
    </span>`;
}
function formatearEstado(estado) {
  const estiloBase = `
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    margin: 1px;
    font-size: 12px;
    border: 0.3px solid;
    width: 100%;
  `;

  let icono = "";
  let colorFondo = "";
  let colorTexto = "";
  let colorBorde = "";

  if (estado === "Habilitado") {
    icono = `<i class="fas fa-check-circle"></i>`;
    colorFondo = "#c3e6cb";
    colorTexto = "#0b5d1e";
    colorBorde = "#0b5d1e";
  } else if (estado === "Bloqueado") {
    icono = `<i class="fas fa-lock"></i>`;
    colorFondo = "#f8d7da";
    colorTexto = "#721c24";
    colorBorde = "#721c24";
  } else {
    icono = `<i class="fas fa-question-circle"></i>`;
    colorFondo = "#e2e3e5";
    colorTexto = "#6c757d";
    colorBorde = "#6c757d";
  }

  return `
    <span style="${estiloBase} background-color: ${colorFondo}; color: ${colorTexto}; border-color: ${colorBorde};">
      ${icono}
      <span>${estado}</span>
    </span>
  `;
}
function licenciaprincipalDestacar(data) {
  if (!data) return "";

  const licenciasPrincipales = Object.values(BD_IdentificadorLicencias)
    .filter(licencia => licencia.LicenciaPrincipal === 1)
    .map(licencia => licencia.NombreLicencia);

  const licenciasDePago = Object.values(BD_IdentificadorLicencias)
    .filter(licencia => licencia.LicenciaDePago === 1)
    .map(licencia => licencia.NombreLicencia);

  const licenciasGratuitas = Object.values(BD_IdentificadorLicencias)
    .filter(licencia => licencia.LicenciaDePago === 0)
    .map(licencia => licencia.NombreLicencia);

  const licencias = data.split(', ');

  let licenciaPrincipal = licencias.find(lic => licenciasPrincipales.includes(lic));
  let licenciasPago = licencias.filter(lic => licenciasDePago.includes(lic) && lic !== licenciaPrincipal);
  let licenciasGratis = licencias.filter(lic => licenciasGratuitas.includes(lic) && lic !== licenciaPrincipal);

  let licenciasNoIdentificadas = licencias.filter(lic =>
    !licenciasPrincipales.includes(lic) &&
    !licenciasDePago.includes(lic) &&
    !licenciasGratuitas.includes(lic) &&
    lic !== licenciaPrincipal &&
    lic !== "Sin Licencia"
  );
  const formatearLicencia = (licencia, tipo) => {
    let clase = "licencia";
    let prefijo = "";

    if (tipo === "pago") {
      clase += " licencia-pago";
      prefijo = `<span class="icono-pago">$</span> `;
    }

    if (tipo === "gratis") {
      clase += " licencia-gratis";
      prefijo = `<span class="icono-gratis"><i class="fas fa-hand-holding-usd"></i></span> `;
    }

    if (tipo === "no-identificada") {
      clase += " licencia-no-identificada";
      prefijo = `<span class="icono-no-identificada">❓</span> `;
    }

    if (tipo === "sin-licencia") {
      clase += " licencia-sin";
      prefijo = `<span class="icono-sin">🚫</span> `;
    }

    if (tipo === "principal") {
      clase += " licencia-principal";
      if (licenciasDePago.includes(licencia)) {
        prefijo = `<span class="icono-pago">$</span> `;
      }
    }

    return `<span class="${clase}">${prefijo}${licencia}</span>`;
  };

  let resultado = [];

  if (licenciaPrincipal) resultado.push(formatearLicencia(licenciaPrincipal, "principal"));
  resultado = resultado.concat(licenciasPago.map(lic => formatearLicencia(lic, "pago")));
  resultado = resultado.concat(licenciasGratis.map(lic => formatearLicencia(lic, "gratis")));
  resultado = resultado.concat(licenciasNoIdentificadas.map(lic => formatearLicencia(lic, "no-identificada")));

  if (licencias.includes("Sin Licencia")) {
    resultado.push(formatearLicencia("Sin Licencia", "sin-licencia"));
  }

  return resultado.join(' ');
}

function esFechaValida(fecha) {
  return moment(fecha, moment.ISO_8601, true).isValid();
}
btnDescargarUltimaSesion?.addEventListener('click', async function () {
  const icon = this.querySelector('i');
  try {
    toggleBotonesOperacion(true, this);
    controlRotationFaDescarga(icon, true);
    await buscarUltimaSesionActualizarUsuariosEntraID();
  } catch (error) {
    console.error('Error al descargar última sesión:', error);
  } finally {
    toggleBotonesOperacion(false);
    controlRotationFaDescarga(icon, false);
  }
});

btnActualizarUsuarios?.addEventListener('click', async function () {
  const icon = this.querySelector('i');
  try {
    toggleBotonesOperacion(true);
    controlRotation(icon, true);
    await buscarActualizarUsuariosEntraID();
  } catch (error) {
    console.error('Error al actualizar usuarios:', error);
  } finally {
    controlRotation(icon, false);
    toggleBotonesOperacion(false);
  }
});
async function buscarActualizarUsuariosEntraID() {
  await buscarUsuariosEntraID(false);
  actualizarDatosUsuarios();
  procesarEstadisticasUsuarios(BD_UsuariosEntraID);
}
async function buscarUltimaSesionActualizarUsuariosEntraID() {
  await buscarUsuariosEntraID(true);
  actualizarDatosUsuarios();
  procesarEstadisticasUsuarios(BD_UsuariosEntraID);
  procesarEstadisticasUsuarios_UltimoInicioSesion(BD_UsuariosEntraID);
  controlarSelectConexion(true);
}
function toggleBotonesOperacion(deshabilitar = true) {
  const btnDescargar = document.querySelector('.btn-DescargarUltimaSesion');
  const btnActualizar = document.querySelector('.btn-ActualizarUsuarios');

  const botones = [btnDescargar, btnActualizar];

  botones.forEach(btn => {
    if (!btn) return;
    if (deshabilitar) {
      btn.disabled = true;
      btn.classList.add('btn-inactivo');
    } else {
      btn.disabled = false;
      btn.classList.remove('btn-inactivo');
    }
  });
}
function controlRotationFaDescarga(icon, activar) {
  if (activar) {
    icon.classList.remove('fa-download');
    icon.classList.add('fa-sync-alt', 'rotating');
  } else {
    icon.classList.remove('fa-sync-alt', 'rotating');
    icon.classList.add('fa-download');
  }
}
document.querySelector('.btn-ExportarExcel').addEventListener('click', function () {
  Swal.fire({
    title: 'Exportando datos',
    html: 'Por favor espere...',
    timerProgressBar: true,
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading()
  });
  setTimeout(() => {
    try {
      exportarAExcelUsuariosLicencias(BD_UsuariosEntraID);
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
  }, 1500);
});
function exportarAExcelUsuariosLicencias(usuarios) {
  const filas = usuarios.map(usuario => {
    const { licenciaPrincipal, otrasLicencias } = obtenerLicencias(usuario.skuIds);
    const usuarioNombre = usuario.mail?.split('@')[0] || '';
    const fechaCreacion = formatearFechaCreacion(usuario.createdDateTime);
    const ultimaConexion = formatearUltimaSesion(usuario.lastSignInDateTime);
    const estadoCuenta = formatearEstado(usuario.accountEnabled);

    return `
            <tr>
                <td>${usuario.id || ''}</td>
                <td>${fechaCreacion}</td>
                <td>${usuario.displayName || ''}</td>
                <td>${usuarioNombre}</td>
                <td>${usuario.mail || ''}</td>
                <td>${usuario.jobTitle || ''}</td>
                <td>${usuario.officeLocation || ''}</td>
                <td>${licenciaPrincipal}</td>
                <td>${otrasLicencias}</td>
                <td>${estadoCuenta}</td>
                <td>${ultimaConexion}</td>
            </tr>
        `;
  }).join('');
  const encabezado = `
        <tr>
            <th>ID del Usuario</th>
            <th>Fecha Creación</th>
            <th>Nombre Completo</th>
            <th>Usuario</th>
            <th>Correo Electrónico</th>
            <th>Cargo</th>
            <th>Oficina</th>
            <th>Licencia Principal</th>
            <th>Otras Licencias</th>
            <th>Inicio de Sesión</th>
            <th>Última Conexión</th>
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
  link.download = `Usuarios_Licencias_${new Date().toISOString().slice(0, 10)}.xls`;
  document.body.appendChild(link);
  link.click();
  setTimeout(() => {
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }, 1500);
}
function obtenerLicencias(skuIdsString) {
  const skuIds = (skuIdsString || '').split(',').map(id => id.trim());
  let licenciaPrincipal = '';
  const otrasLicencias = [];
  skuIds.forEach(skuId => {
    const lic = BD_LicenciasDetallesUnificados.find(l => l.skuId === skuId);

    if (lic) {
      const nombreLicencia = lic.BD_IdentificadorLicencias_NombreLicencia || lic.BD_DetallesLicencias_NombreLicencia;

      if (lic.BD_IdentificadorLicencias_LicenciaPrincipal === 1 && !licenciaPrincipal) {
        licenciaPrincipal = nombreLicencia;
      } else {
        otrasLicencias.push(nombreLicencia);
      }
    }
  });
  return {
    licenciaPrincipal: licenciaPrincipal || 'Sin Licencia Principal',
    otrasLicencias: otrasLicencias.length ? otrasLicencias.join(', ') : 'Ninguna'
  };
}
