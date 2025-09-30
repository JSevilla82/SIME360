async function configuracion() {
  try {
    configurarTabs();
    const tabla = inicializarDataTable();
    configurarEventosEdicion(tabla);
    await cargarYMostrarLicencias(tabla);
    cargarAccesos();
    document.getElementById("contenidoPrincipal_configuracion").style.display = "block";
  } catch (error) {
    mostrarMensaje("error", "Error al iniciar el módulo de configuración");
  }
}

async function cargarYMostrarLicencias(tabla, mostrarCarga = true) {
  const tarea = async () => {
    try {
      
      await Promise.all([
        buscarDetallesLicencias(), 
        buscarDatosIdentificadorLicencias(), 
      ]);

      const datosParaTabla = procesarDatosLicencias(BD_DetallesLicencias, BD_IdentificadorLicencias);
      actualizarTabla(tabla, datosParaTabla);

    } catch (error) {
      mostrarErrorEnTabla(tabla);
      mostrarMensaje("error", `Error al cargar las licencias: ${error.message}`);
    }
  };

  if (mostrarCarga) {
    await mostrarCargaProceso(
      [
        {
          titulo: "Obteniendo datos del servidor",
          icono: "/static/img/servidor.png",
          funcion: tarea,
        },
      ],
      0
    );
  } else {
    await tarea();
  }
}


function configurarTabs() {
  const tabButtons = document.querySelectorAll(".tab-button");

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      tabButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");

      const tabId = button.dataset.tab;
      document.querySelectorAll(".tab-content").forEach((content) => {
        content.classList.remove("active");
      });
      document.getElementById(tabId)?.classList.add("active");
    });
  });
}

function inicializarDataTable() {
  const existeTabla = $.fn.dataTable.isDataTable("#tablaLicencias");
  if (existeTabla) {
    const tablaExistente = $("#tablaLicencias").DataTable();
    tablaExistente.clear().destroy();
    $("#tablaLicencias").empty();
  }

  return $("#tablaLicencias").DataTable({
    language: {
      url: "https://cdn.datatables.net/plug-ins/2.0.2/i18n/es-ES.json",
    },
    responsive: true,
    autoWidth: false,
    pageLength: 100,
    order: [[6, "asc"]],
    columns: [
      { title: "SKU ID", data: "skuId" },
      { title: "Nombre Licencia", data: "nombreLicencia" },
      {
        title: "Nombre Comercial",
        data: "nombreComercial",
        render: function (data, type, row) {
          return formatearLicenciaConEstilo(data, row);
        },
      },
      { title: "Tipo", data: "tipo" },
      { title: "Pago", data: "pago" },
      {
        title: "Opciones",
        data: "opciones",
        orderable: false,
        className: "text-center",
      },
      {
        title: "Orden",
        data: "ordenPersonalizado",
        visible: false,
        searchable: false,
      },
    ],
    createdRow: function (row, data) {
      const claseBase = data.estaConfigurada ? "licencia-configurada" : "licencia-no-configurada";
      $(row).addClass(claseBase);
    },
  });
}

function configurarEventosEdicion(tabla) {
  $("#tablaLicencias").on("click", ".fa-edit, .fa-cog", async function () {
    const fila = $(this).closest("tr");
    const rowData = tabla.row(fila).data();

    if (!rowData) {
      mostrarMensaje("error", "No se pudieron obtener los datos de la licencia");
      return;
    }

    if (!rowData.estaConfigurada && !rowData.datosOriginales) {
      mostrarMensaje("error", "Faltan datos para configurar esta licencia");
      return;
    }

    await mostrarModalEdicion(rowData);
  });

  $("#tablaLicencias").on("click", ".fa-trash-alt", async function () {
    const fila = $(this).closest("tr");
    const rowData = tabla.row(fila).data();

    if (!rowData) {
      mostrarMensaje("error", "No se pudieron obtener los datos de la licencia");
      return;
    }

    await confirmarEliminacionLicencia(rowData);
  });
}

function procesarDatosLicencias(detalles, apiData) {
  // 'detalles' es la lista de licencias de Graph (fuente de verdad)
  // 'apiData' son las licencias configuradas en la BD local.
  const licenciasConfiguradas = apiData.licencias || apiData;

  return detalles
    .filter((detalle) => detalle && (detalle.skuId || detalle.skufd))
    .map((detalle) => {
      const skuId = detalle.skuId || detalle.skufd || "N/A";
      // Busca la configuración local para la licencia actual de Graph
      const licenciaLocal = licenciasConfiguradas[skuId] || null;
      const estaConfigurada = !!licenciaLocal;

      const ordenPersonalizado = estaConfigurada
        ? licenciaLocal.LicenciaPrincipal
          ? 1
          : licenciaLocal.LicenciaDePago
          ? 2
          : 3
        : 0; // Las no configuradas van primero

      return {
        skuId: skuId,
        nombreLicencia: detalle.skuPartNumber || "N/A",
        nombreComercial: estaConfigurada ? licenciaLocal.NombreLicencia : "No configurada",
        tipo: estaConfigurada ? (licenciaLocal.LicenciaPrincipal ? "Principal" : "Secundaria") : "N/A",
        pago: estaConfigurada ? (licenciaLocal.LicenciaDePago ? "De pago" : "Gratuita") : "N/A",
        opciones: estaConfigurada
          ? `
            <i class="fas fa-edit" title="Editar licencia"></i>
            <i class="fas fa-trash-alt text-danger ms-2" title="Eliminar licencia"></i>
          `
          : '<i class="fas fa-cog" title="Configurar licencia"></i>',
        estaConfigurada,
        datosOriginales: detalle,
        datosAPI: licenciaLocal || null,
        ordenPersonalizado,
      };
    });
}


function actualizarTabla(tabla, datos) {
  const datosValidados = datos.map((item) => {
    if (typeof item.ordenPersonalizado === "undefined") {
      item.ordenPersonalizado = item.estaConfigurada ? 1 : 0;
    }
    return item;
  });

  tabla.clear();
  tabla.rows.add(datosValidados);
  tabla.draw();

  if (datosValidados.length === 0) {
    mostrarErrorEnTabla(tabla);
  }
}

function mostrarErrorEnTabla(tabla) {
  tabla.clear();
  tabla.row
    .add({
      skuId: "Error",
      nombreLicencia: "",
      nombreComercial: "No se pudieron cargar los datos",
      tipo: "",
      pago: "",
      opciones: "",
      ordenPersonalizado: 99,
      estaConfigurada: false,
    })
    .draw();
}

async function mostrarModalEdicion(rowData) {
  const esNueva = !rowData.estaConfigurada;
  const datosLicencia = esNueva ? rowData.datosOriginales : rowData.datosAPI;

  const { value: formValues } = await Swal.fire({
    title: esNueva ? "Configurar Nueva Licencia" : "Editar Licencia",
    html: generarFormularioModal(rowData, datosLicencia),
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: "Guardar",
    cancelButtonText: "Cancelar",
    showCloseButton: true,
    customClass: {
      popup: "licencia-modal-popup",
      htmlContainer: "licencia-modal-html",
    },
    didOpen: () => configurarEventosModal(),
    preConfirm: () => validarFormularioModal(),
  });

  if (formValues) {
    await guardarLicencia(
      {
        ...formValues,
        LicenciaSkuId: rowData.skuId,
      },
      esNueva
    );
  }
}

function generarFormularioModal(rowData, datosLicencia) {
  const esNueva = !rowData.estaConfigurada;
  const esPrincipal = datosLicencia?.LicenciaPrincipal || false;
  const esDePago = datosLicencia?.LicenciaDePago || false;
  const nombreComercial = datosLicencia?.NombreLicencia || "";

  return `
    <div class="modal-body-custom">
      <div class="mb-3">
        <label class="form-label">SKU ID</label>
        <input type="text" class="form-control" value="${rowData.skuId}" disabled>
      </div>

      <div class="mb-3">
        <label class="form-label">Nombre Técnico</label>
        <input type="text" class="form-control" value="${rowData.nombreLicencia}" disabled>
      </div>

      <div class="mb-3">
        <label class="form-label">Nombre Comercial *</label>
        <input id="nombreComercial" class="form-control" 
               value="${nombreComercial}" required>
      </div>

      <div class="mb-3">
        <label class="form-label">Tipo de Licencia</label>
        <select id="tipoLicencia" class="form-select">
          <option value="" ${esNueva ? "selected" : ""} disabled>Seleccione tipo</option>
          <option value="true" ${!esNueva && esPrincipal ? "selected" : ""}>Principal</option>
          <option value="false" ${!esNueva && !esPrincipal ? "selected" : ""}>Secundaria</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Tipo de Pago</label>
        <select id="pagoLicencia" class="form-select" ${esPrincipal ? "disabled" : ""}>
          <option value="" ${esNueva || (!esPrincipal && !esDePago) ? "selected" : ""} disabled>Seleccione pago</option>
          <option value="true" ${!esNueva && !esPrincipal && esDePago ? "selected" : ""}>De pago</option>
          <option value="false" ${!esNueva && !esPrincipal && !esDePago ? "selected" : ""}>Gratuita</option>
        </select>
      </div>
    </div>
  `;
}

function configurarEventosModal() {
  const tipoSelect = document.getElementById("tipoLicencia");
  const pagoSelect = document.getElementById("pagoLicencia");

  if (tipoSelect && pagoSelect) {
    tipoSelect.addEventListener("change", (e) => {
      const esPrincipal = e.target.value === "true";
      pagoSelect.disabled = esPrincipal;
      if (esPrincipal) {
        pagoSelect.value = "";
      }
    });
  }
}

function validarFormularioModal() {
  const nombreComercial = document.getElementById("nombreComercial")?.value.trim();
  const tipoLicencia = document.getElementById("tipoLicencia")?.value;
  const pagoLicencia = document.getElementById("pagoLicencia")?.value;

  if (!nombreComercial) {
    Swal.showValidationMessage("El nombre comercial es requerido");
    return false;
  }

  if (!tipoLicencia) {
    Swal.showValidationMessage("Debe seleccionar el tipo de licencia");
    return false;
  }

  const esSecundaria = tipoLicencia === "false";
  if (esSecundaria && !pagoLicencia) {
    Swal.showValidationMessage("Debe seleccionar el tipo de pago para licencias secundarias");
    return false;
  }

  return {
    NombreLicencia: nombreComercial,
    LicenciaPrincipal: tipoLicencia === "true",
    LicenciaDePago: tipoLicencia === "true" ? true : pagoLicencia === "true",
  };
}

async function guardarLicencia(datos, esNueva) {
  try {
    const resourceKey = "gestionarLicencia"; 
    const method = esNueva ? "POST" : "PUT";
    const options = {
      method: method,
      body: datos,
      esNueva: esNueva, 
      id: datos.LicenciaSkuId 
    };

    const resultado = await consultarRecurso(resourceKey, options);

    if ([200, 201].includes(resultado.status)) {
      mostrarMensaje("success", `Licencia ${esNueva ? "configurada" : "actualizada"} correctamente`);
      for (let key in BD_IdentificadorLicencias) delete BD_IdentificadorLicencias[key];
      const tabla = $("#tablaLicencias").DataTable();
      await cargarYMostrarLicencias(tabla, false);
    } else {
      throw new Error(resultado.error || "Error al guardar");
    }
  } catch (error) {
    mostrarMensaje("error", `Error al ${esNueva ? "configurar" : "actualizar"} licencia: ${error.message}`);
  }
}

async function confirmarEliminacionLicencia(rowData) {
  const confirmacion = await Swal.fire({
    title: "¿Eliminar licencia?",
    text: `¿Está seguro de eliminar la configuración de la licencia: ${rowData.nombreComercial}?`,
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar",
    confirmButtonColor: "#d33",
  });

  if (confirmacion.isConfirmed) {
    try {
      const tabla = $("#tablaLicencias").DataTable();
      
      const resultado = await consultarRecurso("gestionarLicencia", {
        method: "DELETE",
        id: rowData.skuId,
      });

      if (resultado.status === 200) {
        for (let key in BD_IdentificadorLicencias) delete BD_IdentificadorLicencias[key];
        mostrarMensaje("success", "Licencia eliminada correctamente");
        await cargarYMostrarLicencias(tabla, false);
      } else {
        throw new Error(resultado.error || "No se pudo eliminar");
      }
    } catch (error) {
      mostrarMensaje("error", `Error al eliminar la licencia: ${error.message}`);
    }
  }
}

function mostrarMensaje(tipo, mensaje) {
  const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.onmouseenter = Swal.stopTimer;
      toast.onmouseleave = Swal.resumeTimer;
    },
  });

  Toast.fire({
    icon: tipo,
    title: mensaje,
    background: tipo === "error" ? "#ffebee" : "#e8f5e9",
  });
}

document.getElementById("btnCancelarAcceso").addEventListener("click", cancelarBusqueda);
document.getElementById("btnAutorizarAcceso").addEventListener("click", autorizarAcceso);

async function buscarUsuarioPorCorreo() {
  const correoInput = document.getElementById("buscarCorreoAcceso");
  const correo = correoInput.value.trim();
  const buscarBtn = document.querySelector("#acceso .busqueda-acceso button");

  if (!correo) {
    mostrarMensaje("error", "Por favor ingrese un correo válido");
    return;
  }

  try {
    if (!buscarBtn._originalText) {
      buscarBtn._originalText = buscarBtn.textContent;
    }

    buscarBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Buscando...';
    buscarBtn.disabled = true;

    const usuario = await consultarRecurso("usuarioPorCorreo", { correo: correo });

    document.getElementById("campoNombreAcceso").value = usuario.nombreCompleto || "";
    document.getElementById("campoCorreoAcceso").value = usuario.correo || "";
    document.getElementById("campoOficinaAcceso").value = usuario.oficina || "";
    document.getElementById("campoCargoAcceso").value = usuario.cargo || "";
    document.getElementById("campoEstadoAcceso").value = usuario.estadoCuenta || "";

    const jefe = usuario.jefe || {};
    document.getElementById("campoJefeNombreAcceso").value = jefe.nombreCompleto || "";
    document.getElementById("campoJefeCorreoAcceso").value = jefe.correo || "";
    document.getElementById("campoJefeCargoAcceso").value = jefe.cargo || "";

    mostrarMensaje("success", "Usuario encontrado correctamente");

    document.getElementById("btnCancelarAcceso").disabled = false;
    document.getElementById("btnAutorizarAcceso").disabled = false;
  } catch (err) {

    document.querySelectorAll("#acceso .campo-acceso input").forEach((input) => (input.value = ""));

    mostrarMensaje("error", err.message || "No se pudo encontrar el usuario. Verifique el correo.");

    document.getElementById("btnCancelarAcceso").disabled = true;
    document.getElementById("btnAutorizarAcceso").disabled = true;
  } finally {
    if (buscarBtn._originalText) {
      buscarBtn.textContent = buscarBtn._originalText;
    } else {
      buscarBtn.textContent = "Buscar";
    }
    buscarBtn.disabled = false;
  }
}
function cancelarBusqueda() {
  document.getElementById("buscarCorreoAcceso").value = "";
  document.querySelectorAll("#acceso .campo-acceso input").forEach((input) => (input.value = ""));
  document.getElementById("btnCancelarAcceso").disabled = true;
  document.getElementById("btnAutorizarAcceso").disabled = true;
}

async function autorizarAcceso() {
  const nombre = document.getElementById("campoNombreAcceso").value;
  const correo = document.getElementById("campoCorreoAcceso").value;

  if (!nombre || !correo) {
    Swal.fire({
      title: "Error",
      text: "Primero busque un usuario válido.",
      icon: "error",
      timer: 2500,
      showConfirmButton: false,
    });
    return;
  }

  await mostrarCargaProcesoAnimada("Realizando verificaciones de seguridad", "/static/img/servidor_verificando.png", 0);
  await new Promise((resolve) => setTimeout(resolve, 1000));

  let result;
  try {
    result = await consultarRecurso("autorizarAcceso", {
      method: "POST",
      body: { correo },
      credentials: "include",
    });

    Swal.close();
    await Swal.fire({
      title: "Autorización exitosa",
      text: result.success || "Acceso autorizado correctamente",
      icon: "success",
      timer: 2500,
      showConfirmButton: false,
    });

  } catch (error) {
    Swal.close();
    if (error.status === 409) {
      Swal.fire({
        title: "Usuario ya autorizado",
        text: error.message || "Este usuario ya fue autorizado anteriormente.",
        icon: "info",
        timer: 3000,
        showConfirmButton: false,
      });
    } else {
      Swal.fire({
        title: "Error",
        text: error.message || "No se pudo conectar al servidor o hubo un error al autorizar el acceso.",
        icon: "error",
        timer: 3500,
        showConfirmButton: false,
      });
    }
  } finally {
    cancelarBusqueda(); 
    cargarAccesos();   
  }
}

async function cargarAccesos() {
  const tbody = document.querySelector("#tabla-accesos tbody");
  tbody.innerHTML = ""; 

  try {
    const data = await consultarRecurso("listaAccesos");

    data.forEach((registro) => {
      const fila = document.createElement("tr");
      const estaActivo = registro.estado === "Activo";
      const claseEstado = estaActivo ? "toggle-activo" : "toggle-inactivo";
      const textoEstado = estaActivo ? "Activo" : "Inactivo";

      fila.innerHTML = `
        <td>${registro.fecha_autorizacion}</td>
        <td>${registro.usuario}</td>
        <td>${registro.correo}</td>
        <td>
          <button class="toggle-switch ${claseEstado}" data-correo="${registro.correo}">
            ${textoEstado}
          </button>
        </td>
      `;
      tbody.appendChild(fila);
    });

    document.querySelectorAll(".toggle-switch").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const correo = btn.getAttribute("data-correo");

        try {
          const result = await consultarRecurso("toggleEstadoAcceso", {
            method: "POST",
            body: { correo },
          });

          if (result.success) {
            const fila = btn.closest("tr");
            const nombreUsuario = fila.querySelector("td:nth-child(2)").textContent;
            const nuevoEstado = result.nuevo_estado;
            mostrarMensaje("success", `El estado de ${nombreUsuario} se cambió a ${nuevoEstado}.`);
            cargarAccesos(); 
          } else {
             mostrarMensaje("error", result.error || "No se pudo cambiar el estado.");
          }
        } catch (error) {
           mostrarMensaje("error", error.message || "Error de conexión al cambiar el estado.");
        }
      });
    });
  } catch (error) {
     mostrarMensaje("error", "No se pudieron cargar los registros de acceso.");
  }
}