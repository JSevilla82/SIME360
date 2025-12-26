**SIME360 – Sistema de Información Microsoft Empresarial**

🔒 **Confidencialidad y propiedad intelectual**
Este proyecto fue desarrollado de manera independiente para uso empresarial. Por razones de protección de la solución, parte del código ha sido ofuscado.
El desarrollo y los derechos de autor pertenecen al autor del proyecto.

**Introducción**

SIME 360 es una plataforma desarrollada como iniciativa personal de Jairo Sevilla, concebida con el objetivo de optimizar, centralizar y analizar el uso de Microsoft 365 dentro de entornos organizacionales.
El proyecto fue diseñado, desarrollado e iterado de manera continua entre enero de 2025 y octubre de 2025, como resultado de la identificación de una necesidad recurrente en las organizaciones: la ausencia de una herramienta unificada que permita visualizar de forma clara, estructurada y accionable la información relacionada con usuarios, licencias, servicios y niveles de adopción de Microsoft 365.

SIME 360 integra múltiples módulos funcionales que permiten monitorear el uso de servicios como Outlook, OneDrive, Teams y SharePoint, analizar el consumo y la clasificación de licencias, centralizar la información de usuarios y sitios, y facilitar la toma de decisiones mediante reportes, filtros y métricas consolidadas.

La plataforma fue construida con una arquitectura modular, orientada a la escalabilidad y la mantenibilidad, utilizando tecnologías web que ofrecen una experiencia fluida y dinámica. Asimismo, incorpora mecanismos de autenticación tanto local como corporativa mediante Azure Active Directory, lo que le permite adaptarse a distintos contextos organizacionales y modelos de seguridad.

Este repositorio documenta el diseño, la estructura y los módulos que componen SIME 360, sirviendo como referencia técnica y funcional del proyecto.

<img width="1915" height="907" alt="Login, Inicio" src="https://github.com/user-attachments/assets/6c066429-8ccb-456c-aa63-dadd65c0e13f" />
<img width="1920" height="900" alt="Login, Iniciando" src="https://github.com/user-attachments/assets/55225b51-c497-4984-831f-b8f4dda17d51" />




**Módulo de Inicio**

El Módulo de Inicio actúa como el punto central de acceso a SIME 360, proporcionando una vista general del sistema y del propósito de la plataforma desde el primer ingreso del usuario.

<img width="1917" height="912" alt="Inicio, Menú" src="https://github.com/user-attachments/assets/2787c119-3ec9-4ab4-a763-a9460526d38b" />


**Módulo de Usuarios**

El Módulo de Usuarios permite la gestión, visualización y análisis de los usuarios asociados al entorno Microsoft 365, ofreciendo una visión clara del estado y comportamiento de las cuentas dentro de la organización.

Desde este módulo es posible visualizar el listado completo de usuarios, organizado desde el más antiguo al más reciente según su fecha de creación, así como consultar la información básica de cada usuario, la licencia asignada y datos relevantes como la fecha de la última conexión. Esta información puede ser descargada para su posterior análisis y seguimiento.

El módulo permite aplicar distintos filtros que facilitan el análisis segmentado, incluyendo el tipo de licencia asignada, el estado de inicio de sesión y la identificación de usuarios con el inicio de sesión bloqueado. Adicionalmente, toda la información de usuarios puede ser exportada a archivo Excel, lo que facilita el análisis externo, la elaboración de reportes y procesos de auditoría.

Asimismo, el módulo presenta estadísticas rápidas que permiten evaluar de forma inmediata el estado general de los usuarios, las licencias asignadas y el nivel de actividad dentro del entorno Microsoft 365.

Este módulo está diseñado para apoyar tareas de control, auditoría y toma de decisiones, proporcionando información clara, estructurada y accionable de manera ágil.


<img width="1919" height="912" alt="Usuarios 1" src="https://github.com/user-attachments/assets/76b9f060-cb4e-487a-ab10-f0af186e6771" />
<img width="1918" height="914" alt="Usuarios 2" src="https://github.com/user-attachments/assets/7c23051f-bd00-429e-a500-811fc61a18d7" />
<img width="1918" height="911" alt="Usuarios 3" src="https://github.com/user-attachments/assets/0efbef1a-d744-4f1e-bc08-7b9eb516391c" />
<img width="1916" height="892" alt="image" src="https://github.com/user-attachments/assets/2b6b32d9-5cd5-47c5-b3d6-fa4e0ccf2678" />



**Módulo de Licencias**

El Módulo de Licencias permite visualizar y analizar de forma rápida el estado de las licencias de Microsoft 365 dentro de la organización, facilitando el control y la toma de decisiones relacionadas con su uso y asignación.

En este módulo, las licencias se presentan en tres secciones principales: licencias de pago, licencias gratuitas y licencias sin clasificar. La clasificación de las licencias depende de la configuración definida previamente en el Módulo de Configuración, lo que permite adaptar el sistema a las necesidades específicas de cada organización y garantizar una correcta interpretación de la información.

Desde este módulo, los usuarios pueden conocer de manera clara cuántas licencias han sido compradas, identificar cuántas se encuentran asignadas a usuarios, visualizar licencias vencidas o inactivas y determinar cuántas licencias están disponibles para asignación. Toda esta información se presenta de forma rápida, concisa y centralizada, permitiendo una visión general inmediata del estado del licenciamiento.

Este módulo proporciona una vista estratégica del licenciamiento, ayudando a optimizar costos, evitar sobreasignaciones y detectar oportunidades de mejora en el uso de los recursos de Microsoft 365 dentro de la organización.


<img width="1916" height="912" alt="Licencias" src="https://github.com/user-attachments/assets/c59916d4-cf30-429d-96da-7e3737719c7a" />


**Módulo de Informes de Uso**

El Módulo de Informes de Uso es uno de los componentes más completos y estratégicos de SIME 360, ya que permite analizar de forma detallada cómo los usuarios de la organización utilizan las principales herramientas de Microsoft 365.

Desde este módulo se puede visualizar y analizar el uso de Outlook, OneDrive, Teams y SharePoint, consolidando la información de actividad y consumo en una sola vista centralizada.

El módulo permite consultar el almacenamiento utilizado en Outlook y OneDrive por cada usuario, identificar la última actividad o conexión en cada uno de los servicios y analizar métricas clave asociadas al uso diario. Entre estas métricas se incluyen los correos recibidos y enviados en Outlook, los archivos sincronizados, activos y totales en OneDrive, las llamadas, reuniones y mensajes privados en Teams, así como los archivos vistos, archivos sincronizados y páginas visitadas en SharePoint.

Adicionalmente, el sistema permite acceder a un detalle individual por usuario, donde se consolida la información de uso de todos los servicios en una sola vista, facilitando el análisis puntual del comportamiento y nivel de adopción de cada cuenta.

Análisis y optimización de licencias

La información presentada en este módulo permite detectar usuarios con baja o nula actividad, que no están aprovechando completamente su licencia asignada, e identificar oportunidades para optimizar el licenciamiento. Por ejemplo, usuarios que reciben pocos correos o utilizan poco almacenamiento pueden migrarse a licencias con menores capacidades, mientras que usuarios con alto consumo de almacenamiento o alta actividad pueden requerir licencias con mayores características.

Este análisis apoya decisiones relacionadas con la reducción de costos, la reasignación de licencias y la mejora en la adopción de las herramientas de Microsoft 365 dentro de la organización.

Filtros, periodos y exportación

El módulo permite analizar la información en distintos periodos de tiempo, incluyendo los últimos 30, 60, 90 y 180 días, lo que facilita el seguimiento de tendencias y cambios en el comportamiento de los usuarios. Adicionalmente, toda la información puede ser exportada a Excel, facilitando el análisis externo, la generación de reportes y el cruce de datos para auditorías o revisiones más profundas.

Este módulo ofrece una visión clara, accionable y basada en datos del nivel de adopción y uso de Microsoft 365 dentro de la organización.


<img width="1917" height="913" alt="Informes de Uso, 1" src="https://github.com/user-attachments/assets/e585ae07-d1c8-450f-bd47-c09011489e04" />
<img width="1919" height="911" alt="Informes de Uso, 3" src="https://github.com/user-attachments/assets/d9b50da3-d128-4d18-99ad-a2f012039680" />
<img width="1919" height="910" alt="Informes de Uso, 2" src="https://github.com/user-attachments/assets/92c703bb-4953-450a-98f1-adae2ed9249f" />
<img width="1919" height="841" alt="image" src="https://github.com/user-attachments/assets/43091036-5637-4c3d-a5a9-c040d8bb6481" />



**Módulo de Sitios de SharePoint**

El Módulo de Sitios de SharePoint permite visualizar y analizar el estado, el nivel de uso y el consumo de almacenamiento de los sitios de SharePoint dentro de la organización, facilitando el control, la supervisión y la optimización del espacio asignado.

Desde este módulo es posible visualizar el listado completo de sitios de SharePoint, ordenados por fecha de creación, consultar la última actividad registrada en cada sitio y analizar métricas clave como la cantidad total de archivos, los archivos activos, el número de visitas, el almacenamiento utilizado en gigabytes frente al almacenamiento asignado y el porcentaje de uso del espacio disponible.

La información presentada permite identificar de manera clara sitios con alto consumo de almacenamiento, sitios con baja o nula actividad, así como aquellos que presentan un uso sobredimensionado o subutilizado del espacio asignado. Adicionalmente, el módulo permite acceder directamente a cada sitio mediante su URL, lo que facilita la validación, revisión manual o gestión directa del contenido.

Análisis y optimización

Los datos consolidados en este módulo permiten detectar sitios inactivos o con poca actividad que continúan consumiendo almacenamiento, identificar oportunidades para optimizar el espacio asignado ajustando las cuotas según el uso real y apoyar la toma de decisiones relacionadas con el archivado de sitios antiguos, la limpieza de información obsoleta y la reorganización del almacenamiento en SharePoint. Asimismo, se obtiene una visión general del consumo total de SharePoint dentro de la organización.

Filtros y exportación

El módulo incluye filtros que permiten segmentar la información por criterios como la última actividad, el número de visitas y los archivos activos, facilitando el análisis focalizado de los sitios. Adicionalmente, toda la información puede ser exportada a Excel, lo que permite realizar análisis detallados, auditorías y la generación de reportes externos.

Este módulo proporciona una visión clara, estructurada y accionable del estado de los sitios de SharePoint, ayudando a mantener un entorno ordenado, eficiente y alineado con las necesidades reales del negocio.

<img width="1919" height="917" alt="Sitios de Sharepoint," src="https://github.com/user-attachments/assets/f66b9b5c-5008-4e8f-8762-bb05128caa90" />
<img width="1919" height="914" alt="image" src="https://github.com/user-attachments/assets/47ab47bc-f51b-4e43-9e42-cc83fceb90f2" />


**Módulo de Configuración del Sistema**

El Módulo de Configuración del Sistema es el componente encargado de definir y administrar las reglas base de funcionamiento de SIME 360, asegurando que la información presentada en los demás módulos sea consistente, confiable y alineada con la configuración real del entorno Microsoft 365 de la organización.

Este módulo se divide en dos secciones principales: Configuración de Licencias y Acceso a la Herramienta, las cuales impactan directamente en el comportamiento general del sistema.

Configuración de Licencias

En esta sección se administran las licencias de Microsoft 365 que el sistema utiliza para clasificar y mostrar la información en los módulos de Usuarios, Licencias e Informes de Uso. Desde aquí se puede visualizar el listado completo de licencias detectadas en el tenant y configurar su información clave, incluyendo el identificador técnico (SKU), el nombre técnico, el nombre comercial, el tipo de licencia y el tipo de pago.

Las licencias pueden clasificarse como principales, correspondientes a las licencias base utilizadas por los usuarios para servicios como Outlook, OneDrive, Teams o SharePoint, o como secundarias, asociadas a productos o servicios específicos como Power BI, Project, Visio, Power Apps u otras soluciones adicionales. Asimismo, es posible definir si una licencia es de pago o gratuita, lo cual permite al sistema diferenciar correctamente el estado del licenciamiento.

Esta configuración es fundamental, ya que influye directamente en la forma en que SIME 360 interpreta, agrupa y presenta la información relacionada con el uso de licencias, facilitando análisis de consumo, optimización de recursos y control de costos.

Acceso a la Herramienta

La sección de Acceso a la Herramienta permite gestionar qué usuarios pueden ingresar a SIME 360 utilizando su cuenta corporativa de Microsoft. Desde este espacio se pueden buscar usuarios por su correo electrónico corporativo y visualizar información relevante como nombre completo, correo electrónico, cargo, oficina, estado de la cuenta e información del líder, antes de autorizar o restringir el acceso al sistema.

El módulo permite autorizar, deshabilitar o revocar accesos de manera controlada, así como consultar un histórico de accesos donde se registra la fecha de autorización, el usuario autorizado y el estado del acceso. Esta funcionalidad garantiza que únicamente los usuarios previamente autorizados puedan acceder a la plataforma, fortaleciendo los controles de seguridad y la administración de permisos.

Valor del módulo

El Módulo de Configuración del Sistema actúa como la base operativa de SIME 360, ya que centraliza la gestión de licencias y el control de accesos, asegurando coherencia en los datos, flexibilidad de configuración y un uso seguro y controlado de la herramienta dentro de la organización.

<img width="1907" height="911" alt="Configuración 1" src="https://github.com/user-attachments/assets/c7237abe-c898-42ec-83c8-00fbf244d0d3" />
<img width="1915" height="912" alt="Configuración 3" src="https://github.com/user-attachments/assets/a537d293-26f0-4561-a660-a40b2f4871a8" />
<img width="1912" height="911" alt="Configuración 2" src="https://github.com/user-attachments/assets/ff84727b-9019-4007-9c80-491ee1b6af1b" />

_____________________________________________________________________________________________________________________________________________


**Arquitectura y Estructura del Proyecto**

SIME 360 está desarrollado como una aplicación web modular, basada en el framework Flask (Python), siguiendo una estructura clara que separa responsabilidades entre backend, frontend, configuración y recursos estáticos, lo que facilita la mantenibilidad y la escalabilidad del proyecto.

El backend está construido sobre Flask y se encarga de la lógica de negocio, la autenticación, el control de accesos y la exposición de rutas y servicios. La aplicación principal se inicializa desde app.py, donde se configuran los componentes base del sistema, incluyendo la carga de configuración, la inicialización de la base de datos, la protección CSRF y el registro de blueprints para mantener una arquitectura ordenada y desacoplada.

La aplicación utiliza blueprints para organizar funcionalidades específicas, como la autenticación con Microsoft mediante Azure Active Directory, permitiendo integrar de forma segura el acceso corporativo. Asimismo, se implementan mecanismos de control de permisos para restringir el acceso a los módulos según el usuario autenticado.

La capa de datos se gestiona mediante SQLAlchemy, permitiendo interactuar con la base de datos de forma estructurada y segura. Los modelos representan entidades clave del sistema, como usuarios y configuraciones necesarias para el funcionamiento de la plataforma.

El frontend está compuesto por plantillas HTML organizadas en el directorio templates, utilizando un enfoque modular donde cada funcionalidad principal del sistema cuenta con su propio archivo HTML dentro del directorio modulos_index. Esto permite cargar dinámicamente los módulos sin recargar completamente la aplicación, mejorando la experiencia de usuario.

Los recursos estáticos se encuentran organizados en el directorio static, separando hojas de estilo CSS, scripts JavaScript e imágenes. Cada módulo cuenta con sus propios archivos JavaScript y CSS, lo que favorece la modularidad y evita dependencias innecesarias entre componentes.

La lógica del lado del cliente se apoya en JavaScript, encargado de la carga dinámica de módulos, el consumo de datos, la interacción con el usuario y la exportación de información, como los reportes en Excel.

Finalmente, el proyecto incluye archivos de configuración y soporte como config.py, requirements.txt, variables de entorno (.env) y scripts de ejecución, lo que permite una instalación controlada y una correcta gestión de dependencias.

En conjunto, esta estructura permite que SIME 360 sea una solución organizada, flexible y preparada para evolucionar, facilitando la incorporación de nuevos módulos, mejoras funcionales y adaptaciones a distintos entornos organizacionales.

<img width="1614" height="978" alt="image" src="https://github.com/user-attachments/assets/5d55b832-fe6d-44b4-945b-8dc6d86dd76b" />







