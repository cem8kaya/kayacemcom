"""Build Cem Kaya resume as a professional ATS-friendly 2-page .docx"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x0F, 0x17, 0x2A)   # #0f172a  – name / section headers
BLUE   = RGBColor(0x25, 0x63, 0xEB)   # #2563eb  – accent / company names
DARK   = RGBColor(0x1E, 0x29, 0x3B)   # #1e293b  – body text
MUTED  = RGBColor(0x47, 0x55, 0x69)   # #475569  – meta / dates
BORDER = RGBColor(0xBF, 0xDB, 0xFE)   # #bfdbfe  – dividers

# ── Helpers ───────────────────────────────────────────────────────────────────

def set_font(run, name="Calibri", size=10, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def para_space(para, before=0, after=0, line=None):
    pf = para.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after  = Pt(after)
    if line:
        pf.line_spacing = Pt(line)

def add_hr(doc, color=BORDER):
    """Thin colored bottom-border paragraph acting as a divider."""
    p = doc.add_paragraph()
    para_space(p, before=2, after=2)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '{:02X}{:02X}{:02X}'.format(*color))
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p

def section_heading(doc, text):
    add_hr(doc)
    p = doc.add_paragraph()
    para_space(p, before=6, after=2)
    run = p.add_run(text.upper())
    set_font(run, size=9, bold=True, color=BLUE)
    run.font.name = "Calibri"
    # letter spacing via rPr is not directly supported; bold+uppercase is enough
    return p

def job_header(doc, title, company, period, location):
    p = doc.add_paragraph()
    para_space(p, before=5, after=1)
    r1 = p.add_run(title)
    set_font(r1, size=10.5, bold=True, color=NAVY)
    r2 = p.add_run(f"  ·  {company}")
    set_font(r2, size=10.5, bold=False, color=BLUE)
    # meta line
    pm = doc.add_paragraph()
    para_space(pm, before=0, after=2)
    rm = pm.add_run(f"{period}    {location}")
    set_font(rm, size=9, color=MUTED, italic=False)
    return p

def bullet(doc, text, indent=0.35):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent  = Inches(indent)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    para_space(p, before=1, after=1)
    run = p.add_run(text)
    set_font(run, size=9.5, color=DARK)
    return p

def inline_tags(doc, items, indent=0):
    """One-line comma-separated tag row for skills."""
    p = doc.add_paragraph()
    para_space(p, before=1, after=2)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    run = p.add_run("  ·  ".join(items))
    set_font(run, size=9, color=DARK)
    return p

# ── Document setup ─────────────────────────────────────────────────────────────
doc = Document()

# Page margins — narrow for density
for section in doc.sections:
    section.page_height   = Cm(29.7)
    section.page_width    = Cm(21.0)
    section.top_margin    = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin   = Cm(2.0)
    section.right_margin  = Cm(2.0)

# Default paragraph style
style = doc.styles['Normal']
style.font.name = "Calibri"
style.font.size = Pt(10)

# ── NAME & CONTACT HEADER ──────────────────────────────────────────────────────
p_name = doc.add_paragraph()
para_space(p_name, before=0, after=2)
r = p_name.add_run("CEM KAYA")
set_font(r, name="Calibri", size=24, bold=True, color=NAVY)

p_title = doc.add_paragraph()
para_space(p_title, before=0, after=4)
r2 = p_title.add_run("Telecom & AI Engineer  ·  5G Core Networks  ·  AI/ML Systems  ·  Protocol Engineering")
set_font(r2, size=10.5, color=BLUE)

p_contact = doc.add_paragraph()
para_space(p_contact, before=0, after=2)
contact_parts = [
    "tcckaya8@gmail.com",
    "linkedin.com/in/cemkaya",
    "github.com/cem8kaya",
    "Istanbul, Turkey"
]
rc = p_contact.add_run("   |   ".join(contact_parts))
set_font(rc, size=9, color=MUTED)

add_hr(doc, color=NAVY)

# ── PROFESSIONAL SUMMARY ───────────────────────────────────────────────────────
section_heading(doc, "Professional Summary")
p_sum = doc.add_paragraph()
para_space(p_sum, before=2, after=4)
summary = (
    "Telecom & AI Engineer with 15+ years of hands-on experience across 5G/4G core networks, "
    "AI/ML systems, and protocol-level engineering. Proven track record at Odine Labs, B-YOND, "
    "and Turkcell delivering production-grade solutions for Verizon, AT&T, Vodafone, and Ooredoo. "
    "Deep expertise in 3GPP standards (TS 23.501/502, TS 29.244, TS 23.288), C++/Python protocol "
    "engineering, and applied ML — including multi-agent LLM orchestration, anomaly detection, "
    "and fine-tuned telecom LLMs. Builder of 9 open-source projects spanning 5G simulation, "
    "PFCP firewalls, DPI platforms, and iOS seismic detection."
)
rs = p_sum.add_run(summary)
set_font(rs, size=9.8, color=DARK)

# ── EXPERIENCE ─────────────────────────────────────────────────────────────────
section_heading(doc, "Professional Experience")

# Odine Labs
job_header(doc, "Solution Architect", "Odine Labs R&D", "Apr 2025 – Present", "Istanbul, Turkey")
for b in [
    "Architecting cloud-native AI/ML solutions using Kubernetes/OpenShift and GCP Vertex AI, "
    "enabling 40% faster model deployment cycles for R&D telco use cases.",
    "Designed and led development of a conversational AI chatbot and document analyzer using "
    "LangGraph multi-agent orchestration and FAISS-based RAG pipelines.",
    "Built a statistically rigorous synthetic telecom data generator (Gamma/Lognormal/Beta/Poisson "
    "distributions, ARIMA time series, 5 anomaly types) used for training ML models.",
    "Implemented V2X sidelink QoS prediction models with XGBoost and Neural Networks for connected "
    "mobility research.",
]:
    bullet(doc, b)

# B-YOND
job_header(doc, "Data Analyst & Scientist", "B-YOND", "Dec 2022 – Mar 2025", "Canada (Remote)")
for b in [
    "Developed mobility and connectivity prediction models for 5G Core and VoNR for Verizon, "
    "improving network reliability by 25%.",
    "Created EPC and 5GC predictive models for 4G-5G network migration for AT&T.",
    "Delivered real-time anomaly detection system handling millions of concurrent users during "
    "the FIFA World Cup 2023 (Ooredoo Qatar).",
    "Built automated VoLTE diagnostic models for Telenet and Vodafone Ziggo.",
    "Developed advanced protocol parsers for SIP, Diameter, GTPv2, HTTP/2, PFCP, and NGAP "
    "following the latest 3GPP specifications.",
]:
    bullet(doc, b)

# Turkcell
job_header(doc, "Senior Core Network Optimization Engineer", "Turkcell", "Sep 2019 – Feb 2022", "Istanbul, Turkey")
for b in [
    "Built network operation automation and anomaly detection software from scratch using Python, "
    "SQL, and JavaScript, reducing manual intervention by 70%.",
    "Implemented Meta Prophet ML models for predictive network performance forecasting.",
    "Led VoiceX project: full migration from legacy Ericsson/Huawei IMS to Mavenir architecture "
    "with zero service downtime.",
    "Integrated Ericsson ENM, Mavenir XA, and Huawei OSS platforms into a unified management layer.",
]:
    bullet(doc, b)

# Early Career
job_header(doc, "Core Network & VoIP Engineer", "Vodafone Turkey · VOTEL · Self-Employed · Turkcell", "2010 – 2019", "Turkey / Various")
for b in [
    "Managed critical voice network infrastructure serving millions of subscribers across multiple operators.",
    "Established VoIP consulting business; delivered solutions on Oracle ACME SBC, GENBAND, and Asterisk.",
]:
    bullet(doc, b)

# ── SKILLS ─────────────────────────────────────────────────────────────────────
section_heading(doc, "Technical Skills")

skills = [
    ("5G / Telecom Protocols",
     ["AMF", "SMF", "UPF", "AUSF/UDM/PCF", "NRF/NWDAF", "SIP", "DIAMETER",
      "GTPv1/v2", "PFCP", "NGAP/S1AP/X2AP", "NAS (LTE/5G)", "RTP/RTCP",
      "HTTP/2 (5G SBA)", "TS 23.501/502/503", "TS 23.288", "TS 29.244", "TS 33.501/513"]),
    ("AI / ML",
     ["LangGraph Multi-Agent", "RAG / FAISS", "QLoRA Fine-Tuning", "HuggingFace PEFT",
      "Isolation Forest", "DTW Pattern Matching", "Anomaly Detection", "Predictive Modeling"]),
    ("Languages",
     ["Python", "C++ (C++17)", "Swift", "JavaScript (ES6+)", "Bash", "SQL", "R"]),
    ("Frameworks & Tools",
     ["Open5GS", "UERANSIM", "Flask", "FastAPI", "Scapy", "CMake", "Docker",
      "Kubernetes", "libpcap", "nDPI", "OpenSSL"]),
    ("Cloud & Infra",
     ["GCP", "GCP Vertex AI", "Prometheus", "Grafana", "MongoDB", "OpenStack", "Jenkins/CI/CD"]),
    ("Mobile",
     ["iOS / Swift", "CoreMotion", "AVFoundation", "App Store", "On-Device ML"]),
]

for cat, items in skills:
    p = doc.add_paragraph()
    para_space(p, before=3, after=0)
    rl = p.add_run(cat + ": ")
    set_font(rl, size=9.5, bold=True, color=NAVY)
    ri = p.add_run("  ·  ".join(items))
    set_font(ri, size=9.5, color=DARK)

# ── PORTFOLIO HIGHLIGHTS ────────────────────────────────────────────────────────
section_heading(doc, "Open-Source Portfolio Highlights")

projects = [
    ("Open5GS AI/ML Laboratory",
     "Full 5G SA core (7 NFs) on GCP with UERANSIM. 8 labeled traffic scenarios, "
     "ETL pipeline, Isolation Forest / Random Forest. Documents the gtp5g kernel bypass."),
    ("Open5GS NWDAF — C++ Reference",
     "Standalone C++ NWDAF compliant with 3GPP TS 23.288 v17. All 7 analytics IDs, "
     "embedded Isolation Forest + EWMA, full TS 29.520 SBI REST API, systemd service."),
    ("Digital Twin RCA Agent",
     "LangGraph multi-agent system (Master + 3 specialists) for automated 5G RCA. "
     "DTW matching across 15 KPIs, FAISS RAG over 3GPP specs, LLM failover chain. "
     "<3 min MTRCA."),
    ("Callflow Visualizer — Enhanced DPI",
     "C++17 PCAP analyzer with 15+ protocol parsers (SIP/GTP/PFCP/NGAP/NAS/HTTP2). "
     "D3.js ladder diagrams, WebSocket streaming, JWT+RBAC. ~34,700 packets/sec."),
    ("5GC Secure CUPS Shield",
     "PFCP firewall per TS 29.244 / TS 33.513. HMAC-SHA256 auth, RSA signatures, "
     "DoS protection, dynamic threat scoring, lock-free atomic design."),
    ("5G LLM Engine",
     "QLoRA fine-tuned telecom LLM with FAISS RAG over 3GPP specs. FastAPI output "
     "with structured RCA + troubleshooting for AMF/SMF/UPF/IMS/GTPv2."),
]

for title, desc in projects:
    p = doc.add_paragraph()
    para_space(p, before=3, after=1)
    rt = p.add_run(title + "  —  ")
    set_font(rt, size=9.5, bold=True, color=NAVY)
    rd = p.add_run(desc)
    set_font(rd, size=9.5, color=DARK)

p_gh = doc.add_paragraph()
para_space(p_gh, before=3, after=2)
rg = p_gh.add_run("All projects: github.com/cem8kaya")
set_font(rg, size=9, color=MUTED, italic=True)

# ── EDUCATION & CERTIFICATIONS ─────────────────────────────────────────────────
section_heading(doc, "Education")

edu = [
    ("M.Sc. Management Information Systems", "Bilgi University", "Istanbul, Turkey"),
    ("B.Sc. Electronics and Communication Engineering", "Kocaeli University", "Turkey"),
]
for deg, school, loc in edu:
    p = doc.add_paragraph()
    para_space(p, before=3, after=1)
    r1 = p.add_run(deg + "  ·  ")
    set_font(r1, size=9.5, bold=True, color=NAVY)
    r2 = p.add_run(f"{school}, {loc}")
    set_font(r2, size=9.5, color=DARK)

section_heading(doc, "Certifications")
certs = [
    "IELTS 7.0 (Advanced English Proficiency)",
    "Nokia Vo5G Protocol Stack & Standards · IMS Protocols and Call Flows",
    "3GPP 5G Security Specification",
    "Business Analyst Certification — Udacity",
    "Python, Machine Learning & Data Visualization — Kaggle",
]
p_certs = doc.add_paragraph()
para_space(p_certs, before=2, after=2)
rc = p_certs.add_run("  ·  ".join(certs))
set_font(rc, size=9, color=DARK)

# ── Save ───────────────────────────────────────────────────────────────────────
out = "/home/user/kayacemcom/origresumes/Cem_Kaya_Resume_2026.docx"
doc.save(out)
print(f"Saved → {out}")
