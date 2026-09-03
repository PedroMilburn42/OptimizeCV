import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
import win32com.client

slug = "deloitte-desarrollador_dotnet_senior-260903"
app_dir = Path("data/applications") / slug
app_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. CV HTML (Spanish, Tailored for Deloitte .NET Senior Ref. 7750)
# -------------------------------------------------------------
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
    <div class="tagline">Desarrollador .NET Senior &amp; Arquitecto de Soluciones | Especialista en Sector Financiero</div>
    <div class="contact">Montevideo, Uruguay &middot; pierre.milburn@hotmail.com &middot; +598 92 806 401 &middot; linkedin.com/in/pedro-milburn-a0700417</div>
  </div>

  <h2>Perfil Profesional</h2>
  <p>Desarrollador .NET Senior y Arquitecto de Soluciones con más de 15 años de trayectoria diseñando, implementando y optimizando aplicaciones empresariales, servicios backend y bases de datos relacionales para instituciones financieras y corporativas líderes (Banco Itaú, Collector Bank, Banco de Chile, Banco Comercial). Especialista en C#, .NET (.NET 8, .NET Core, Framework), diseño de APIs REST, optimización avanzada de SQL Server y MySQL (procedimientos almacenados, índices y rendimiento), documentación técnica y soporte de segundo nivel ante incidentes críticos.</p>

  <h2>Competencias Clave</h2>
  <p class="competency-row"><span class="competency-label">Desarrollo .NET &amp; APIs:</span> C#, .NET 8, .NET Core, .NET Framework, ASP.NET MVC, Web API, APIs REST (diseño, documentación y consumo), Microservicios, WCF, SOAP.</p>
  <p class="competency-row"><span class="competency-label">Bases de Datos &amp; Rendimiento:</span> SQL Server (T-SQL avanzado, stored procedures, optimización de queries, índices y planes de ejecución), MySQL, PostgreSQL, Oracle, Entity Framework Core, Dapper.</p>
  <p class="competency-row"><span class="competency-label">Experiencia en Sector Financiero:</span> Desarrollo para banca (Banco Itaú, Collector Bank, Banco de Chile), digitalización de documentos, pasarelas de pago, cumplimiento regulatorio y normativo.</p>
  <p class="competency-row"><span class="competency-label">Calidad, Soporte &amp; DevOps:</span> Soporte de segundo nivel (N2), análisis de causa raíz (RCA), TDD, pruebas unitarias y de integración, Veracode, SonarQube, Azure DevOps, Jenkins, Git.</p>
  <p class="competency-row"><span class="competency-label">Habilidades &amp; Metodologías:</span> Liderazgo técnico, autonomía, análisis de requerimientos funcionales y técnicos, documentación técnica exhaustiva, Scrum / Agile.</p>

  <h2>Experiencia Profesional</h2>
  <div class="entry">
    <div class="entry-header"><span>Lead Software Engineer | Aven Hospitality</span> <span>Ene 2026 - Jul 2026</span></div>
    <div class="entry-meta">Montevideo, Uruguay (Híbrido)</div>
    <ul>
      <li>Liderazgo técnico de un equipo de 8 ingenieros y especialistas de QA en el desarrollo de servicios backend en C# y .NET para procesamiento de transacciones.</li>
      <li>Diseño e integración de APIs REST y servicios distribuidos sobre GCP y máquinas virtuales, asegurando alta disponibilidad.</li>
      <li>Optimización de consultas a bases de datos relacionales y gestión de pipelines CI/CD automatizados mediante Jenkins y scripts PowerShell.</li>
      <li>Responsable de la resolución de incidentes en producción, análisis de rendimiento y remediación de vulnerabilidades con SonarQube y Veracode.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Manager &amp; Development Team Lead | Sabre Corporation</span> <span>Oct 2023 - Feb 2026</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Lideré un equipo de 8 desarrolladores .NET Senior en el diseño e implementación de la lógica de negocio central y microservicios transaccionales.</li>
      <li>Arquitectura e integración de servicios RESTful y Azure Services (App Services, Functions, AKS), optimizando latencias en consultas de alto volumen.</li>
      <li>Definición de estándares de código, documentación técnica y resolución de incidentes complejos de segundo nivel de escalación.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Power Platform Architect &amp; .NET Developer | Globant</span> <span>Sep 2018 - Sep 2023</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Diseño y desarrollo de soluciones empresariales en .NET/C#, integraciones de APIs REST y automatizaciones cloud para clientes corporativos de EE.UU. y Reino Unido.</li>
      <li>Desarrollo de herramientas de productividad y extensiones en C# integradas con plataformas de automatización.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Desarrollador .NET Senior | Urudata Software (Proyecto Banco Itaú)</span> <span>Sep 2016 - Dic 2016</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Desarrollo en .NET MVC 5 y SQL Server 2012 para el sistema central de digitalización, seguimiento y trazabilidad de legajos de clientes en 20 agencias de <strong>Banco Itaú</strong>.</li>
      <li>Diseño de modelos de datos, stored procedures complejos y optimización de consultas SQL bajo estrictos estándares de seguridad bancaria.</li>
      <li>Integración de APIs y motores de procesos (Q-Flow) con interfaces web en HTML5, JavaScript y jQuery.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Software Architect &amp; Program Manager | Grupo Pragma Consultores (Practia)</span> <span>Ago 2015 - Ago 2016</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Lideré equipos de desarrollo en proyectos corporativos, incluyendo sistemas de Business Intelligence e Intranet normativa para <strong>Banco de Chile</strong> y GNL Quintero.</li>
      <li>Refactorización de sistemas core para UPM Uruguay implementando arquitectura en capas desacoplada con Entity Framework y SQL Server 2014.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Technical Solution Architect &amp; .NET Developer | HiQ</span> <span>Ene 2011 - Jul 2015</span></div>
    <div class="entry-meta">Gotemburgo, Suecia</div>
    <ul>
      <li><strong>Collector Bank (2014):</strong> Desarrollo de backend REST en Azure para procesamiento automático de facturas y pasarela de pagos móviles (App Collector Betalkoll).</li>
      <li><strong>Envac AB (2013-2015):</strong> Desarrollo de servicios Windows de alta disponibilidad, APIs multiplataforma y stored procedures recursivos optimizados en SQL Server.</li>
      <li><strong>Volvo Cars Corporation (2011-2013):</strong> Arquitectura y desarrollo de la plataforma corporativa global en tecnologías Microsoft.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Software Developer | IBM (Proyecto Banco Comercial)</span> <span>Mar 2000 - Dic 2000</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Desarrollo en Visual Basic y C, participando en la parametrización e integración del sistema Siebel CRM para <strong>Banco Comercial</strong> en Montevideo.</li>
    </ul>
  </div>

  <h2>Formación Académica</h2>
  <div class="entry">
    <div class="entry-header"><span>Máster en Servicios Móviles &amp; Telecomunicaciones | Chalmers University of Technology (Suecia)</span> <span>2004 - 2006</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Estudios de Ingeniería en Sistemas | Universidad ORT Uruguay</span> <span>1993 - 1999</span></div>
  </div>

  <h2>Certificaciones &amp; Reconocimientos</h2>
  <div class="entry">
    <div class="entry-header"><span>Certificaciones Microsoft:</span> <span>MCTS: Programming in C# (70-483), Power Platform Developer Associate (PL-400), App Maker (PL-100)</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Bases de Datos &amp; AI:</span> <span>Bases de datos SQL en Microsoft Fabric (2026), ETL/ELT in PostgreSQL (2023), MLOps Essentials (2026)</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Patente Internacional:</span> <span>Método de optimización de información (Registrada en EE.UU. US 13/254,248, Europa y Suecia)</span></div>
  </div>
</body>
</html>
"""

cv_html_path = app_dir / f"CV-{slug}.html"
cv_html_path.write_text(cv_html.strip(), encoding="utf-8")
print(f"Written CV HTML: {cv_html_path}")

# -------------------------------------------------------------
# 2. CV DOCX (Spanish)
# -------------------------------------------------------------
cv_docx_path = app_dir / f"CV-{slug}.docx"
doc_cv = docx.Document()

for section in doc_cv.sections:
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

style_cv = doc_cv.styles['Normal']
style_cv.font.name = 'Arial'
style_cv.font.size = Pt(9.5)
style_cv.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

PRIMARY_COLOR = RGBColor(0x1f, 0x3a, 0x5f)
GRAY_COLOR = RGBColor(0x55, 0x55, 0x55)

def add_cv_h2(text):
    p = doc_cv.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text.upper())
    r.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = PRIMARY_COLOR
    return p

# Header
p_name = doc_cv.add_paragraph()
p_name.paragraph_format.space_after = Pt(1)
r_name = p_name.add_run('Pedro Milburn')
r_name.bold = True
r_name.font.size = Pt(18)
r_name.font.color.rgb = PRIMARY_COLOR

p_tag = doc_cv.add_paragraph()
p_tag.paragraph_format.space_after = Pt(2)
r_tag = p_tag.add_run('Desarrollador .NET Senior & Arquitecto de Soluciones | Especialista en Sector Financiero')
r_tag.italic = True
r_tag.font.size = Pt(10.5)
r_tag.font.color.rgb = GRAY_COLOR

p_contact = doc_cv.add_paragraph('Montevideo, Uruguay · pierre.milburn@hotmail.com · +598 92 806 401 · linkedin.com/in/pedro-milburn-a0700417')
p_contact.runs[0].font.size = Pt(9)
p_contact.runs[0].font.color.rgb = GRAY_COLOR
p_contact.paragraph_format.space_after = Pt(6)

# Profile
add_cv_h2('Perfil Profesional')
p_prof = doc_cv.add_paragraph(
    'Desarrollador .NET Senior y Arquitecto de Soluciones con más de 15 años de trayectoria diseñando, implementando y optimizando '
    'aplicaciones empresariales, servicios backend y bases de datos relacionales para instituciones financieras y corporativas líderes '
    '(Banco Itaú, Collector Bank, Banco de Chile, Banco Comercial). Especialista en C#, .NET (.NET 8, .NET Core, Framework), diseño '
    'de APIs REST, optimización avanzada de SQL Server y MySQL (procedimientos almacenados, índices y rendimiento), documentación '
    'técnica y soporte de segundo nivel ante incidentes críticos.'
)
p_prof.paragraph_format.space_after = Pt(4)
p_prof.paragraph_format.line_spacing = 1.15

# Competencies
add_cv_h2('Competencias Clave')

def add_comp(label, text):
    p = doc_cv.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_l = p.add_run(f'{label}: ')
    r_l.bold = True
    r_l.font.color.rgb = PRIMARY_COLOR
    p.add_run(text)

add_comp('Desarrollo .NET & APIs', 'C#, .NET 8, .NET Core, .NET Framework, ASP.NET MVC, Web API, APIs REST (diseño, documentación y consumo), Microservicios, WCF, SOAP.')
add_comp('Bases de Datos & Rendimiento', 'SQL Server (T-SQL avanzado, stored procedures, optimización de queries, índices y planes de ejecución), MySQL, PostgreSQL, Oracle, Entity Framework Core, Dapper.')
add_comp('Experiencia en Sector Financiero', 'Desarrollo para banca (Banco Itaú, Collector Bank, Banco de Chile), digitalización de documentos, pasarelas de pago, cumplimiento regulatorio y normativo.')
add_comp('Calidad, Soporte & DevOps', 'Soporte de segundo nivel (N2), análisis de causa raíz (RCA), TDD, pruebas unitarias y de integración, Veracode, SonarQube, Azure DevOps, Jenkins, Git.')
add_comp('Habilidades & Metodologías', 'Liderazgo técnico, autonomía, análisis de requerimientos funcionales y técnicos, documentación técnica exhaustiva, Scrum / Agile.')

# Experience
add_cv_h2('Experiencia Profesional')

def add_role_cv(title, company, dates, loc, bullets):
    p_head = doc_cv.add_paragraph()
    p_head.paragraph_format.space_before = Pt(4)
    p_head.paragraph_format.space_after = Pt(1)
    p_head.paragraph_format.keep_with_next = True
    r_t = p_head.add_run(f'{title} | {company}')
    r_t.bold = True
    r_t.font.color.rgb = PRIMARY_COLOR
    r_d = p_head.add_run(f'   ({dates})')
    r_d.font.color.rgb = GRAY_COLOR
    r_d.italic = True
    
    p_loc = doc_cv.add_paragraph(loc)
    p_loc.runs[0].font.size = Pt(8.5)
    p_loc.runs[0].font.italic = True
    p_loc.runs[0].font.color.rgb = GRAY_COLOR
    p_loc.paragraph_format.space_after = Pt(2)
    p_loc.paragraph_format.keep_with_next = True
    
    for b in bullets:
        bp = doc_cv.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(1.5)
        bp.paragraph_format.line_spacing = 1.15
        bp.add_run(b)

add_role_cv(
    'Lead Software Engineer', 'Aven Hospitality', 'Ene 2026 - Jul 2026', 'Montevideo, Uruguay (Híbrido)',
    [
        'Liderazgo técnico de un equipo de 8 ingenieros y especialistas de QA en el desarrollo de servicios backend en C# y .NET para procesamiento de transacciones.',
        'Diseño e integración de APIs REST y servicios distribuidos sobre GCP y máquinas virtuales, asegurando alta disponibilidad.',
        'Optimización de consultas a bases de datos relacionales y gestión de pipelines CI/CD automatizados mediante Jenkins y scripts PowerShell.',
        'Responsable de la resolución de incidentes en producción, análisis de rendimiento y remediación de vulnerabilidades con SonarQube y Veracode.'
    ]
)

add_role_cv(
    'Manager & Development Team Lead', 'Sabre Corporation', 'Oct 2023 - Feb 2026', 'Montevideo, Uruguay',
    [
        'Lideré un equipo de 8 desarrolladores .NET Senior en el diseño e implementación de la lógica de negocio central y microservicios transaccionales.',
        'Arquitectura e integración de servicios RESTful y Azure Services (App Services, Functions, AKS), optimizando latencias en consultas de alto volumen.',
        'Definición de estándares de código, documentación técnica y resolución de incidentes complejos de segundo nivel de escalación.'
    ]
)

add_role_cv(
    'Power Platform Architect & .NET Developer', 'Globant', 'Sep 2018 - Sep 2023', 'Montevideo, Uruguay',
    [
        'Diseño y desarrollo de soluciones empresariales en .NET/C#, integraciones de APIs REST y automatizaciones cloud para clientes corporativos de EE.UU. y Reino Unido.',
        'Desarrollo de herramientas de productividad y extensiones en C# integradas con plataformas de automatización.'
    ]
)

add_role_cv(
    'Desarrollador .NET Senior', 'Urudata Software (Proyecto Banco Itaú)', 'Sep 2016 - Dic 2016', 'Montevideo, Uruguay',
    [
        'Desarrollo en .NET MVC 5 y SQL Server 2012 para el sistema central de digitalización, seguimiento y trazabilidad de legajos de clientes en 20 agencias de Banco Itaú.',
        'Diseño de modelos de datos, stored procedures complejos y optimización de consultas SQL bajo estrictos estándares de seguridad bancaria.',
        'Integración de APIs y motores de procesos (Q-Flow) con interfaces web en HTML5, JavaScript y jQuery.'
    ]
)

add_role_cv(
    'Software Architect & Program Manager', 'Grupo Pragma Consultores (Practia)', 'Ago 2015 - Ago 2016', 'Montevideo, Uruguay',
    [
        'Lideré equipos de desarrollo en proyectos corporativos, incluyendo sistemas de Business Intelligence e Intranet normativa para Banco de Chile y GNL Quintero.',
        'Refactorización de sistemas core para UPM Uruguay implementando arquitectura en capas desacoplada con Entity Framework y SQL Server 2014.'
    ]
)

add_role_cv(
    'Technical Solution Architect & .NET Developer', 'HiQ', 'Ene 2011 - Jul 2015', 'Gotemburgo, Suecia',
    [
        'Collector Bank (2014): Desarrollo de backend REST en Azure para procesamiento automático de facturas y pasarela de pagos móviles (App Collector Betalkoll).',
        'Envac AB (2013-2015): Desarrollo de servicios Windows de alta disponibilidad, APIs multiplataforma y stored procedures recursivos optimizados en SQL Server.',
        'Volvo Cars Corporation (2011-2013): Arquitectura y desarrollo de la plataforma corporativa global en tecnologías Microsoft.'
    ]
)

add_role_cv(
    'Software Developer', 'IBM (Proyecto Banco Comercial)', 'Mar 2000 - Dic 2000', 'Montevideo, Uruguay',
    [
        'Desarrollo en Visual Basic y C, participando en la parametrización e integración del sistema Siebel CRM para Banco Comercial en Montevideo.'
    ]
)

# Education
add_cv_h2('Formación Académica')
pe1 = doc_cv.add_paragraph()
pe1.paragraph_format.space_after = Pt(2)
re1_t = pe1.add_run('Máster en Servicios Móviles & Telecomunicaciones | Chalmers University of Technology (Suecia)')
re1_t.bold = True
pe1.add_run(' (2004 - 2006)')

pe2 = doc_cv.add_paragraph()
pe2.paragraph_format.space_after = Pt(4)
re2_t = pe2.add_run('Estudios de Ingeniería en Sistemas | Universidad ORT Uruguay')
re2_t.bold = True
pe2.add_run(' (1993 - 1999)')

# Certs
add_cv_h2('Certificaciones & Reconocimientos')
pc1 = doc_cv.add_paragraph()
pc1.paragraph_format.space_after = Pt(2)
rc1_l = pc1.add_run('Certificaciones Microsoft: ')
rc1_l.bold = True
rc1_l.font.color.rgb = PRIMARY_COLOR
pc1.add_run('MCTS: Programming in C# (70-483), Power Platform Developer Associate (PL-400), App Maker (PL-100)')

pc2 = doc_cv.add_paragraph()
pc2.paragraph_format.space_after = Pt(2)
rc2_l = pc2.add_run('Bases de Datos & AI: ')
rc2_l.bold = True
rc2_l.font.color.rgb = PRIMARY_COLOR
pc2.add_run('Bases de datos SQL en Microsoft Fabric (2026), ETL/ELT in PostgreSQL (2023), MLOps Essentials (2026)')

pc3 = doc_cv.add_paragraph()
pc3.paragraph_format.space_after = Pt(2)
rc3_l = pc3.add_run('Patente Internacional: ')
rc3_l.bold = True
rc3_l.font.color.rgb = PRIMARY_COLOR
pc3.add_run('Método de optimización de información (Registrada en EE.UU. US 13/254,248, Europa y Suecia)')

doc_cv.save(str(cv_docx_path))
print(f"Written CV DOCX: {cv_docx_path}")

# -------------------------------------------------------------
# 3. Cover Letter HTML (Spanish, addressed to Deloitte Ref. 7750)
# -------------------------------------------------------------
cl_html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Pedro Milburn - Carta de Presentación</title>
<style>
  @page { size: A4; margin: 2.2cm 2.4cm; }
  body { font-family: "Helvetica Neue", Arial, sans-serif; font-size: 11pt; color: #1a1a1a; background: #ffffff; line-height: 1.45; }

  .sender { border-bottom: 2pt solid #1f3a5f; padding-bottom: 6pt; margin-bottom: 14pt; }
  .sender-name { font-size: 15pt; font-weight: bold; color: #1f3a5f; }
  .sender-contact { font-size: 9.5pt; color: #444; margin-top: 2pt; }

  .date { margin-bottom: 14pt; font-size: 10pt; color: #555; }
  .recipient { margin-bottom: 14pt; font-size: 10.5pt; }
  p { margin: 0 0 9pt 0; }
  ul { margin: 0 0 9pt 0; padding-left: 16pt; break-inside: avoid; }
  li { margin-bottom: 3pt; }
  .signature { margin-top: 14pt; }
</style>
</head>
<body>
  <div class="sender">
    <div class="sender-name">Pedro Milburn</div>
    <div class="sender-contact">Montevideo, Uruguay &middot; pierre.milburn@hotmail.com &middot; +598 92 806 401 &middot; linkedin.com/in/pedro-milburn-a0700417</div>
  </div>
  <div class="date">3 de septiembre de 2026</div>
  <div class="recipient">Equipo de Selección / Capital Humano<br>Deloitte Uruguay<br><strong>Ref. 7750: Desarrollador/a .NET Senior (Sector Financiero)</strong></div>

  <p>Estimado equipo de selección de Deloitte,</p>

  <p>Me dirijo a ustedes para presentar mi postulación a la posición de <strong>Desarrollador/a .NET Senior (Ref. 7750)</strong> para la institución financiera líder cliente de su firma. Cuento con más de 15 años de experiencia liderando el desarrollo backend en el ecosistema .NET (C#), diseño de APIs REST y gestión avanzada de bases de datos relacionales (SQL Server y MySQL) en entornos altamente regulados.</p>

  <p>A lo largo de mi carrera he tenido la oportunidad de desarrollar soluciones clave para instituciones bancarias y financieras de primer nivel, lo que me permite adaptarme de inmediato a los estándares de seguridad, rigor y rendimiento requeridos:</p>

  <ul>
    <li><strong>Experiencia en Sector Financiero y Banca:</strong> Diseñé e implementé en .NET MVC y SQL Server el sistema central de trazabilidad documental para 20 agencias de <strong>Banco Itaú</strong>, desarrollé servicios REST backend para pagos móviles en <strong>Collector Bank</strong> (Suecia) y gestioné plataformas de Business Intelligence e Intranets normativas para <strong>Banco de Chile</strong>.</li>
    <li><strong>Dominio Avanzado de SQL Server y MySQL:</strong> Amplia experiencia en diseño de esquemas relacionales, elaboración de procedimientos almacenados complejos, análisis de planes de ejecución y optimización de performance en consultas transaccionales de alto volumen.</li>
    <li><strong>APIs REST, Arquitectura y Soporte N2:</strong> Diseño, implementación, documentación técnica y consumo de APIs REST robustas, junto con una sólida capacidad de análisis de requerimientos, liderazgo técnico y resolución ágil de incidentes en entornos de producción.</li>
  </ul>

  <p>Con base en Montevideo y disponibilidad para trabajar en modalidad híbrida o presencial, aporto compromiso, autonomía, capacidad de trabajo en equipo y una clara orientación a resultados técnicos de calidad.</p>

  <p>Agradezco su consideración y quedo a su disposición para mantener una entrevista y profundizar en cómo mi experiencia puede contribuir al éxito del proyecto.</p>

  <div class="signature">Atentamente,<br><strong>Pedro Milburn</strong></div>
</body>
</html>
"""

cl_html_path = app_dir / f"CL-{slug}.html"
cl_html_path.write_text(cl_html.strip(), encoding="utf-8")
print(f"Written CL HTML: {cl_html_path}")

# -------------------------------------------------------------
# 4. Cover Letter DOCX (Spanish)
# -------------------------------------------------------------
cl_docx_path = app_dir / f"CL-{slug}.docx"
doc_cl = docx.Document()

for section in doc_cl.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

style_cl = doc_cl.styles['Normal']
style_cl.font.name = 'Arial'
style_cl.font.size = Pt(10.5)
style_cl.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

p_cl_name = doc_cl.add_paragraph()
p_cl_name.paragraph_format.space_after = Pt(2)
r_cl_name = p_cl_name.add_run('Pedro Milburn')
r_cl_name.bold = True
r_cl_name.font.size = Pt(16)
r_cl_name.font.color.rgb = PRIMARY_COLOR

p_cl_contact = doc_cl.add_paragraph('Montevideo, Uruguay · pierre.milburn@hotmail.com · +598 92 806 401 · linkedin.com/in/pedro-milburn-a0700417')
p_cl_contact.runs[0].font.size = Pt(9.5)
p_cl_contact.runs[0].font.color.rgb = GRAY_COLOR
p_cl_contact.paragraph_format.space_after = Pt(14)

p_cl_date = doc_cl.add_paragraph('3 de septiembre de 2026')
p_cl_date.paragraph_format.space_after = Pt(12)

p_cl_rec = doc_cl.add_paragraph('Equipo de Selección / Capital Humano\nDeloitte Uruguay\nRef. 7750: Desarrollador/a .NET Senior (Sector Financiero)')
p_cl_rec.paragraph_format.space_after = Pt(14)

p_cl_sal = doc_cl.add_paragraph('Estimado equipo de selección de Deloitte,')
p_cl_sal.paragraph_format.space_after = Pt(10)

p_cl_open = doc_cl.add_paragraph(
    'Me dirijo a ustedes para presentar mi postulación a la posición de Desarrollador/a .NET Senior (Ref. 7750) para la institución '
    'financiera líder cliente de su firma. Cuento con más de 15 años de experiencia liderando el desarrollo backend en el ecosistema '
    '.NET (C#), diseño de APIs REST y gestión avanzada de bases de datos relacionales (SQL Server y MySQL) en entornos altamente regulados.'
)
p_cl_open.paragraph_format.space_after = Pt(10)
p_cl_open.paragraph_format.line_spacing = 1.15

p_cl_body = doc_cl.add_paragraph(
    'A lo largo de mi carrera he tenido la oportunidad de desarrollar soluciones clave para instituciones bancarias y financieras de primer nivel, lo que me permite adaptarme de inmediato a los estándares de seguridad, rigor y rendimiento requeridos:'
)
p_cl_body.paragraph_format.space_after = Pt(8)
p_cl_body.paragraph_format.line_spacing = 1.15

cl_b1 = doc_cl.add_paragraph(style='List Bullet')
r1 = cl_b1.add_run('Experiencia en Sector Financiero y Banca: ')
r1.bold = True
cl_b1.add_run(
    'Diseñé e implementé en .NET MVC y SQL Server el sistema central de trazabilidad documental para 20 agencias de Banco Itaú, desarrollé servicios REST backend para pagos móviles en Collector Bank (Suecia) y gestioné plataformas de Business Intelligence e Intranets normativas para Banco de Chile.'
)
cl_b1.paragraph_format.space_after = Pt(4)
cl_b1.paragraph_format.line_spacing = 1.15

cl_b2 = doc_cl.add_paragraph(style='List Bullet')
r2 = cl_b2.add_run('Dominio Avanzado de SQL Server y MySQL: ')
r2.bold = True
cl_b2.add_run(
    'Amplia experiencia en diseño de esquemas relacionales, elaboración de procedimientos almacenados complejos, análisis de planes de ejecución y optimización de performance en consultas transaccionales de alto volumen.'
)
cl_b2.paragraph_format.space_after = Pt(4)
cl_b2.paragraph_format.line_spacing = 1.15

cl_b3 = doc_cl.add_paragraph(style='List Bullet')
r3 = cl_b3.add_run('APIs REST, Arquitectura y Soporte N2: ')
r3.bold = True
cl_b3.add_run(
    'Diseño, implementación, documentación técnica y consumo de APIs REST robustas, junto con una sólida capacidad de análisis de requerimientos, liderazgo técnico y resolución ágil de incidentes en entornos de producción.'
)
cl_b3.paragraph_format.space_after = Pt(10)
cl_b3.paragraph_format.line_spacing = 1.15

p_cl_close1 = doc_cl.add_paragraph(
    'Con base en Montevideo y disponibilidad para trabajar en modalidad híbrida o presencial, aporto compromiso, autonomía, capacidad de trabajo en equipo y una clara orientación a resultados técnicos de calidad.'
)
p_cl_close1.paragraph_format.space_after = Pt(10)
p_cl_close1.paragraph_format.line_spacing = 1.15

p_cl_close2 = doc_cl.add_paragraph('Agradezco su consideración y quedo a su disposición para mantener una entrevista y profundizar en cómo mi experiencia puede contribuir al éxito del proyecto.')
p_cl_close2.paragraph_format.space_after = Pt(16)

p_cl_sign = doc_cl.add_paragraph('Atentamente,\n')
r_cl_sig = p_cl_sign.add_run('Pedro Milburn')
r_cl_sig.bold = True

doc_cl.save(str(cl_docx_path))
print(f"Written CL DOCX: {cl_docx_path}")

# -------------------------------------------------------------
# 5. Convert DOCX to PDF via Word COM
# -------------------------------------------------------------
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
try:
    # CV PDF
    cv_pdf_path = app_dir / f"CV-{slug}.pdf"
    doc1 = word.Documents.Open(str(cv_docx_path.resolve()))
    doc1.SaveAs(str(cv_pdf_path.resolve()), FileFormat=17)
    doc1.Close()
    print(f"Written CV PDF: {cv_pdf_path}")

    # CL PDF
    cl_pdf_path = app_dir / f"CL-{slug}.pdf"
    doc2 = word.Documents.Open(str(cl_docx_path.resolve()))
    doc2.SaveAs(str(cl_pdf_path.resolve()), FileFormat=17)
    doc2.Close()
    print(f"Written CL PDF: {cl_pdf_path}")
finally:
    word.Quit()

print("All Deloitte application documents generated successfully!")
