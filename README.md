**Introducción**

SIME 360 es una plataforma desarrollada como iniciativa personal de Jairo Sevilla, concebida con el objetivo de optimizar, centralizar y analizar el uso de Microsoft 365 dentro de entornos organizacionales, proporcionando una visión integral (360°) del consumo, la actividad y la gestión de los servicios digitales.

El proyecto fue diseñado, desarrollado e iterado de manera continua entre enero de 2025 y octubre de 2025, como resultado de la identificación de una necesidad recurrente en las organizaciones: la falta de una herramienta unificada que permita visualizar de forma clara, estructurada y accionable la información relacionada con usuarios, licencias, servicios y adopción de Microsoft 365.

SIME 360 integra múltiples módulos funcionales que permiten:

Monitorear el uso de servicios como Outlook, OneDrive, Teams y SharePoint.

Analizar el consumo de licencias y su clasificación.

Centralizar información de usuarios y sitios.

Facilitar la toma de decisiones mediante reportes, filtros y métricas consolidadas.

La plataforma fue construida con una arquitectura modular, orientada a la escalabilidad y la mantenibilidad, utilizando tecnologías web que permiten una experiencia fluida y dinámica, así como mecanismos de autenticación tanto local como corporativa (Azure AD), adaptándose a distintos contextos organizacionales.

Este repositorio documenta el diseño, la estructura y los módulos que componen SIME 360, sirviendo como referencia técnica y funcional del proyecto.

<img width="1915" height="907" alt="Login, Inicio" src="https://github.com/user-attachments/assets/6c066429-8ccb-456c-aa63-dadd65c0e13f" />


**Módulo de Inicio**

El Módulo de Inicio actúa como el punto central de acceso a SIME 360, proporcionando una vista general del sistema y del propósito de la plataforma desde el primer ingreso del usuario.

<img width="1919" height="914" alt="Inicio" src="https://github.com/user-attachments/assets/a4e0b3c3-14f0-4f26-b231-0b77cb9bc381" />


**Módulo de Usuarios**

El Módulo de Usuarios permite la gestión, visualización y análisis de los usuarios asociados al entorno Microsoft 365, ofreciendo una visión clara del estado y comportamiento de las cuentas dentro de la organización.

Desde este módulo es posible:

Visualizar el listado completo de usuarios, organizado desde el más antiguo al más reciente según su fecha de creación.

Consultar la información básica del usuario, la licencia asignada y datos relevantes como la fecha de la última conexión de cada usuario, así como descargar esta información para su posterior análisis.

Aplicar filtros, incluyendo:

Tipo de licencia asignada.

Estado de inicio de sesión.

Usuarios con inicio de sesión bloqueado.

Exportar la información de usuarios a archivo Excel, facilitando el análisis externo y la elaboración de reportes.

Acceder a estadísticas rápidas que permiten evaluar de forma inmediata el estado general de los usuarios, licencias y actividad.

Este módulo está diseñado para apoyar tareas de control, auditoría y toma de decisiones, proporcionando información accionable de manera rápida y estructurada.


<img width="1919" height="912" alt="Usuarios 1" src="https://github.com/user-attachments/assets/76b9f060-cb4e-487a-ab10-f0af186e6771" />
<img width="1918" height="914" alt="Usuarios 2" src="https://github.com/user-attachments/assets/7c23051f-bd00-429e-a500-811fc61a18d7" />
<img width="1918" height="911" alt="Usuarios 3" src="https://github.com/user-attachments/assets/0efbef1a-d744-4f1e-bc08-7b9eb516391c" />
<img width="1881" height="778" alt="Usuarios, Reporte" src="https://github.com/user-attachments/assets/5d39f9b5-cfa4-4e56-84e2-b1478006f1a0" />


**Módulo de Licencias**

El Módulo de Licencias permite visualizar y analizar de forma rápida el estado de las licencias de Microsoft 365 dentro de la organización, facilitando el control y la toma de decisiones relacionadas con su uso y asignación.

En este módulo, las licencias se presentan en tres secciones principales: Licencias de pago, Licencias gratuitas, Licencias sin clasificar.

La clasificación de las licencias depende de la configuración definida previamente en el Módulo de Configuración, lo que permite adaptar el sistema a las necesidades de cada organización.

Desde este módulo, los usuarios pueden:

Conocer de manera clara cuántas licencias han sido compradas.

Identificar cuántas licencias se encuentran asignadas a usuarios.

Visualizar licencias vencidas o inactivas.

Determinar cuántas licencias están disponibles para asignación.

Obtener una visión general del estado de licenciamiento de forma rápida, concisa y centralizada.

Este módulo proporciona una vista estratégica del licenciamiento, ayudando a optimizar costos, evitar sobreasignaciones y detectar oportunidades de mejora en el uso de los recursos.

<img width="1916" height="912" alt="Licencias" src="https://github.com/user-attachments/assets/c59916d4-cf30-429d-96da-7e3737719c7a" />




