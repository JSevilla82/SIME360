document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const btnMenu = document.getElementById("btnMenu");
    const contenedor = document.getElementById("contenidoPrincipal");
    const menuList = document.querySelector(".menu"); // Seleccionamos la lista ul

    const modulosCargados = new Set();
    const modulosEjecutados = new Set();

    btnMenu.addEventListener("click", () => {
        sidebar.classList.toggle("active");
    });

    const gestionarVisibilidadModulos = (idModuloVisible) => {
        Array.from(contenedor.children).forEach((child) => {
            child.style.display = child.id === idModuloVisible ? "block" : "none";
        });
    };

    const ejecutarFuncionModulo = (modulo) => {
        // Asegura que la función del módulo solo se ejecute una vez.
        if (typeof window[modulo] === "function" && !modulosEjecutados.has(modulo)) {
            try {
                window[modulo]();
                modulosEjecutados.add(modulo);
                console.log(`Función del módulo ${modulo} ejecutada.`);
            } catch (error) {
                console.error(`Error al ejecutar la función del módulo ${modulo}:`, error);
                Swal.fire("Error", `Hubo un problema al inicializar el módulo: ${modulo}`, "error");
            }
        }
    };

    const cargarScriptModulo = async (modulo, jsPath) => {
        if (modulosCargados.has(modulo)) {
            ejecutarFuncionModulo(modulo);
            return;
        }
        try {
            const response = await fetch(jsPath, { method: 'HEAD' });
            if (response.ok) {
                const script = document.createElement("script");
                script.src = jsPath;
                script.onload = () => {
                    console.log(`${modulo}.js cargado.`);
                    modulosCargados.add(modulo);
                    ejecutarFuncionModulo(modulo);
                };
                script.onerror = (e) => { throw new Error(`Error de red o script no encontrado: ${jsPath}`); };
                document.body.appendChild(script);
            } else {
                console.warn(`No existe JS para ${modulo}. Se cargó solo el HTML.`);
            }
        } catch (error) {
            console.error(`❌ Error al cargar el script ${jsPath}:`, error);
        }
    };

    const cargarModulo = async (modulo) => {
        const idModulo = `modulo-${modulo}`;
        gestionarVisibilidadModulos(idModulo);

        if (document.getElementById(idModulo)) {
            ejecutarFuncionModulo(modulo);
            return;
        }

        const nuevoDiv = document.createElement("div");
        nuevoDiv.id = idModulo;
        contenedor.appendChild(nuevoDiv);

        try {
            const htmlPath = `/modulos_index/${modulo}.html`;
            const response = await fetch(htmlPath);
            if (!response.ok) throw new Error(`No se encontró ${htmlPath}`);
            
            nuevoDiv.innerHTML = await response.text();

            const jsPath = `/static/js/${modulo}.js`;
            await cargarScriptModulo(modulo, jsPath);

        } catch (error) {
            console.error(error);
            Swal.fire("Error", `No se pudo cargar el módulo: ${modulo}`, "error");
            nuevoDiv.remove();
        }
    };

    // --- Lógica de Inicialización y Eventos ---
    if (menuList) {
        // Usamos delegación de eventos para más robustez
        menuList.addEventListener("click", (e) => {
            const item = e.target.closest("li[data-modulo]");
            if (!item) return;

            const modulo = item.getAttribute("data-modulo");
            
            // Gestionar la clase activa
            menuList.querySelectorAll("li").forEach(li => li.classList.remove('active'));
            item.classList.add('active');
            
            cargarModulo(modulo);
        });
    }

    // Cargar el módulo inicial
    const moduloInicial = "inicio";
    const botonInicial = document.querySelector(`[data-modulo="${moduloInicial}"]`);
    if (botonInicial) {
        botonInicial.click();
    }
});