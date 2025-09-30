let BD_UsuariosEntraID = [],
  BD_IdentificadorLicencias = [],
  BD_DetallesLicencias = [],
  BD_LicenciasDetallesUnificados = [],
  BD_LicenciasDetallesUnificadosExtendido = [];

const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');


function activarFiltroConLimpiar(selector) {
  
  const filtro = document.querySelector(selector);

  if (!filtro) return;

  const btnLimpiar = document.createElement("button");
  btnLimpiar.className = "btn-limpiar";
  btnLimpiar.innerText = "▼"; 
  btnLimpiar.title = "Quitar filtro";

  const contenedor = document.createElement("div");
  contenedor.className = "contenedorFiltro";
  filtro.parentNode.insertBefore(contenedor, filtro);
  contenedor.appendChild(filtro);
  contenedor.appendChild(btnLimpiar);

  btnLimpiar.style.display = "block";

  filtro.addEventListener("change", function () {
    btnLimpiar.innerText = filtro.value ? "❌" : "▼";
  });

  btnLimpiar.addEventListener("click", function () {
    filtro.selectedIndex = 0;
    btnLimpiar.innerText = "▼";
    filtro.dispatchEvent(new Event("change"));
  });
}

function aplicarBordeSiTieneValor(selectElement) {
  if (selectElement.value) {
    selectElement.classList.add('select-con-valor');
  } else {
    selectElement.classList.remove('select-con-valor');
  }

  selectElement.addEventListener('change', function () {
    if (this.value) {
      this.classList.add('select-con-valor');
    } else {
      this.classList.remove('select-con-valor');
    }
  });
}


async function cargarDatosLicenciamiento(mostrarCarga = true) {
  const tarea = async () => {
    const promesas = [];

    const debeDescargarDetalles = BD_DetallesLicencias.length === 0;
    const debeDescargarIdentificadores = Object.keys(BD_IdentificadorLicencias).length === 0;
    const debeDescargarUsuarios = BD_UsuariosEntraID.length === 0;

    if (debeDescargarDetalles) {
      promesas.push(buscarDetallesLicencias());
    }
    if (debeDescargarIdentificadores) {
      promesas.push(buscarDatosIdentificadorLicencias());
    }
    if (debeDescargarUsuarios) {
      promesas.push(buscarUsuariosEntraID());
    }

    if (promesas.length > 0) {
      await Promise.all(promesas);
    }
    if (BD_DetallesLicencias.length > 0) {

      BD_LicenciasDetallesUnificados = [];
      BD_LicenciasDetallesUnificadosExtendido = [];

      consolidarInformacionLicenciasUnicas();
      consolidarInformacionLicenciasExtendido();
    } else {
      console.warn("No hay datos de BD_DetallesLicencias para consolidar.");
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

async function consultarRecurso(resourceKey, options = {}) {
  const recursos = {
    "licenciasDisponibles": "/api/licenciasDisponibles",
    "licenciasConocidas": "/api/licenciasConocidas",
    "informeSharePointSitios": "/api/informe/sharepoint_uso/",
    "usuariosEntraID": "/api/",
    "gestionarLicencia": "/api/licencias",
    "usuarioPorCorreo": "/api/usuario",
    "autorizarAcceso": "/api/autorizar",
    "listaAccesos": "/api/accesos",
    "toggleEstadoAcceso": "/api/accesos/toggle-estado",
    "informeTeams": "/api/informe/teams_actividad/",
    "informeOneDrive": "/api/informe/onedrive/",
    "informeOutlook": "/api/informe/outlook/",
    "informeSharePointActividad": "/api/informe/sharepoint_actividad/",
    "sitiosSharePoint": "/api/sitiosSharePoint",
  };

  let url = recursos[resourceKey];
  if (!url) {
    throw new Error(`Recurso '${resourceKey}' no definido.`);
  }

  if (resourceKey === "informeSharePointSitios" && options.dias) {
    url += options.dias;
  } else if (resourceKey === "usuariosEntraID") {
    const endpointUsuario = options.consultaConSignIn ? "usuariosMiembrosActividad" : "usuariosMiembros";
    url += endpointUsuario;
  } else if (resourceKey === "gestionarLicencia") {

    if ((options.method === "PUT" || options.method === "DELETE") && options.id) {
      url += `/${options.id}`;
    }
  } else if (resourceKey === "usuarioPorCorreo" && options.correo) {
    url += `?correo=${encodeURIComponent(options.correo)}`;
  } else if (
    (resourceKey === "informeTeams" ||
      resourceKey === "informeOneDrive" ||
      resourceKey === "informeOutlook" ||
      resourceKey === "informeSharePointActividad") &&
    options.periodo
  ) {
    url += options.periodo;
  }

  const fetchOptions = {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    credentials: options.credentials || 'same-origin'
  };

  const metodoHttp = fetchOptions.method.toUpperCase();
  if (!['GET', 'HEAD', 'OPTIONS', 'TRACE'].includes(metodoHttp) && csrfToken) {
    fetchOptions.headers['X-CSRFToken'] = csrfToken;
  }

  if (options.body) {
    fetchOptions.body = JSON.stringify(options.body);
  }

  try {
    const respuesta = await fetch(url, fetchOptions);
    if (!respuesta.ok) {
      let errorData = await respuesta.json().catch(() => ({}));
      const errorMessage = errorData.error || `Error HTTP: ${respuesta.status} ${respuesta.statusText}`;
      const error = new Error(errorMessage);
      error.status = respuesta.status;
      throw error;
    }
    // Si la respuesta no tiene cuerpo (ej. en un DELETE exitoso), devuelve un objeto de éxito.
    if (respuesta.status === 204 || respuesta.headers.get("content-length") === "0") {
      return { success: true, status: respuesta.status };
    }
    return await respuesta.json();
  } catch (error) {
    console.error(`Error en la consulta del recurso '${resourceKey}':`, error);
    throw error;
  }
}


/*-----------------------------------------------------------------------------------------------------------*/

function formatearLicenciaConEstilo(nombreLicencia) {
  if (!nombreLicencia) return "";

  const licenciaEncontrada = Object.values(BD_IdentificadorLicencias || {})
    .find(lic => lic.NombreLicencia === nombreLicencia);

  let clase = "licencia";
  let prefijo = "";

  if (!licenciaEncontrada) {
    clase += " licencia-no-identificada";
    prefijo = `<span class="icono-no-identificada" title="Licencia no registrada">❓</span> `;
  } else if (licenciaEncontrada.LicenciaPrincipal === 1) {
    clase += " licencia-principal";
    if (licenciaEncontrada.LicenciaDePago === 1) {
      prefijo = `<span class="icono-pago" title="Licencia de pago">$</span> `;
    }
  } else if (licenciaEncontrada.LicenciaDePago === 1) {
    clase += " licencia-pago";
    prefijo = `<span class="icono-pago" title="Licencia de pago">$</span> `;
  } else {
    clase += " licencia-gratis";
    prefijo = `<span class="icono-gratis" title="Licencia gratuita">
                  <i class="fas fa-hand-holding-usd"></i></span> `;
  }

  return `<span class="${clase}">${prefijo}${nombreLicencia}</span>`;
}



async function procesarInformeSitiosSharePoint() {
  try {
    const resultado = await consultarRecurso("informeSharePointSitios", { dias: 7 });
    if (resultado.error || !Array.isArray(resultado.datos)) {
      console.error("No se pudo obtener el informe de uso de SharePoint:", resultado.error);
      return;
    }
    BD_InformeSitioSharePoint = resultado.datos;
  } catch (error) {
    console.error("Error al procesar el informe de SharePoint:", error);
  }
}

function formatearFechaDDMMYYYY(fechaStr) {
  if (!fechaStr) return "";

  const fecha = moment(fechaStr, ["DD/MM/YYYY", "YYYY-MM-DD", moment.ISO_8601], true);

  return fecha.isValid() ? fecha.format("DD-MM-YYYY") : fechaStr;
}

function convertirBytesAGB(bytes) {
  const numeroBytes = Number(bytes);

  if (isNaN(numeroBytes) || numeroBytes < 0) {
    return "0.00 GB";
  }

  const gb = numeroBytes / 1024 ** 3;
  const resultado = gb < 0.01 ? 0 : gb;

  return resultado.toFixed(2) + " GB";
}

function convertirAGB(valorTexto) {
  if (!valorTexto || typeof valorTexto !== "string") return 0;

  const valor = parseFloat(valorTexto);
  return isNaN(valor) ? 0 : valor;
}

function formatearAlmacenamiento(valor) {
  const [usadoTexto, totalTexto] = valor.split("/").map((v) => v.trim());
  const usadoGB = convertirAGB(usadoTexto);
  const totalGB = convertirAGB(totalTexto);

  let porcentaje = 0;
  if (totalGB > 0) {
    porcentaje = (usadoGB / totalGB) * 100;
  }

  let icono = "",
    colorFondo = "",
    colorTexto = "",
    colorBorde = "",
    colorBarra = "";

  if (usadoGB === 0 && totalGB === 0) {
    icono = `<i class="fas fa-minus-circle"></i>`;
    colorFondo = "#e2e3e5";
    colorTexto = "#6c757d";
    colorBorde = "#6c757d";
    colorBarra = "#adb5bd";
  } else if (porcentaje < 50) {
    icono = `<i class="fas fa-check-circle"></i>`;
    colorFondo = "#c3e6cb";
    colorTexto = "#0b5d1e";
    colorBorde = "#0b5d1e";
    colorBarra = "#0b5d1e";
  } else if (porcentaje <= 80) {
    icono = `<i class="fas fa-exclamation-circle"></i>`;
    colorFondo = "#ffeeba";
    colorTexto = "#8a6d3b"; // Cambié el amarillo a un tono más oscuro
    colorBorde = "#8a6d3b"; // Cambié el borde a un tono más oscuro
    colorBarra = "#ffc107";
  } else {
    icono = `<i class="fas fa-times-circle"></i>`;
    colorFondo = "#f8d7da";
    colorTexto = "#721c24";
    colorBorde = "#721c24";
    colorBarra = "#dc3545";
  }

  const usadoFormatted = usadoGB.toFixed(2);
  const totalFormatted = totalGB.toFixed(2);

  return `
        <div class="almacenamiento-box" style="
            background-color: ${colorFondo};
            color: ${colorTexto};
            border-color: ${colorBorde};
        ">
            <div class="almacenamiento-contenido">
                ${icono}
                <span>${usadoFormatted} GB / ${totalFormatted} GB</span>
            </div>
            <div class="almacenamiento-barra-fondo">
                <div class="almacenamiento-barra-uso" style="
                    width: ${porcentaje}%;
                    background-color: ${colorBarra};
                    border-bottom-right-radius: ${porcentaje === 100 ? "5px" : "0"};
                "></div>
            </div>
        </div>
    `;
}

async function buscarUsuariosEntraID(consultaConSignIn = false) {
  try {

    const datosUsuarios = await consultarRecurso("usuariosEntraID", { consultaConSignIn });

    if (datosUsuarios) {
      if (!consultaConSignIn) {
        let estabaVacio = BD_UsuariosEntraID.length === 0;
        BD_UsuariosEntraID = datosUsuarios.map((usuario) => {
          let usuarioExistente = BD_UsuariosEntraID.find((u) => u.id === usuario.id);
          return {
            id: usuario.id || "-",
            displayName: usuario.displayName || "",
            mail: usuario.userPrincipalName || usuario.mail || "",
            jobTitle: usuario.jobTitle || "",
            // Asegúrate de que obtenerNombreLicencia esté disponible en este scope
            assignedLicenses: obtenerNombreLicencia(usuario.assignedLicenses),
            skuIds: usuario.assignedLicenses?.map((lic) => lic.skuId).join(", ") || "",
            officeLocation: usuario.officeLocation || "",
            accountEnabled: usuario.accountEnabled ? "Habilitado" : "Bloqueado",
            createdDateTime: usuario.createdDateTime,
            lastSignInDateTime:
              usuarioExistente?.lastSignInDateTime ??
              (estabaVacio ? "Sin Descargar" : usuario.lastSignInDateTime || ""),
          };
        });
      } else {
        datosUsuarios.forEach(({ id, signInActivity }) => {
          let usuarioLocal = BD_UsuariosEntraID.find((user) => user.id === id);
          if (usuarioLocal) {
            if (!usuarioLocal.lastSignInDateTime || usuarioLocal.lastSignInDateTime === "Sin Descargar") {
              usuarioLocal.lastSignInDateTime = signInActivity?.lastSignInDateTime || "";
            }
          }
        });
      }
    }
  } catch (error) {
    console.error(`Error al procesar usuarios de Entra ID:`, error);
  }
}

async function buscarDetallesLicencias() {
  try {
    BD_DetallesLicencias = await consultarRecurso("licenciasDisponibles");
  } catch (error) {
    console.error("Error cargando licencias disponibles:", error);
  }
}

async function buscarDatosIdentificadorLicencias() {
  try {
    BD_IdentificadorLicencias = await consultarRecurso("licenciasConocidas");
  } catch (error) {
    console.error("Error cargando licencias conocidas:", error);
  }
}

function obtenerNombreLicencia(assignedLicenses) {
  if (!assignedLicenses?.length) return "Sin Licencia";

  let licenciasPrincipales = [];
  let otrasLicencias = [];

  assignedLicenses.forEach((license) => {
    const skuId = license.skuId;

    let licenciaInfo = BD_IdentificadorLicencias[skuId];
    let licenciaNombre = licenciaInfo?.NombreLicencia;

    if (!licenciaNombre) {
      licenciaNombre = BD_DetallesLicencias.find((lic) => lic.skuId === skuId)?.skuPartNumber;
    }

    licenciaNombre = licenciaNombre || "Licencia sin Identificar";

    if (licenciaInfo?.LicenciaPrincipal === 1) {
      licenciasPrincipales.push(licenciaNombre);
    } else {
      otrasLicencias.push(licenciaNombre);
    }
  });

  return [...licenciasPrincipales, ...otrasLicencias].join(", ");
}

function consolidarInformacionLicenciasUnicas() {
  const skusUnicos = new Set();

  BD_UsuariosEntraID.forEach((usuario) => {
    if (usuario.skuIds) {
      usuario.skuIds.split(",").forEach((sku) => skusUnicos.add(sku.trim()));
    }
  });

  const detallesLicenciasMap = new Map(BD_DetallesLicencias.map((item) => [item.skuId, item]));

  BD_LicenciasDetallesUnificados = Array.from(skusUnicos).map((skuId) => {
    const infoLicencia = {
      skuId: skuId,
      BD_IdentificadorLicencias_NombreLicencia: BD_IdentificadorLicencias[skuId]?.NombreLicencia || null,
      BD_IdentificadorLicencias_LicenciaDePago: BD_IdentificadorLicencias[skuId]?.LicenciaDePago || null,
      BD_IdentificadorLicencias_LicenciaPrincipal: BD_IdentificadorLicencias[skuId]?.LicenciaPrincipal || null,
      BD_DetallesLicencias_NombreLicencia: detallesLicenciasMap.get(skuId)?.skuPartNumber || null,
    };
    return infoLicencia;
  });
}

function consolidarInformacionLicenciasExtendido() {
  BD_DetallesLicencias.forEach((licencia) => {
    const skuId = licencia.skuId;
    const skuPartNumber = licencia.skuPartNumber || null;
    const compradas = licencia.prepaidUnits?.enabled || 0;
    const vencidas = licencia.prepaidUnits?.warning || 0;

    let asignadas = 0;

    BD_UsuariosEntraID.forEach((usuario) => {
      if (usuario.skuIds) {
        const listaSku = usuario.skuIds.split(",").map((s) => s.trim());
        if (listaSku.includes(skuId)) {
          asignadas++;
        }
      }
    });

    const disponibles = compradas + vencidas - asignadas;

    BD_LicenciasDetallesUnificadosExtendido.push({
      skuId: skuId,
      BD_IdentificadorLicencias_NombreLicencia: BD_IdentificadorLicencias[skuId]?.NombreLicencia || null,
      BD_IdentificadorLicencias_LicenciaDePago: BD_IdentificadorLicencias[skuId]?.LicenciaDePago || null,
      BD_IdentificadorLicencias_LicenciaPrincipal: BD_IdentificadorLicencias[skuId]?.LicenciaPrincipal || null,
      BD_DetallesLicencias_NombreLicencia: skuPartNumber,
      LicenciasCompradas: compradas,
      LicenciasVencidas: vencidas,
      LicenciasAsignadas: asignadas,
      LicenciasDisponibles: disponibles,
    });
  });
}

function obtenerDatosLicencias(tipo) {
  return BD_LicenciasDetallesUnificadosExtendido.filter((lic) => {
    const nombreComercial = lic.BD_IdentificadorLicencias_NombreLicencia;
    const esDePago = lic.BD_IdentificadorLicencias_LicenciaDePago === 1;

    if (tipo === "microsoft365") {
      return esDePago;
    } else if (tipo === "freeTrial") {
      return !esDePago && nombreComercial && nombreComercial.trim() !== "" && nombreComercial !== "No disponible";
    } else if (tipo === "sinCategorizar") {
      return !nombreComercial || nombreComercial.trim() === "" || nombreComercial === "No disponible";
    }

    return false;
  }).map((lic) => ({
    nombreLicencia: lic.BD_DetallesLicencias_NombreLicencia || "No especificado",
    nombreComercial: lic.BD_IdentificadorLicencias_NombreLicencia || "No especificado",
    licenciaPrincipal: lic.BD_IdentificadorLicencias_LicenciaPrincipal === 1 ? "Sí" : "No",
    esDePago: lic.BD_IdentificadorLicencias_LicenciaDePago === 1 ? "Sí" : "No",
    skuPartNumber: lic.skuId,
    compradas: lic.LicenciasCompradas,
    vencidas: lic.LicenciasVencidas,
    asignadas: lic.LicenciasAsignadas,
    disponibles: lic.LicenciasDisponibles,
  }));
}

function formatearUsoPorcentaje(porcentajeTexto) {
  const porcentaje = parseFloat(porcentajeTexto.replace("%", "").trim());

  let colorFondo = "",
    colorTexto = "",
    colorBorde = "",
    contenido = "";

  if (porcentaje > 100) {
    // Excedido - rojo oscuro
    colorFondo = "#f5c6cb";
    colorTexto = "#721c24";
    colorBorde = "#dc3545";
    contenido = `${porcentaje}% ¡Excedido!`;
  } else if (porcentaje >= 95) {
    // Rojo
    colorFondo = "#f8d7da";
    colorTexto = "#721c24";
    colorBorde = "#721c24";
    contenido = `${porcentaje}%`;
  } else if (porcentaje >= 85) {
    // Amarillo
    colorFondo = "#ffeeba";
    colorTexto = "#544324";
    colorBorde = "#8a6d3b";
    contenido = `${porcentaje}%`;
  } else {
    // Verde
    colorFondo = "#c3e6cb";
    colorTexto = "#0b5d1e";
    colorBorde = "#0b5d1e";
    contenido = `${porcentaje}%`;
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
            min-width: 60px;
        ">
            ${contenido}
        </div>
    `;
}

function formatearEspacioGB(valor) {
  let colorFondo = "",
    colorTexto = "",
    colorBorde = "";

  if (valor < 100) {
    colorFondo = "#c3e6cb";
    colorTexto = "#0b5d1e";
    colorBorde = "#0b5d1e";
  } else if (valor >= 100 && valor <= 300) {
    colorFondo = "#ffeeba";
    colorTexto = "#856404";
    colorBorde = "#ffc107";
  } else {
    colorFondo = "#f8d7da";
    colorTexto = "#721c24";
    colorBorde = "#dc3545";
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
            min-width: 80px;
        ">
            ${valor.toFixed(2)}
        </div>
    `;
}

// Botón: Exportar a Excel
const btnExportarExcel = document.querySelector(".btn-ExportarExcel");

/*--------------- Funciones para mostrar las alertas de sweetalert2----------------*/

function mostrarAlerta({ titulo = "Alerta", texto = "", icono = "info", mostrarBoton = true, tiempo = null }) {
  Swal.fire({
    title: titulo,
    text: texto,
    icon: icono,
    showConfirmButton: mostrarBoton,
    timer: tiempo,
    confirmButtonColor: "#0086CB",
    confirmButtonText: "Aceptar",
  });
}

async function mostrarAlertaConfirmacion({
  titulo = "¿Estás seguro?",
  mensaje = "Esta acción no se puede deshacer.",
  icono = "warning",
  textoConfirmar = "Sí, continuar",
  textoCancelar = "Cancelar",
}) {
  return Swal.fire({
    title: titulo,
    html: mensaje,
    icon: icono,
    showCancelButton: true,
    confirmButtonText: textoConfirmar,
    cancelButtonText: textoCancelar,
    reverseButtons: true,
  });
}

btnExportarExcel?.addEventListener("click", function () {
  Swal.fire({
    title: "Funcionalidad en desarrollo",
    text: "Esta opción estará disponible próximamente. Por favor, inténtelo más adelante.",
    icon: "info",
    confirmButtonColor: "#0086CB",
    confirmButtonText: "Aceptar",
  });
});

function controlRotation(iconElement, shouldRotate) {
  if (shouldRotate) {
    iconElement.classList.add("rotating");
  } else {
    iconElement.classList.remove("rotating");
  }
}

async function mostrarCargaProceso(procesos, periodo) {
  const urlsIconos = procesos.map(p => p.icono);
  await Promise.all(urlsIconos.map(url => {
      return new Promise((resolve, reject) => {
          const img = new Image();
          img.src = url;
          img.onload = resolve;
          img.onerror = reject;
      });
  }));

  Swal.fire({
    title: '<span class="titulo-sime">SIME 360</span>',
    html: `
        <div class="contenedor-proceso">
            <div class="spinner-bubble"></div>
            <img id="iconoProceso" src="" class="icono-proceso">
            <div id="textoProceso" class="texto-proceso">Iniciando...</div>
            <div id="periodoProceso" class="periodo-proceso"></div>
        </div>
      `,
    background: "#f8f9fa",
    backdrop: `rgba(0, 0, 0, 0.4) left top no-repeat`,
    allowOutsideClick: false,
    showConfirmButton: false,
    customClass: {
      popup: "custom-popup",
    },
  });

  for (const proceso of procesos) {
    const iconoElement = document.getElementById("iconoProceso");
    const textoElement = document.getElementById("textoProceso");
    const periodoElement = document.getElementById("periodoProceso");

    if (iconoElement && textoElement && periodoElement) {
      iconoElement.style.opacity = "0";
      textoElement.style.opacity = "0";
      periodoElement.style.opacity = "0";

      await new Promise((res) => setTimeout(res, 300));

      iconoElement.src = proceso.icono;
      textoElement.textContent = proceso.titulo;

      if (periodo === 0) {
        periodoElement.textContent = "Procesando datos...";
      } else {
        periodoElement.textContent = `Últimos ${periodo} días`;
      }
      iconoElement.style.opacity = "1";
      textoElement.style.opacity = "1";
      periodoElement.style.opacity = "1";
    }
    await proceso.funcion();
  }
  Swal.close();
}


async function mostrarCargaProcesoAnimada(titulo, icono, periodo) {
  await new Promise((resolve, reject) => {
      const img = new Image();
      img.src = icono;
      img.onload = resolve;
      img.onerror = reject;
  });

  Swal.fire({
    title: '<span class="titulo-sime">SIME 360</span>',
    html: `
        <div class="contenedor-proceso">
            <div class="spinner-bubble"></div>
            <img id="iconoProceso" src="${icono}" class="icono-proceso">
            <div id="textoProceso" class="texto-proceso">${titulo}</div>
            <div id="periodoProceso" class="periodo-proceso">
                ${periodo === 0 ? "Procesando datos..." : `Últimos ${periodo} días`}
            </div>
        </div>
      `,
    background: "#f8f9fa",
    backdrop: `rgba(0, 0, 0, 0.4) left top no-repeat`,
    allowOutsideClick: false,
    showConfirmButton: false,
    customClass: {
      popup: "custom-popup",
    },
  });
}


document.addEventListener("contextmenu", function (e) {
  e.preventDefault();
});