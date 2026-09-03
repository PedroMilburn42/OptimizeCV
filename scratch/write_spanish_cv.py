import os
from pathlib import Path

slug = "missionhires-supervisor_desarrollo-260826"
app_dir = Path("data/applications") / slug
app_dir.mkdir(parents=True, exist_ok=True)

cv_html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Pedro Milburn - CV</title>
<style>
  @page { size: A4; margin: 1.4cm 1.7cm; }
  body { font-family: "Helvetica Neue", Arial, sans-serif; font-size: 9.8pt; color: #1a1a1a; background: #ffffff; line-height: 1.32; }

  .header { border-bottom: 2pt solid #1f3a5f; padding-bottom: 5pt; margin-bottom: 7pt; }
  h1 { font-size: 19pt; color: #1f3a5f; margin: 0 0 1pt 0; }
  .tagline { font-size: 10.5pt; color: #444; font-style: italic; margin-bottom: 3pt; }
  .contact { font-size: 9pt; color: #444; }

  h2 { font-size: 10.5pt; color: #1f3a5f; text-transform: uppercase; letter-spacing: 0.5pt; border-bottom: 1pt solid #1f3a5f; margin: 9pt 0 4pt 0; break-after: avoid; }

  .competency-row { margin-bottom: 2.5pt; break-inside: avoid; font-size: 9.2pt; }
  .competency-label { font-weight: bold; color: #1f3a5f; }

  .entry { margin-bottom: 6.5pt; break-inside: avoid; }
  .entry-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 9.8pt; }
  .entry-meta { font-size: 8.8pt; color: #555; font-style: italic; margin-bottom: 1.5pt; }
  ul { margin: 1.5pt 0 0 0; padding-left: 13pt; }
  li { margin-bottom: 1.5pt; font-size: 9.2pt; }
</style>
</head>
<body>
  <div class="header">
    <h1>Pedro Milburn</h1>
    <div class="tagline">Supervisor de Desarrollo | Líder Técnico &amp; Arquitecto de Software</div>
    <div class="contact">Montevideo, Uruguay &middot; pierre.milburn@hotmail.com &middot; +598 92 806 401 &middot; linkedin.com/in/pedro-milburn-a0700417</div>
  </div>

  <h2>Perfil Profesional</h2>
  <p>Líder Técnico, Supervisor de Desarrollo y Arquitecto de Software con más de 15 años de experiencia liderando equipos de ingeniería, coordinando proyectos tecnológicos complejos y diseñando sistemas empresariales de misión crítica. Especializado en gestión ágil (Scrum/Kanban), coordinación de proveedores, gobierno de arquitectura en .NET y SQL Server, y entrega de soluciones para el sector financiero, bancario y corporativo.</p>

  <h2>Competencias Clave</h2>
  <p class="competency-row"><span class="competency-label">Liderazgo y Gestión de Proyectos:</span> Supervisión de equipos de desarrollo (8+ ingenieros y QA), asignación de tareas, seguimiento de desempeño, estimación y control de plazos/alcance, gestión de riesgos técnicos, coordinación con stakeholders y proveedores.</p>
  <p class="competency-row"><span class="competency-label">Ecosistema Técnico:</span> C#, .NET 8 / .NET Core, ASP.NET Core, SQL Server, APIs REST, GraphQL, Microservicios, Entity Framework, WCF.</p>
  <p class="competency-row"><span class="competency-label">DevOps y Calidad:</span> Azure DevOps, Jira, Git, CI/CD pipelines, pruebas automatizadas (TDD), SonarQube, Veracode, estándares ISO y cumplimiento regulatorio.</p>
  <p class="competency-row"><span class="competency-label">Plataformas Cloud y Datos:</span> Microsoft Azure (AKS, Functions, App Services), Google Cloud Platform (Cloud Run, VMs), PostgreSQL, Oracle, Microsoft Fabric.</p>
  <p class="competency-row"><span class="competency-label">Metodologías e Innovación:</span> Scrum, Kanban, Domain-Driven Design (DDD), orquestación de soluciones con IA generativa, Microsoft Power Platform (PL-400, PL-100).</p>

  <h2>Experiencia Profesional</h2>
  <div class="entry">
    <div class="entry-header"><span>Lead Software Engineer | Aven Hospitality</span> <span>Ene 2026 - Presente</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Superviso y lidero un equipo técnico multidisciplinario de 8 profesionales (desarrolladores senior y especialistas de QA).</li>
      <li>Coordino la planificación de sprints, asignación de tareas y seguimiento de hitos de entrega para sistemas centrales de alta disponibilidad.</li>
      <li>Lidero la modernización de servicios desde .NET Framework hacia .NET moderno y migración a GCP (Cloud Run, VMs), asegurando continuidad operativa.</li>
      <li>Gestiono la calidad del código, mitigación de riesgos de seguridad y análisis de vulnerabilidades mediante Veracode y SonarQube.</li>
      <li>Articulo la comunicación técnica con gerencia, equipos de producto y áreas operativas para alinear prioridades estratégicas.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Development Team Lead | Sabre Corporation</span> <span>Oct 2023 - Feb 2026</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Lideré y gestioné directamente un equipo de 8 desarrolladores Senior .NET dedicados a los servicios y lógica de negocio de la plataforma global.</li>
      <li>Coordiné diariamente con directores y gerentes de producto la planificación de lanzamientos, resolución de incidencias críticas y cumplimiento de SLAs.</li>
      <li>Definí la arquitectura de microservicios en Microsoft Azure (AKS, Functions, App Services) e implementé pipelines de despliegue continuo en Azure DevOps.</li>
      <li>Promoví la mentoría técnica, estandarización de revisiones de código y optimización de velocidad de entrega del equipo.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Power Platform Architect &amp; .NET Developer | Globant</span> <span>Sep 2018 - Sep 2023</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Arquitecté e implementé soluciones empresariales complejas en .NET, SharePoint y Microsoft Power Platform para clientes corporativos de EE.UU. y Reino Unido.</li>
      <li>Coordiné requerimientos con múltiples partes interesadas internacionales y gestioné despliegues integrados mediante Azure DevOps.</li>
      <li>Desarrollé herramientas de productividad y extensiones en C# integradas con plataformas de IA para desarrollo de software.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Microsoft Architect &amp; SharePoint Developer | MVD Technologies</span> <span>Ago 2017 - Ago 2018</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Lideré el desarrollo y evolución de productos de cumplimiento normativo (MVD Quality para normas ISO y MVD Comply para alertas regulatorias) en Uruguay, Argentina, Chile y Perú.</li>
      <li>Diseñé arquitecturas de integración en la nube con Azure y APIs REST, coordinando la parametrización para más de 100 clientes corporativos.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>.NET Developer | Urudata Software (Proyecto Banco Itaú)</span> <span>Sep 2016 - Dic 2016</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Desarrollé en .NET MVC 5 y SQL Server el sistema central de digitalización y seguimiento de legajos de clientes para Banco Itaú en 20 sucursales bancarias.</li>
      <li>Integré motores de procesos y flujos de trabajo (Q-Flow) para trazabilidad documental bajo rigurosos estándares del sector bancario.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Software Architect &amp; Consultor | Grupo Pragma Consultores (Practia)</span> <span>Ago 2015 - Ago 2016</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Refactoricé los sistemas centrales de UPM Uruguay a una arquitectura desacoplada en 3 capas con Entity Framework y SQL Server, liderando un equipo de 4 desarrolladores.</li>
      <li>Gestioné soluciones tecnológicas e intranets de Business Intelligence para clientes regulados de gran escala, incluidos Banco de Chile y GNL Quintero.</li>
      <li>Implementé integración continua y pruebas automatizadas en servidores de compilación TeamCity.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Technical Solution Architect &amp; .NET Developer | HiQ</span> <span>Ene 2011 - Jul 2015</span></div>
    <div class="entry-meta">Gotemburgo, Suecia</div>
    <ul>
      <li>Desarrollé servicios backend en Azure para pagos automáticos de facturas en aplicaciones móviles para Collector Bank (Collector Betalkoll).</li>
      <li>Diseñé e implementé la arquitectura de la intranet corporativa global para Volvo Cars Corporation en SharePoint y Office 365.</li>
      <li>Construí APIs multiplataforma y servicios Windows de alta disponibilidad con integración OPC para Envac AB.</li>
    </ul>
  </div>

  <h2>Educación y Formación Académica</h2>
  <div class="entry">
    <div class="entry-header"><span>Estudios de Ingeniería en Sistemas | Universidad ORT Uruguay</span> <span>1993 - 1999</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Master's Degree in Mobile Services | Chalmers University of Technology (Suecia)</span> <span>2004 - 2006</span></div>
  </div>

  <h2>Certificaciones y Patentes</h2>
  <div class="entry">
    <div class="entry-header"><span>Certificaciones Microsoft:</span> <span>Power Platform Developer Associate (PL-400), App Maker (PL-100), MCTS C# &amp; SharePoint</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Certificaciones IA y DevOps:</span> <span>MLOps Essentials (2026), Generative AI Pair Programming (2026), Azure DevOps CI/CD</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Patente Internacional:</span> <span>Method for optimising the placement of at least two pieces of information (US 13/254,248)</span></div>
  </div>
</body>
</html>
"""

cv_path = app_dir / f"CV-{slug}.html"
cv_path.write_text(cv_html.strip(), encoding="utf-8")
print(f"Written HTML CV to {cv_path}")
