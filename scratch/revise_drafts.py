from pathlib import Path

slug = "bairesdev-dotnet_software_engineer-260825"
app_dir = Path("data/applications") / slug

cv_html = """<!DOCTYPE html>
<html lang="en">
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
    <div class="tagline">Senior .NET Software Engineer &amp; Solution Architect</div>
    <div class="contact">Montevideo, Uruguay (Remote) &middot; pierre.milburn@hotmail.com &middot; +598 92 806 401 &middot; linkedin.com/in/pedro-milburn-a0700417</div>
  </div>

  <h2>Profile</h2>
  <p>Senior .NET Software Engineer and Solution Architect with 15+ years designing, modernizing, and operating scalable backend systems. Specialized in modernizing monolithic architectures to modern .NET and cloud-native microservices on GCP and Azure, leading cross-functional teams of up to 8 engineers, and embedding rigorous automated testing and security standards.</p>

  <h2>Core Competencies</h2>
  <p class="competency-row"><span class="competency-label">Backend &amp; Architecture:</span> C#, modern .NET (.NET 8, .NET Core), ASP.NET Core, Microservices, Domain-Driven Design (DDD), RESTful APIs, WCF.</p>
  <p class="competency-row"><span class="competency-label">Cloud &amp; DevOps:</span> GCP (Cloud Run, VMs, PubSub), Azure (AKS, Functions, App Services), Docker, Terraform, Jenkins, Azure DevOps, CI/CD.</p>
  <p class="competency-row"><span class="competency-label">Databases:</span> SQL Server, PostgreSQL, MySQL, Oracle, NHibernate, Entity Framework, Microsoft Fabric.</p>
  <p class="competency-row"><span class="competency-label">Quality &amp; Security:</span> TDD, Unit &amp; Integration Testing, SonarQube, Veracode, Splunk, Grafana, SOLID Principles.</p>
  <p class="competency-row"><span class="competency-label">Emerging Tech &amp; Tools:</span> LLM Solution Orchestration, Python (AI/ML), Microsoft Power Platform (PL-400, PL-100), Git.</p>

  <h2>Experience</h2>
  <div class="entry">
    <div class="entry-header"><span>Lead Software Engineer | Aven Hospitality</span> <span>Jan 2026 - Present</span></div>
    <div class="entry-meta">Montevideo, Uruguay (Remote/Hybrid)</div>
    <ul>
      <li>Upgraded core hospitality platform from legacy .NET Framework to modern .NET, migrating on-premise backend services to Google Cloud Platform (GCP).</li>
      <li>Designed scalable backend components on GCP Cloud Run and virtual machines, integrating PubSub messaging for high-throughput booking transaction processing.</li>
      <li>Managed CI/CD deployment pipelines via Jenkins and automated PowerShell scripts, collaborating daily with QA on automated testing.</li>
      <li>Led codebase security and quality remediation using Veracode and SonarQube, establishing clean code patterns across the service layer.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Development Team Lead | Sabre Corporation</span> <span>Oct 2023 - Feb 2026</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Led an engineering team of 8 Senior .NET developers building core business logic and microservices for the global travel platform.</li>
      <li>Architected distributed cloud services on Azure (AKS, Azure Functions, App Services), resolving critical bottlenecks in transaction latency.</li>
      <li>Standardized engineering practices, peer code reviews, and Azure DevOps release automation to improve delivery velocity.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Power Platform Architect and .NET Developer | Globant</span> <span>Sep 2018 - Sep 2023</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Architected and deployed custom .NET cloud solutions, integrations, and Power Platform automations for enterprise clients in the US and UK.</li>
      <li>Developed developer productivity tooling in C# and .NET integrated with internal AI coding platforms.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Microsoft Architect and SharePoint Developer | MVD Technologies</span> <span>Aug 2017 - Aug 2018</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Engineered enterprise ISO compliance software in C# and SharePoint Online, supporting enterprise clients across Latin America.</li>
      <li>Modernized legacy modules to cloud REST APIs using client-side JavaScript frameworks.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Technical Solution Architect &amp; .NET Developer | HiQ</span> <span>Jan 2011 - Jul 2015</span></div>
    <div class="entry-meta">Gothenburg, Sweden</div>
    <ul>
      <li>Built high-availability, self-recovering Windows Services, cross-platform APIs, and optimized SQL stored procedures for Envac AB worldwide operations.</li>
      <li>Developed Azure Mobile Services REST backend and client API integrations for Collector Bank mobile payment system.</li>
      <li>Designed architecture and led core development for Volvo Cars Corporation worldwide enterprise intranet in SharePoint and Office 365.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Software Engineer | Admeta</span> <span>Feb 2007 - Dec 2009</span></div>
    <div class="entry-meta">Gothenburg, Sweden</div>
    <ul>
      <li>Developed optimization algorithms, multithreaded Windows Services, and web applications in ASP.NET and C# for online media yield management.</li>
    </ul>
  </div>

  <h2>Education &amp; Credentials</h2>
  <div class="entry">
    <div class="entry-header"><span>Master's Degree, Mobile Services | Chalmers University of Technology</span> <span>2004 - 2006</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Degree Studies, Systems Engineering | Universidad ORT Uruguay</span> <span>1993 - 1999</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Key Certifications:</span> <span>Microsoft Certified PL-400, PL-100, MCTS C#, MLOps &amp; AI (2026)</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>US Patent 13/254,248:</span> <span>Method for optimising the placement of at least two pieces of information (US, Europe, Sweden)</span></div>
  </div>
</body>
</html>
"""

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
    <div class="sender-contact">Montevideo, Uruguay &middot; pierre.milburn@hotmail.com &middot; +598 92 806 401</div>
  </div>
  <div class="date">25 de agosto de 2026</div>
  <div class="recipient">Equipo de Selección / Hiring Team<br>BairesDev</div>

  <p>Estimado equipo de selección de BairesDev,</p>

  <p>Me postulo al rol de <strong>Ingeniero de Software .NET (Trabajo Remoto)</strong> con más de 15 años de experiencia como desarrollador senior y arquitecto de soluciones en el ecosistema .NET y C#, especializado en el diseño, modernización y operación de sistemas backend robustos y escalables para clientes y organizaciones globales.</p>

  <p>A lo largo de mi carrera en empresas como Aven Hospitality, Sabre Corporation y Globant, he liderado la transición de plataformas monolíticas hacia microservicios modernos en .NET Core y .NET 8 sobre infraestructuras cloud en GCP y Azure, garantizando alta disponibilidad y rendimiento:</p>

  <ul>
    <li><strong>Desarrollo Backend y Modernización Cloud:</strong> Experiencia directa en C#, ASP.NET Core, APIs REST, arquitecturas desacopladas y contenedores (Cloud Run, AKS), optimizando la persistencia de datos con SQL Server, PostgreSQL y Oracle.</li>
    <li><strong>Calidad de Software y CI/CD:</strong> Implementación de pruebas automatizadas (TDD), mejores prácticas SOLID y remediación continua de vulnerabilidades mediante Veracode y SonarQube en pipelines de integración continua.</li>
  </ul>

  <p>Con amplia experiencia en trabajo 100% remoto y entrega nearshore para clientes de Estados Unidos y Europa, colaboro fluidamente en inglés y español aportando disciplina técnica, autonomía en la resolución de problemas y enfoque en entrega continua.</p>

  <p>Agradezco su consideración y quedo a su disposición para coordinar una entrevista técnica.</p>

  <div class="signature">Atentamente,<br><strong>Pedro Milburn</strong></div>
</body>
</html>
"""

cv_path = app_dir / f"CV-{slug}.html"
cl_path = app_dir / f"CL-{slug}.html"

cv_path.write_text(cv_html.strip(), encoding="utf-8")
cl_path.write_text(cl_html.strip(), encoding="utf-8")

print("Revised drafts written successfully.")
