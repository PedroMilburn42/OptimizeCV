import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
import win32com.client

slug = "nango-staff_backend_engineer-260903"
app_dir = Path("data/applications") / slug
app_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. CV HTML (English, Tailored for Nango Staff Backend Engineer)
# -------------------------------------------------------------
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
    <div class="tagline">Staff Backend Engineer | Developer Infrastructure &amp; Applied AI Systems</div>
    <div class="contact">Montevideo, Uruguay (Remote) &middot; pierre.milburn@hotmail.com &middot; +598 92 806 401 &middot; linkedin.com/in/pedro-milburn-a0700417</div>
  </div>

  <h2>Profile</h2>
  <p>Staff Backend Engineer and Distributed Systems Architect with 15+ years of experience designing high-throughput developer infrastructure, scalable API runtimes, and distributed backend platforms. Proven track record taking complex systems from ideation to production, building developer tools and SDKs, and architecting unified integration layers for AI agent workflows. Deep expertise in high-concurrency backend services, open-source architecture (hexagonal ports &amp; adapters), API performance optimization, and international patent-backed algorithm engines.</p>

  <h2>Core Competencies</h2>
  <p class="competency-row"><span class="competency-label">Developer Infrastructure &amp; APIs:</span> API Runtime Architecture, Developer Experience (DX), SDKs &amp; Developer Tooling, High-Throughput RESTful APIs, OpenAPI / Schema Mapping, Webhooks, Rate-Limiting.</p>
  <p class="competency-row"><span class="competency-label">Backend &amp; Distributed Systems:</span> Node.js, C#, Python, Distributed Worker Runtimes, Event-Driven Queues (PubSub, Message Queues), Microservices, Hexagonal Architecture, Asynchronous Systems.</p>
  <p class="competency-row"><span class="competency-label">AI Agent Integrations:</span> Tool-Calling Runtimes, Context Engineering, LLM Integration Guardrails, MLOps Essentials (2026), Generative AI Pair Programming (2026), Responsible AI.</p>
  <p class="competency-row"><span class="competency-label">Data Platforms &amp; Scale:</span> SQL Server, PostgreSQL, Redis / Caching, Query Tuning, Connection Pooling, Distributed Transactions, Cloud (GCP, Azure).</p>
  <p class="competency-row"><span class="competency-label">Engineering Leadership &amp; Open Source:</span> Product Ownership, Specification-Driven Development, Code Reviews, Incident Command &amp; Blameless RCAs, Open Source Community Engagement.</p>

  <h2>Professional Experience</h2>
  <div class="entry">
    <div class="entry-header"><span>Lead Software Engineer &amp; Backend Architect | Aven Hospitality</span> <span>Jan 2026 - Jul 2026</span></div>
    <div class="entry-meta">Montevideo, Uruguay (Remote/Hybrid)</div>
    <ul>
      <li>Architected high-throughput backend services and event-driven messaging pipelines on GCP (Cloud Run, PubSub) handling high-volume transaction workloads.</li>
      <li>Built context orchestration and API integration tooling for LLM-assisted developer workflows using Gemini, Copilot, and internal agents.</li>
      <li>Instituted automated CI/CD deployment pipelines in Jenkins, establishing rigorous automated testing (TDD) and zero-downtime releases.</li>
      <li>Conducted security code reviews and threat modeling with Veracode and SonarQube, eliminating latency and security bottlenecks.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Manager &amp; Development Team Lead | Sabre Corporation</span> <span>Oct 2023 - Feb 2026</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Led a high-output backend engineering pod of 8 Senior developers building core transaction microservices on Microsoft Azure.</li>
      <li>Architected distributed cloud services (Azure Functions, AKS, App Services), resolving critical bottlenecks in transactional API latency.</li>
      <li>Directly shaped product specifications, technical roadmaps, and delivery cadences, maintaining high architectural standards across teams.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Power Platform Architect &amp; Developer Tooling Lead | Globant</span> <span>Sep 2018 - Sep 2023</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Engineered developer productivity plugins and AI-assisted tooling in C# and TypeScript for Globant's internal Augmented Coding initiative.</li>
      <li>Architected scalable cloud solutions, third-party API integrations, and developer platforms for enterprise accounts in the US and UK.</li>
      <li>Standardized async documentation and release engineering workflows in Azure DevOps and GitHub.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Software Architect &amp; Program Manager | Grupo Pragma Consultores (Practia)</span> <span>Aug 2015 - Aug 2016</span></div>
    <div class="entry-meta">Montevideo, Uruguay</div>
    <ul>
      <li>Led 4 delivery teams architecting decoupled, testable 3-layer enterprise platforms for UPM Uruguay and BI portals for Banco de Chile.</li>
      <li>Established automated build verification and continuous integration standards on build servers.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Technical Solution Architect &amp; API Runtime Lead | HiQ</span> <span>Jan 2011 - Jul 2015</span></div>
    <div class="entry-meta">Gothenburg, Sweden</div>
    <ul>
      <li><strong>Collector Bank (2014):</strong> Architected Azure Mobile Services backend REST APIs for automated mobile invoice payment processing.</li>
      <li><strong>Envac AB (2013-2015):</strong> Built self-healing, high-availability Windows Services, cross-platform APIs, and recursive SQL stored procedures for worldwide operations.</li>
      <li><strong>Volvo Cars Corporation (2011-2013):</strong> Delivered core architecture and development for the global worldwide enterprise platform on Microsoft cloud services.</li>
    </ul>
  </div>

  <div class="entry">
    <div class="entry-header"><span>Software Engineer | Admeta</span> <span>Feb 2007 - Dec 2009</span></div>
    <div class="entry-meta">Gothenburg, Sweden</div>
    <ul>
      <li>Developed yield optimization algorithms, multithreaded backend services, and high-throughput real-time bidding data pipelines.</li>
    </ul>
  </div>

  <h2>Education &amp; Credentials</h2>
  <div class="entry">
    <div class="entry-header"><span>Master's Degree in Mobile Services | Chalmers University of Technology (Sweden)</span> <span>2004 - 2006</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>Degree Studies, Systems Engineering | Universidad ORT Uruguay</span> <span>1993 - 1999</span></div>
  </div>

  <h2>Certifications &amp; Patents</h2>
  <div class="entry">
    <div class="entry-header"><span>AI &amp; Systems Credentials:</span> <span>Foundations of Responsible AI (2026), MLOps Essentials (2026), Generative AI Pair Programming (2026), PL-400</span></div>
  </div>
  <div class="entry">
    <div class="entry-header"><span>International Patent:</span> <span>Method for optimising the placement of at least two pieces of information (US 13/254,248 · registered in US, Europe, Sweden)</span></div>
  </div>
</body>
</html>
"""

cv_html_path = app_dir / f"CV-{slug}.html"
cv_html_path.write_text(cv_html.strip(), encoding="utf-8")
print(f"Written CV HTML: {cv_html_path}")

# -------------------------------------------------------------
# 2. CV DOCX (English)
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
r_tag = p_tag.add_run('Staff Backend Engineer | Developer Infrastructure & Applied AI Systems')
r_tag.italic = True
r_tag.font.size = Pt(10.5)
r_tag.font.color.rgb = GRAY_COLOR

p_contact = doc_cv.add_paragraph('Montevideo, Uruguay (Remote) · pierre.milburn@hotmail.com · +598 92 806 401 · linkedin.com/in/pedro-milburn-a0700417')
p_contact.runs[0].font.size = Pt(9)
p_contact.runs[0].font.color.rgb = GRAY_COLOR
p_contact.paragraph_format.space_after = Pt(6)

# Profile
add_cv_h2('Profile')
p_prof = doc_cv.add_paragraph(
    'Staff Backend Engineer and Distributed Systems Architect with 15+ years of experience designing high-throughput developer infrastructure, '
    'scalable API runtimes, and distributed backend platforms. Proven track record taking complex systems from ideation to production, '
    'building developer tools and SDKs, and architecting unified integration layers for AI agent workflows. Deep expertise in '
    'high-concurrency backend services, open-source architecture (hexagonal ports & adapters), API performance optimization, and '
    'international patent-backed algorithm engines.'
)
p_prof.paragraph_format.space_after = Pt(4)
p_prof.paragraph_format.line_spacing = 1.15

# Competencies
add_cv_h2('Core Competencies')

def add_comp(label, text):
    p = doc_cv.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_l = p.add_run(f'{label}: ')
    r_l.bold = True
    r_l.font.color.rgb = PRIMARY_COLOR
    p.add_run(text)

add_comp('Developer Infrastructure & APIs', 'API Runtime Architecture, Developer Experience (DX), SDKs & Developer Tooling, High-Throughput RESTful APIs, OpenAPI / Schema Mapping, Webhooks, Rate-Limiting.')
add_comp('Backend & Distributed Systems', 'Node.js, C#, Python, Distributed Worker Runtimes, Event-Driven Queues (PubSub, Message Queues), Microservices, Hexagonal Architecture, Asynchronous Systems.')
add_comp('AI Agent Integrations', 'Tool-Calling Runtimes, Context Engineering, LLM Integration Guardrails, MLOps Essentials (2026), Generative AI Pair Programming (2026), Responsible AI.')
add_comp('Data Platforms & Scale', 'SQL Server, PostgreSQL, Redis / Caching, Query Tuning, Connection Pooling, Distributed Transactions, Cloud (GCP, Azure).')
add_comp('Engineering Leadership & Open Source', 'Product Ownership, Specification-Driven Development, Code Reviews, Incident Command & Blameless RCAs, Open Source Community Engagement.')

# Experience
add_cv_h2('Professional Experience')

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
    'Lead Software Engineer & Backend Architect', 'Aven Hospitality', 'Jan 2026 - Jul 2026', 'Montevideo, Uruguay (Remote/Hybrid)',
    [
        'Architected high-throughput backend services and event-driven messaging pipelines on GCP (Cloud Run, PubSub) handling high-volume transaction workloads.',
        'Built context orchestration and API integration tooling for LLM-assisted developer workflows using Gemini, Copilot, and internal agents.',
        'Instituted automated CI/CD deployment pipelines in Jenkins, establishing rigorous automated testing (TDD) and zero-downtime releases.',
        'Conducted security code reviews and threat modeling with Veracode and SonarQube, eliminating latency and security bottlenecks.'
    ]
)

add_role_cv(
    'Manager & Development Team Lead', 'Sabre Corporation', 'Oct 2023 - Feb 2026', 'Montevideo, Uruguay',
    [
        'Led a high-output backend engineering pod of 8 Senior developers building core transaction microservices on Microsoft Azure.',
        'Architected distributed cloud services (Azure Functions, AKS, App Services), resolving critical bottlenecks in transactional API latency.',
        'Directly shaped product specifications, technical roadmaps, and delivery cadences, maintaining high architectural standards across teams.'
    ]
)

add_role_cv(
    'Power Platform Architect & Developer Tooling Lead', 'Globant', 'Sep 2018 - Sep 2023', 'Montevideo, Uruguay',
    [
        'Engineered developer productivity plugins and AI-assisted tooling in C# and TypeScript for Globant\'s internal Augmented Coding initiative.',
        'Architected scalable cloud solutions, third-party API integrations, and developer platforms for enterprise accounts in the US and UK.',
        'Standardized async documentation and release engineering workflows in Azure DevOps and GitHub.'
    ]
)

add_role_cv(
    'Software Architect & Program Manager', 'Grupo Pragma Consultores (Practia)', 'Aug 2015 - Aug 2016', 'Montevideo, Uruguay',
    [
        'Led 4 delivery teams architecting decoupled, testable 3-layer enterprise platforms for UPM Uruguay and BI portals for Banco de Chile.',
        'Established automated build verification and continuous integration standards on build servers.'
    ]
)

add_role_cv(
    'Technical Solution Architect & API Runtime Lead', 'HiQ', 'Jan 2011 - Jul 2015', 'Gothenburg, Sweden',
    [
        'Collector Bank (2014): Architected Azure Mobile Services backend REST APIs for automated mobile invoice payment processing.',
        'Envac AB (2013-2015): Built self-healing, high-availability Windows Services, cross-platform APIs, and recursive SQL stored procedures for worldwide operations.',
        'Volvo Cars Corporation (2011-2013): Delivered core architecture and development for the global worldwide enterprise platform on Microsoft cloud services.'
    ]
)

add_role_cv(
    'Software Engineer', 'Admeta', 'Feb 2007 - Dec 2009', 'Gothenburg, Sweden',
    [
        'Developed yield optimization algorithms, multithreaded backend services, and high-throughput real-time bidding data pipelines.'
    ]
)

# Education
add_cv_h2('Education & Credentials')
pe1 = doc_cv.add_paragraph()
pe1.paragraph_format.space_after = Pt(2)
re1_t = pe1.add_run('Master\'s Degree in Mobile Services | Chalmers University of Technology (Sweden)')
re1_t.bold = True
pe1.add_run(' (2004 - 2006)')

pe2 = doc_cv.add_paragraph()
pe2.paragraph_format.space_after = Pt(4)
re2_t = pe2.add_run('Degree Studies, Systems Engineering | Universidad ORT Uruguay')
re2_t.bold = True
pe2.add_run(' (1993 - 1999)')

# Certs
add_cv_h2('Certifications & Patents')
pc1 = doc_cv.add_paragraph()
pc1.paragraph_format.space_after = Pt(2)
rc1_l = pc1.add_run('AI & Systems Credentials: ')
rc1_l.bold = True
rc1_l.font.color.rgb = PRIMARY_COLOR
pc1.add_run('Foundations of Responsible AI (2026), MLOps Essentials (2026), Generative AI Pair Programming (2026), PL-400')

pc2 = doc_cv.add_paragraph()
pc2.paragraph_format.space_after = Pt(2)
rc2_l = pc2.add_run('International Patent: ')
rc2_l.bold = True
rc2_l.font.color.rgb = PRIMARY_COLOR
pc2.add_run('Method for optimising the placement of at least two pieces of information (US 13/254,248 · registered in US, Europe, Sweden)')

doc_cv.save(str(cv_docx_path))
print(f"Written CV DOCX: {cv_docx_path}")

# -------------------------------------------------------------
# 3. Cover Letter HTML (English, addressed to Nango)
# -------------------------------------------------------------
cl_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pedro Milburn - Cover Letter</title>
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
    <div class="sender-contact">Montevideo, Uruguay (Remote) &middot; pierre.milburn@hotmail.com &middot; +598 92 806 401 &middot; linkedin.com/in/pedro-milburn-a0700417</div>
  </div>
  <div class="date">September 3, 2026</div>
  <div class="recipient">Engineering Leadership &amp; Core Team<br>Nango (YC W23)</div>

  <p>Dear Nango Team,</p>

  <p>I am applying for the <strong>Staff Software Engineer, Backend</strong> role at Nango. Having spent 15+ years architecting developer infrastructure, high-throughput API runtimes, and distributed integration platforms, I have dedicated my career to building developer tools that turn complex backend protocols into seamless, reliable developer experiences.</p>

  <p>Nango's mission to provide the foundational API runtime connecting AI agents and applications to the real world directly reflects my technical background and engineering passions:</p>

  <ul>
    <li><strong>Developer Infrastructure &amp; Tooling Craftsmanship:</strong> Developed developer productivity extensions and AI coding tooling at Globant (Augmented Coding initiative), architected open-source platforms using hexagonal ports &amp; adapters architecture, and authored an international patent (US 13/254,248) in algorithmic optimization used across major tech ecosystems.</li>
    <li><strong>High-Throughput API Runtimes &amp; Scalability:</strong> Designed and scaled distributed microservices, asynchronous message queues (PubSub / Azure Service Bus), and rate-limited API integration layers across Aven Hospitality, Sabre Corporation, and Collector Bank, ensuring high reliability under heavy concurrency.</li>
    <li><strong>AI Agent Ecosystem &amp; Product Mindset:</strong> Deeply immersed in the AI developer stack, holding certifications in MLOps, Responsible AI, and Generative AI Pair Programming (2026). I operate as a product-minded engineer with strong developer empathy, taking end-to-end ownership from initial specification through implementation and open-source collaboration.</li>
  </ul>

  <p>Based in Uruguay and working seamlessly across North American and European time zones with full professional fluency in English, I bring a pragmatic, low-ego leadership style focused on unblocking teammates and delighting developer users.</p>

  <p>I look forward to discussing how my backend architecture and developer infrastructure experience can help Nango scale its unified integration platform.</p>

  <div class="signature">Sincerely,<br><strong>Pedro Milburn</strong></div>
</body>
</html>
"""

cl_html_path = app_dir / f"CL-{slug}.html"
cl_html_path.write_text(cl_html.strip(), encoding="utf-8")
print(f"Written CL HTML: {cl_html_path}")

# -------------------------------------------------------------
# 4. Cover Letter DOCX (English)
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

p_cl_contact = doc_cl.add_paragraph('Montevideo, Uruguay (Remote) · pierre.milburn@hotmail.com · +598 92 806 401 · linkedin.com/in/pedro-milburn-a0700417')
p_cl_contact.runs[0].font.size = Pt(9.5)
p_cl_contact.runs[0].font.color.rgb = GRAY_COLOR
p_cl_contact.paragraph_format.space_after = Pt(14)

p_cl_date = doc_cl.add_paragraph('September 3, 2026')
p_cl_date.paragraph_format.space_after = Pt(12)

p_cl_rec = doc_cl.add_paragraph('Engineering Leadership & Core Team\nNango (YC W23)')
p_cl_rec.paragraph_format.space_after = Pt(14)

p_cl_sal = doc_cl.add_paragraph('Dear Nango Team,')
p_cl_sal.paragraph_format.space_after = Pt(10)

p_cl_open = doc_cl.add_paragraph(
    'I am applying for the Staff Software Engineer, Backend role at Nango. Having spent 15+ years architecting developer '
    'infrastructure, high-throughput API runtimes, and distributed integration platforms, I have dedicated my career to building '
    'developer tools that turn complex backend protocols into seamless, reliable developer experiences.'
)
p_cl_open.paragraph_format.space_after = Pt(10)
p_cl_open.paragraph_format.line_spacing = 1.15

p_cl_body = doc_cl.add_paragraph(
    'Nango\'s mission to provide the foundational API runtime connecting AI agents and applications to the real world directly reflects my technical background and engineering passions:'
)
p_cl_body.paragraph_format.space_after = Pt(8)
p_cl_body.paragraph_format.line_spacing = 1.15

cl_b1 = doc_cl.add_paragraph(style='List Bullet')
r1 = cl_b1.add_run('Developer Infrastructure & Tooling Craftsmanship: ')
r1.bold = True
cl_b1.add_run(
    'Developed developer productivity extensions and AI coding tooling at Globant (Augmented Coding initiative), architected open-source platforms using hexagonal ports & adapters architecture, and authored an international patent (US 13/254,248) in algorithmic optimization used across major tech ecosystems.'
)
cl_b1.paragraph_format.space_after = Pt(4)
cl_b1.paragraph_format.line_spacing = 1.15

cl_b2 = doc_cl.add_paragraph(style='List Bullet')
r2 = cl_b2.add_run('High-Throughput API Runtimes & Scalability: ')
r2.bold = True
cl_b2.add_run(
    'Designed and scaled distributed microservices, asynchronous message queues (PubSub / Azure Service Bus), and rate-limited API integration layers across Aven Hospitality, Sabre Corporation, and Collector Bank, ensuring high reliability under heavy concurrency.'
)
cl_b2.paragraph_format.space_after = Pt(4)
cl_b2.paragraph_format.line_spacing = 1.15

cl_b3 = doc_cl.add_paragraph(style='List Bullet')
r3 = cl_b3.add_run('AI Agent Ecosystem & Product Mindset: ')
r3.bold = True
cl_b3.add_run(
    'Deeply immersed in the AI developer stack, holding certifications in MLOps, Responsible AI, and Generative AI Pair Programming (2026). I operate as a product-minded engineer with strong developer empathy, taking end-to-end ownership from initial specification through implementation and open-source collaboration.'
)
cl_b3.paragraph_format.space_after = Pt(10)
cl_b3.paragraph_format.line_spacing = 1.15

p_cl_close1 = doc_cl.add_paragraph(
    'Based in Uruguay and working seamlessly across North American and European time zones with full professional fluency in English, '
    'I bring a pragmatic, low-ego leadership style focused on unblocking teammates and delighting developer users.'
)
p_cl_close1.paragraph_format.space_after = Pt(10)
p_cl_close1.paragraph_format.line_spacing = 1.15

p_cl_close2 = doc_cl.add_paragraph('I look forward to discussing how my backend architecture and developer infrastructure experience can help Nango scale its unified integration platform.')
p_cl_close2.paragraph_format.space_after = Pt(16)

p_cl_sign = doc_cl.add_paragraph('Sincerely,\n')
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

print("All Nango application documents generated successfully!")
