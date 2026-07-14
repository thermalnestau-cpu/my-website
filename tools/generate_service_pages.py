#!/usr/bin/env python3
"""
Thermal Nest static page generator -- service pages.

Usage:
    python3 tools/generate_service_pages.py

Reads the SERVICES list below and writes one static HTML file per service
into /services/. To add a new service (or later, a city-specific variant),
duplicate a dict in SERVICES, edit the fields, and rerun this script. No
build step is required in production -- the output is plain static HTML.

Keep this script dependency-free (stdlib only) so it always runs with a
plain `python3`, no pip install needed.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICES_DIR = os.path.join(ROOT, "services")

SITE_URL = "https://thermalnest.com.au"

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared_style.css"), encoding="utf-8") as f:
    SHARED_CSS = f.read()

NAV_HTML = """
<nav id="navbar">
  <a href="/index.html" class="nav-logo">Thermal<span>Nest</span></a>
  <ul class="nav-links">
    <li><a href="/index.html">Home</a></li>
    <li><a href="/services/index.html">Services</a></li>
    <li><a href="/blog/index.html">Blog</a></li>
    <li><a href="/contact.html" class="nav-cta">Get a Quote</a></li>
  </ul>
  <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</nav>
"""

FOOTER_HTML = """
<footer>
  <div class="footer-top">
    <div class="footer-brand">
      <a href="/index.html" class="nav-logo">Thermal<span style="color:var(--sage)">Nest</span></a>
      <p>Accredited ESD consultants delivering fast, accurate energy compliance certificates nationwide across Australia.</p>
      <a href="tel:+61481361912" class="footer-contact-line">\U0001F4DE &nbsp;+61 481 361 912</a>
      <a href="mailto:hello@thermalnest.com.au" class="footer-contact-line">✉️ &nbsp;hello@thermalnest.com.au</a>
    </div>
    <div class="footer-col">
      <h4>Services</h4>
      <ul>
        <li><a href="/services/basix-certificate.html">BASIX Certificate</a></li>
        <li><a href="/services/nathers-assessment.html">NatHERS Assessment</a></li>
        <li><a href="/services/sustainable-design-assessment.html">Sustainable Design</a></li>
        <li><a href="/services/whole-of-home-assessment.html">Whole of Home (WoH)</a></li>
        <li><a href="/services/bess-assessment.html">BESS Reports</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <ul>
        <li><a href="/index.html">Home</a></li>
        <li><a href="/services/index.html">Services</a></li>
        <li><a href="/blog/index.html">Blog</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Thermal Nest. All rights reserved.</p>
    <p>Accredited ESD Consultants -- Nationwide Australia</p>
  </div>
</footer>
"""

WHY_US_HTML = """
      <h2>Why Work With Thermal Nest</h2>
      <p>We're accredited to operate in every Australian state and territory, so whether your project is in Sydney, Melbourne, Brisbane, Perth or regional Australia, you get the same turnaround and the same standard of report. Across 500+ projects, every certificate and report we've issued has been accepted on first submission -- no rejections, no rounds of council back-and-forth eating into your build timeline.</p>
      <p>We also work with your design team from early in the process rather than only stepping in once drawings are locked. Catching a compliance issue at concept stage costs a conversation; catching it after a DA is lodged costs a redesign. That's the gap we're built to close.</p>
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{canonical}" />

  <!-- Open Graph -->
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="{site_url}/office-lady.png" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />

  <!-- Schema: Service -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": "{service_type}",
    "provider": {{
      "@type": "ProfessionalService",
      "name": "Thermal Nest",
      "url": "{site_url}"
    }},
    "areaServed": {{ "@type": "Country", "name": "Australia" }},
    "description": "{schema_description}"
  }}
  </script>

  <!-- Schema: FAQPage -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{faq_schema}
    ]
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
{shared_css}
</head>
<body>
{nav}
<main>
  <section class="page-hero">
    <div class="page-hero-inner">
      <p class="breadcrumb"><a href="/index.html">Home</a> / <a href="/services/index.html">Services</a> / {name}</p>
      <h1>{h1}</h1>
      <p class="page-hero-lead">{lead}</p>
      <div class="page-hero-badges"><span>{badge}</span><span>Nationwide Coverage</span></div>
    </div>
  </section>

  <section class="prose-section">
{body}
  </section>

  <section class="faq-section">
    <div class="faq-inner">
      <h2 class="section-title">Frequently Asked Questions</h2>
{faq_html}
    </div>
  </section>

  <section class="related-links">
    <h3>Related Services</h3>
    <ul>
{related_links}
    </ul>
  </section>

  <section class="cta-band">
    <h2>Ready to Get Started?</h2>
    <p>Same-day quotes, accredited assessors, no surprises. Tell us about your project and we'll get back to you within one business day.</p>
    <a href="/contact.html" class="btn-primary">Request a Free Quote &rarr;</a>
  </section>
</main>
{footer}
</body>
</html>
"""


def faq_block(faqs):
    schema_items = []
    html_items = []
    for q, a in faqs:
        q_esc = q.replace('"', '\\"')
        a_esc = a.replace('"', '\\"')
        schema_items.append(
            '      {\n'
            '        "@type": "Question",\n'
            '        "name": "%s",\n'
            '        "acceptedAnswer": { "@type": "Answer", "text": "%s" }\n'
            '      }' % (q_esc, a_esc)
        )
        html_items.append(
            f'      <div class="faq-item">\n        <h3>{q}</h3>\n        <p>{a}</p>\n      </div>'
        )
    return ",\n".join(schema_items), "\n".join(html_items)


def related_links_block(slugs, all_services):
    by_slug = {s["slug"]: s for s in all_services}
    items = []
    for slug in slugs:
        s = by_slug[slug]
        items.append(f'      <li><a href="/services/{slug}.html">{s["name"]}</a></li>')
    return "\n".join(items)


def render(service, all_services):
    full_body = service["body"] + WHY_US_HTML
    faq_schema, faq_html = faq_block(service["faq"])
    related = related_links_block(service["related"], all_services)
    canonical = f'{SITE_URL}/services/{service["slug"]}.html'
    html = PAGE_TEMPLATE.format(
        title=service["title"],
        description=service["description"],
        canonical=canonical,
        site_url=SITE_URL,
        service_type=service["service_type"],
        schema_description=service["schema_description"],
        faq_schema=faq_schema,
        shared_css=SHARED_CSS,
        nav=NAV_HTML,
        name=service["name"],
        h1=service["h1"],
        lead=service["lead"],
        badge=service["badge"],
        body=full_body,
        faq_html=faq_html,
        related_links=related,
        footer=FOOTER_HTML,
    )
    assert len(service["title"]) <= 60, f'{service["slug"]}: title too long ({len(service["title"])})'
    assert len(service["description"]) <= 155, f'{service["slug"]}: description too long ({len(service["description"])})'
    assert html.count("<h1") == 1, f'{service["slug"]}: must have exactly one H1'
    return html


SERVICES = [
    {
        "slug": "basix-certificate",
        "name": "BASIX Certificate",
        "badge": "DA & CDC Required",
        "service_type": "BASIX Certificate",
        "title": "BASIX Certificate Consultant | Thermal Nest",
        "description": "Accredited BASIX certificates for NSW new builds, renovations and duplexes. 48-hour turnaround, same-day quotes, 100% approval rate.",
        "schema_description": "Accredited BASIX certificate assessments for new homes, renovations and multi-dwelling developments across NSW.",
        "h1": "BASIX Certificate Consultants, NSW-Wide",
        "lead": "Every new home, granny flat and major renovation in NSW needs a BASIX certificate before a DA or CDC can be lodged. We deliver accurate, fully compliant certificates in as little as 48 hours.",
        "related": ["nathers-assessment", "basix-certificate-sydney"],
        "body": """
      <h2>What Is a BASIX Certificate?</h2>
      <p>BASIX (Building Sustainability Index) is a NSW Government requirement that's been part of the planning process since 2004. It confirms that your home or renovation meets minimum targets for thermal comfort, energy efficiency and water conservation before council will accept your Development Application (DA) or Complying Development Certificate (CDC).</p>
      <p>An accredited assessor enters your project details -- location, floor area, orientation, insulation, glazing, appliances and water fixtures -- into the NSW Planning Portal's BASIX tool, which calculates whether your design hits the required targets. If it does, the certificate is issued. If it doesn't, we'll tell you exactly what to change -- usually insulation, glazing or a rainwater tank -- to get there.</p>

      <h2>Who Needs a BASIX Certificate?</h2>
      <p>If you're building or significantly renovating a residential property in NSW, you almost certainly need one:</p>
      <ul>
        <li><strong>New homes</strong> -- single-storey, double-storey, knockdown-rebuilds and custom builds</li>
        <li><strong>Granny flats and secondary dwellings</strong> -- required over 60m&sup2;, sometimes exempt below that</li>
        <li><strong>Major renovations</strong> -- alterations and additions valued over $50,000</li>
        <li><strong>Duplexes, townhouses and multi-dwelling developments</strong> -- with targets that differ from single dwellings</li>
      </ul>

      <h2>How We Deliver It</h2>
      <p>Send us your architectural drawings -- floor plan, elevations, window schedule and site plan -- and we'll respond with a same-day quote. Our accredited assessors then run the assessment and issue your certificate, typically within 48 hours of receiving complete plans. Urgent same-day turnarounds are available when your DA deadline is tight.</p>
      <p>Every certificate we issue is lodged as commitments your builder is legally required to follow, and we make sure the report is structured exactly the way your council expects -- no back-and-forth, no resubmissions.</p>

      <div class="info-band">
        <h3>Pricing</h3>
        <p>BASIX pricing depends on dwelling type and project complexity. Get in touch for a same-day, no-obligation quote tailored to your plans.</p>
        <a href="/contact.html" class="btn-outline-dark">Get a Free Quote &rarr;</a>
      </div>
""",
        "faq": [
            ("Do I need a BASIX certificate for a granny flat?",
             "Standalone granny flats and secondary dwellings over 60 square metres need a BASIX certificate. Smaller structures may be exempt in some cases -- send us your plans and we'll confirm."),
            ("How long does a BASIX certificate take?",
             "With complete architectural drawings, we typically issue your certificate within 48 hours. Same-day turnaround is available for urgent DA deadlines."),
            ("What's the difference between BASIX and NatHERS?",
             "BASIX is a NSW-specific assessment covering energy, water and thermal comfort. NatHERS is a more detailed national thermal performance rating. You can meet BASIX's thermal comfort requirement via a full NatHERS assessment or the BASIX prescriptive pathway."),
            ("What happens if my design doesn't meet the BASIX targets?",
             "We'll recommend specific adjustments -- typically insulation upgrades, different glazing, or adding a rainwater tank -- to bring your design into compliance before the certificate is issued."),
            ("Can I change my design after the certificate is issued?",
             "Any change that affects your BASIX commitments, such as swapping windows or your hot water system, requires an amended certificate. Let us know before you proceed so your DA stays valid."),
        ],
    },
    {
        "slug": "nathers-assessment",
        "name": "NatHERS Assessment",
        "badge": "Nationwide",
        "service_type": "NatHERS Assessment",
        "title": "NatHERS Assessment | Thermal Nest",
        "description": "Accredited NatHERS star rating assessments for new homes and renovations Australia-wide, using AccuRate and FirstRate5 software.",
        "schema_description": "Nationwide House Energy Rating Scheme (NatHERS) thermal performance assessments for residential projects across Australia.",
        "h1": "NatHERS Assessments, Nationwide",
        "lead": "NatHERS rates how well your home's design retains comfortable temperatures, on a scale of 0 to 10 stars. It's required for new homes and major renovations across every Australian state and territory.",
        "related": ["basix-certificate", "nathers-assessor-sydney"],
        "body": """
      <h2>What Is a NatHERS Assessment?</h2>
      <p>The Nationwide House Energy Rating Scheme (NatHERS) measures the thermal performance of your home's building fabric -- walls, roof, floor and windows -- independent of any heating or cooling appliances. Using accredited software (AccuRate or FirstRate5), an assessor models your design against your specific climate zone and orientation to produce a star rating from 0 to 10.</p>
      <p>The higher the rating, the less energy your home will need to stay comfortable year-round. Most Australian states now require a minimum 7-star NatHERS rating for new homes under the National Construction Code (NCC 2022), up from the previous 6-star minimum.</p>

      <h2>Who Needs a NatHERS Assessment?</h2>
      <ul>
        <li><strong>New home builds</strong> -- required in every state and territory before construction approval</li>
        <li><strong>Major renovations and extensions</strong> -- where thermal performance of the altered area is assessed</li>
        <li><strong>Multi-unit developments</strong> -- townhouses, duplexes and apartments each need individual ratings</li>
        <li><strong>NSW projects choosing the NatHERS pathway</strong> -- as an alternative to the BASIX prescriptive method for thermal comfort</li>
      </ul>

      <h2>How We Deliver It</h2>
      <p>Send through your floor plans, elevations, window schedule and site details, and we'll model your design in accredited software to determine your star rating. If your design falls short of the target, we'll identify the most cost-effective changes -- often glazing specification, insulation, or shading -- to get you there without over-engineering the build.</p>
      <p>Because we're accredited to operate nationwide, we understand how climate zone data and council requirements shift from Sydney to Perth to regional Queensland, so your rating is calculated correctly the first time.</p>

      <div class="info-band">
        <h3>Pricing</h3>
        <p>NatHERS pricing varies by dwelling size and complexity. Get in touch for a same-day, no-obligation quote.</p>
        <a href="/contact.html" class="btn-outline-dark">Get a Free Quote &rarr;</a>
      </div>
""",
        "faq": [
            ("What star rating do I need?",
             "Most states now require a minimum 7-star NatHERS rating for new homes under NCC 2022, though some councils and the Whole of Home framework may require more. We'll confirm the exact target for your location."),
            ("Is NatHERS the same as BASIX?",
             "No. NatHERS is a national thermal performance rating; BASIX is a broader NSW-specific assessment covering energy, water and thermal comfort. A NatHERS assessment can be used to satisfy BASIX's thermal comfort requirement."),
            ("Does a renovation need a NatHERS assessment?",
             "Major renovations and extensions often need an assessment of the altered area, depending on your state and council requirements. Send us your plans and we'll confirm."),
            ("How can I improve a low star rating?",
             "Common improvements include better window glazing, increased ceiling and wall insulation, improved orientation of glazing, and external shading. We'll recommend the most cost-effective combination for your design."),
            ("How long does a NatHERS assessment take?",
             "With complete plans, most assessments are completed within a few business days. Let us know your deadline and we'll confirm a turnaround when you request your quote."),
        ],
    },
    {
        "slug": "sustainable-design-assessment",
        "name": "Sustainable Design Assessment",
        "badge": "Council Compliance",
        "service_type": "Sustainable Design Assessment",
        "title": "Sustainable Design Assessment (SDA) | Thermal Nest",
        "description": "Sustainable Design Assessments for council-required developments, covering energy, water, waste and biodiversity across Australia.",
        "schema_description": "Sustainable Design Assessments (SDA) evaluating energy, water, waste and biodiversity outcomes for council-required developments.",
        "h1": "Sustainable Design Assessments (SDA)",
        "lead": "Many Australian councils require a Sustainable Design Assessment for medium-to-large developments, evaluating energy, water, waste and biodiversity outcomes before approval.",
        "related": ["bess-assessment", "whole-of-home-assessment"],
        "body": """
      <h2>What Is a Sustainable Design Assessment?</h2>
      <p>A Sustainable Design Assessment (SDA) is a council-level planning requirement, most commonly seen across Victorian councils, for medium-to-large residential and mixed-use developments. Unlike single-issue assessments, an SDA takes a whole-of-project view: energy performance, water efficiency, waste management, indoor environment quality, transport and biodiversity impact are all evaluated against council-specific benchmarks.</p>
      <p>The assessment is submitted alongside your planning application (often called a Sustainable Design Assessment or Sustainability Management Plan, depending on the council) and demonstrates that your development meets local sustainability policy before a permit is issued.</p>

      <h2>Who Needs an SDA?</h2>
      <ul>
        <li><strong>Multi-unit residential developments</strong> -- apartments, townhouse developments and larger subdivisions</li>
        <li><strong>Mixed-use developments</strong> -- where council sustainability policy applies to the whole site</li>
        <li><strong>Commercial and institutional projects</strong> -- subject to local environmentally sustainable design policy</li>
        <li><strong>Any development where council has flagged an SDA as a condition</strong> of a planning permit application</li>
      </ul>
      <p>Not every project needs one -- it depends on your council and the scale of your development. If you're unsure, send us your plans and we'll confirm what's required before you submit.</p>

      <h2>How We Deliver It</h2>
      <p>We work with your architect and design team from early in the process to identify what your specific council expects, then prepare a report addressing each category -- energy, water, waste, indoor environment quality, transport and biodiversity -- with the evidence and calculations needed to satisfy the assessing planner. Getting this right at design stage avoids costly redesigns after a permit application is lodged.</p>

      <div class="info-band">
        <h3>Pricing</h3>
        <p>SDA pricing depends on development scale and council requirements. Get in touch for a same-day, no-obligation quote.</p>
        <a href="/contact.html" class="btn-outline-dark">Get a Free Quote &rarr;</a>
      </div>
""",
        "faq": [
            ("Which councils require a Sustainable Design Assessment?",
             "SDAs are most commonly required by Victorian councils for medium-to-large developments, though requirements vary by local sustainability policy. We'll confirm what your specific council expects."),
            ("What does an SDA actually assess?",
             "A typical SDA covers energy performance, water efficiency, waste management, indoor environment quality, transport and biodiversity impact, each benchmarked against council policy."),
            ("Is an SDA the same as a BESS report?",
             "They're related but distinct -- BESS is a specific scorecard tool used by many Victorian councils, while 'Sustainable Design Assessment' is a broader category of report some councils require in a different format. We'll confirm which applies to your project."),
            ("When should I get an SDA started?",
             "As early as possible -- ideally alongside your architect at concept design stage, so sustainability requirements shape the design rather than being retrofitted after a permit application is knocked back."),
            ("Does my project definitely need one?",
             "Not every development does -- it depends on scale, location and council policy. Send us your plans and we'll tell you plainly whether an SDA applies."),
        ],
    },
    {
        "slug": "whole-of-home-assessment",
        "name": "Whole of Home (WoH) Assessment",
        "badge": "NCC 2022 Compliant",
        "service_type": "Whole of Home Assessment",
        "title": "Whole of Home (WoH) Assessment | Thermal Nest",
        "description": "Whole of Home assessments under NCC 2022, covering total household energy use for new homes and major renovations nationwide.",
        "schema_description": "Whole of Home (WoH) assessments evaluating total household energy budget under NCC 2022 for new homes and renovations across Australia.",
        "h1": "Whole of Home (WoH) Assessments",
        "lead": "Whole of Home is the newest national energy standard, mandated under NCC 2022. It assesses your home's total energy budget -- not just the building shell -- covering appliances, hot water and on-site energy generation.",
        "related": ["nathers-assessment", "basix-certificate"],
        "body": """
      <h2>What Is a Whole of Home Assessment?</h2>
      <p>Introduced as part of NCC 2022 and mandatory nationally since 2023, the Whole of Home (WoH) framework looks beyond the building fabric that NatHERS assesses and evaluates your home's total annual energy budget. That means heating and cooling, hot water systems, lighting, cooking appliances and any on-site renewable generation like solar PV are all scored together against a national benchmark.</p>
      <p>A WoH assessment produces a score out of 100, with most jurisdictions requiring a minimum threshold alongside your NatHERS star rating. The two work together: NatHERS covers how well your home retains temperature, WoH covers how efficiently the whole household runs.</p>

      <h2>Who Needs a Whole of Home Assessment?</h2>
      <ul>
        <li><strong>New homes</strong> -- required nationally alongside NatHERS under NCC 2022</li>
        <li><strong>Major alterations and additions</strong> -- where NCC 2022 energy provisions apply to the works</li>
        <li><strong>Multi-dwelling developments</strong> -- townhouses, duplexes and apartment developments</li>
        <li><strong>Projects specifying solar, heat pumps or all-electric systems</strong> -- where WoH can demonstrate the efficiency benefit</li>
      </ul>

      <h2>How We Deliver It</h2>
      <p>We assess your specified appliances, hot water system, lighting and any on-site generation alongside your NatHERS model to produce a compliant WoH score. Where your initial specification falls short, we'll recommend targeted changes -- often a more efficient hot water system or added solar capacity -- that lift your score without blowing out your build cost.</p>
      <p>Because WoH and NatHERS are assessed together, ordering both from the same team keeps your energy compliance consistent and avoids the back-and-forth of two separate assessors working from different assumptions.</p>

      <div class="info-band">
        <h3>Pricing</h3>
        <p>WoH pricing depends on project scope and whether it's bundled with a NatHERS assessment. Get in touch for a same-day, no-obligation quote.</p>
        <a href="/contact.html" class="btn-outline-dark">Get a Free Quote &rarr;</a>
      </div>
""",
        "faq": [
            ("Is Whole of Home the same as NatHERS?",
             "No, but they're assessed together. NatHERS rates the building fabric's thermal performance; Whole of Home scores the total household energy budget, including appliances, hot water and on-site generation."),
            ("Do I need a Whole of Home assessment for a renovation?",
             "Major alterations and additions where NCC 2022 energy provisions apply typically need one. Send us your plans and we'll confirm whether your renovation is in scope."),
            ("What's a good Whole of Home score?",
             "Requirements vary by jurisdiction and dwelling type -- we'll confirm the exact threshold that applies to your project and location."),
            ("Can solar panels improve my Whole of Home score?",
             "Yes -- on-site renewable generation like solar PV is factored into the total household energy budget and can meaningfully improve your score."),
            ("Can you assess NatHERS and Whole of Home together?",
             "Yes, we typically deliver both together since they draw on the same building model, which keeps your energy compliance consistent and can reduce turnaround time."),
        ],
    },
    {
        "slug": "bess-assessment",
        "name": "BESS Assessment & Reports",
        "badge": "Multi-Unit & Commercial",
        "service_type": "BESS Assessment",
        "title": "BESS Assessment & Reports | Thermal Nest",
        "description": "BESS (Built Environment Sustainability Scorecard) reports for Victorian council developments, prepared by accredited assessors.",
        "schema_description": "Built Environment Sustainability Scorecard (BESS) assessments and reports for multi-unit and commercial developments across Victoria.",
        "h1": "BESS Assessments & Reports",
        "lead": "BESS -- the Built Environment Sustainability Scorecard -- is the online tool used by many Victorian councils to assess a development's sustainability performance before a planning permit is issued.",
        "related": ["sustainable-design-assessment", "whole-of-home-assessment"],
        "body": """
      <h2>What Is a BESS Report?</h2>
      <p>BESS is a free online scorecard tool, developed by the Council Alliance for a Sustainable Built Environment (CASBE), used by most Victorian councils to score a development across categories including energy, water, stormwater, waste, transport, urban ecology, indoor environment quality and innovation. Councils typically require a minimum overall score -- often around 50% -- before a permit application will be considered complete.</p>
      <p>The report is submitted alongside your planning application and needs to reflect exactly what's shown on your architectural drawings, so any changes made during design review need to be re-checked against the scorecard.</p>

      <h2>Who Needs a BESS Report?</h2>
      <ul>
        <li><strong>Multi-unit residential developments</strong> -- apartments, townhouse developments and larger subdivisions in Victoria</li>
        <li><strong>Commercial developments</strong> -- subject to council ESD policy</li>
        <li><strong>Mixed-use developments</strong> -- where council sustainability conditions apply to the whole site</li>
        <li><strong>Any project where your Victorian council has listed BESS as a permit requirement</strong></li>
      </ul>

      <h2>How We Deliver It</h2>
      <p>We work directly with your architect and design team to score your development against each BESS category, identify the fastest path to your council's minimum threshold, and prepare a submission-ready report with the supporting evidence assessors expect. Where your initial design falls short, we'll flag the lowest-cost changes -- often around energy efficiency or water fixtures -- that lift your score without a major redesign.</p>
      <p>Because BESS scores are checked against your architectural drawings at multiple stages, we stay involved through design development, not just at the initial submission, so your score doesn't drift out of compliance as the design evolves.</p>

      <div class="info-band">
        <h3>Pricing</h3>
        <p>BESS pricing depends on development scale and category count. Get in touch for a same-day, no-obligation quote.</p>
        <a href="/contact.html" class="btn-outline-dark">Get a Free Quote &rarr;</a>
      </div>
""",
        "faq": [
            ("What score do I need to pass BESS?",
             "Most Victorian councils require a minimum overall score, commonly around 50%, though the exact threshold and category minimums vary by council. We'll confirm the target for your site."),
            ("Is BESS required outside Victoria?",
             "BESS is a Victorian tool used by most councils across the state. Other states use different assessment types -- we'll confirm which applies if your project is interstate."),
            ("What happens if my design doesn't meet the BESS threshold?",
             "We'll identify the most cost-effective changes -- often energy efficiency measures or water-saving fixtures -- needed to lift your score before you submit."),
            ("Does BESS need to be resubmitted if my design changes?",
             "Yes -- your BESS report needs to reflect what's on your current architectural drawings, so material design changes should be re-checked against the scorecard."),
            ("Can you handle BESS and Sustainable Design Assessment together?",
             "Yes, many Victorian projects need both. We can prepare them together so your evidence and assumptions stay consistent across both reports."),
        ],
    },
    {
        "slug": "nathers-assessor-sydney",
        "name": "NatHERS Assessor Sydney",
        "badge": "Sydney-Wide",
        "service_type": "NatHERS Assessment",
        "title": "NatHERS Assessor Sydney | Thermal Nest",
        "description": "Accredited NatHERS assessor covering Greater Sydney. Same-day quotes, fast turnaround, 7-star ratings for new homes and renovations.",
        "schema_description": "Accredited NatHERS star rating assessments for new homes, renovations and multi-dwelling developments across Greater Sydney.",
        "h1": "NatHERS Assessor, Sydney",
        "lead": "Every new home and major renovation across Greater Sydney needs a NatHERS star rating under NCC 2022. We're accredited assessors delivering accurate ratings with a same-day quote.",
        "related": ["basix-certificate-sydney", "whole-of-home-assessment"],
        "body": """
      <h2>NatHERS Assessments for Sydney Projects</h2>
      <p>Most new homes and major renovations across Sydney now need a minimum 7-star NatHERS rating under NCC 2022, whether you're building in the Inner West, the Northern Beaches, or out toward Penrith and the Hawkesbury. We model your design in accredited software (AccuRate or FirstRate5) against the correct climate data for your specific location and produce the star rating your council and certifier need to see.</p>
      <p>Climate matters more than people expect here. Western Sydney suburbs run noticeably hotter through summer than the coastal and inner-city areas, which changes what actually works in a design -- glazing choice, insulation levels and shading that suit a Bondi renovation won't necessarily be the right call for a new build in Penrith. We factor your specific location's climate data into the assessment rather than applying a one-size-fits-all Sydney average.</p>

      <h2>Who Needs a NatHERS Rating in Sydney?</h2>
      <ul>
        <li><strong>New home builds</strong> -- required before construction approval, anywhere across Greater Sydney</li>
        <li><strong>Knockdown-rebuilds</strong> -- a common project type across established Sydney suburbs with ageing housing stock</li>
        <li><strong>Major renovations and extensions</strong> -- where the altered area needs its own thermal assessment</li>
        <li><strong>Townhouse, duplex and apartment developments</strong> -- increasingly common across Sydney's middle-ring suburbs, each dwelling assessed individually</li>
      </ul>

      <h2>How We Deliver It</h2>
      <p>Send through your floor plans, elevations, window schedule and site details and we'll respond with a same-day quote. Once we have complete plans, most Sydney assessments are turned around within a few business days. If your design falls short of the target rating, we'll recommend the most cost-effective fix for your specific suburb's climate -- often glazing, insulation or shading -- rather than an expensive blanket upgrade.</p>

      <div class="info-band">
        <h3>Pricing</h3>
        <p>NatHERS pricing for Sydney projects varies by dwelling size and complexity. Get in touch for a same-day, no-obligation quote.</p>
        <a href="/contact.html" class="btn-outline-dark">Get a Free Quote &rarr;</a>
      </div>
""",
        "faq": [
            ("Does my star rating requirement change depending on where in Sydney I'm building?",
             "The minimum rating (typically 7 stars under NCC 2022) is generally consistent, but what it takes to achieve that rating changes with your local climate. Western Sydney's hotter summers usually need different glazing and shading choices than coastal or inner-city Sydney."),
            ("Is NatHERS the same as BASIX?",
             "No. NatHERS is a national thermal performance rating for the building fabric; BASIX is a broader NSW-specific assessment covering energy, water and thermal comfort, and is required for every Sydney project alongside or instead of a standalone NatHERS assessment. We handle both together."),
            ("Do Sydney apartments and townhouses need individual NatHERS ratings?",
             "Yes -- each dwelling in a multi-unit development typically needs its own rating, even within the same building."),
            ("How long does a NatHERS assessment take for a Sydney project?",
             "With complete plans, most assessments are completed within a few business days. Let us know your DA deadline and we'll confirm a turnaround with your quote."),
            ("Can you assess a renovation in an established Sydney suburb?",
             "Yes -- knockdown-rebuilds and major renovations are some of the most common projects we assess across Sydney's established suburbs. Send us your plans and we'll confirm what's required."),
        ],
    },
    {
        "slug": "basix-certificate-sydney",
        "name": "BASIX Certificate Sydney",
        "badge": "DA & CDC Required",
        "service_type": "BASIX Certificate",
        "title": "BASIX Certificate Consultant Sydney | Thermal Nest",
        "description": "Accredited BASIX certificates for Sydney new builds, renovations and duplexes. 48-hour turnaround, same-day quotes, 100% approval rate.",
        "schema_description": "Accredited BASIX certificate assessments for new homes, renovations and multi-dwelling developments across Greater Sydney.",
        "h1": "BASIX Certificate Consultant, Sydney",
        "lead": "Every Sydney council requires a BASIX certificate before a DA or CDC will be accepted. We deliver accurate, fully compliant certificates for Sydney projects in as little as 48 hours.",
        "related": ["nathers-assessor-sydney", "whole-of-home-assessment"],
        "body": """
      <h2>BASIX Certificates for Sydney Councils</h2>
      <p>BASIX applies the same way across every council in Greater Sydney -- from the City of Sydney to Blacktown, Sutherland Shire to the Northern Beaches -- because it's a NSW Government requirement administered through the state's Planning Portal, not set by individual councils. What changes from project to project isn't the rules, it's the plans: a terrace renovation in the Inner West faces different constraints than a new knockdown-rebuild in Western Sydney, and we work with both regularly.</p>
      <p>An accredited assessor enters your project details -- location, floor area, orientation, insulation, glazing, appliances and water fixtures -- into the BASIX tool, which calculates whether your design meets the required targets. If it does, the certificate is issued. If it doesn't, we'll tell you exactly what to change to get there.</p>

      <h2>Who Needs a BASIX Certificate in Sydney?</h2>
      <ul>
        <li><strong>New homes</strong> -- single-storey, double-storey, knockdown-rebuilds and custom builds, common across established Sydney suburbs</li>
        <li><strong>Granny flats and secondary dwellings</strong> -- a fast-growing project type across Sydney given local housing pressure, required over 60m&sup2;</li>
        <li><strong>Major renovations</strong> -- alterations and additions valued over $50,000, from terrace extensions to full rebuilds</li>
        <li><strong>Duplexes, townhouses and multi-dwelling developments</strong> -- increasingly common across Sydney's middle-ring suburbs</li>
      </ul>

      <h2>How We Deliver It</h2>
      <p>Send us your architectural drawings and we'll respond with a same-day quote, wherever in Sydney your project sits. Our accredited assessors then run the assessment and issue your certificate, typically within 48 hours of receiving complete plans -- with urgent same-day options available when your DA deadline is tight.</p>

      <div class="info-band">
        <h3>Pricing</h3>
        <p>BASIX pricing for Sydney projects depends on dwelling type and project complexity. Get in touch for a same-day, no-obligation quote tailored to your plans.</p>
        <a href="/contact.html" class="btn-outline-dark">Get a Free Quote &rarr;</a>
      </div>
""",
        "faq": [
            ("Does BASIX work differently between Sydney councils?",
             "No -- BASIX is a NSW Government scheme administered through the state Planning Portal, so the requirement itself is consistent across every Sydney council. What differs is your specific site and design, which is what we assess."),
            ("Do I need a BASIX certificate for a granny flat in Sydney?",
             "Standalone granny flats and secondary dwellings over 60 square metres need a BASIX certificate. Given how common granny flats have become across Sydney, this catches a lot of projects -- send us your plans and we'll confirm."),
            ("How long does a BASIX certificate take for a Sydney project?",
             "With complete architectural drawings, we typically issue your certificate within 48 hours. Same-day turnaround is available for urgent DA deadlines."),
            ("Can you handle a knockdown-rebuild in an established Sydney suburb?",
             "Yes, knockdown-rebuilds are one of the most common project types we assess across Sydney's established suburbs."),
            ("What's the difference between BASIX and NatHERS for my Sydney project?",
             "BASIX is the broader NSW-specific assessment covering energy, water and thermal comfort; NatHERS is the national thermal performance rating that can satisfy BASIX's thermal comfort requirement. We deliver both together when needed."),
        ],
    },
]


def main():
    os.makedirs(SERVICES_DIR, exist_ok=True)
    for service in SERVICES:
        html = render(service, SERVICES)
        out_path = os.path.join(SERVICES_DIR, f'{service["slug"]}.html')
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        full_text = service["body"] + WHY_US_HTML
        for q, a in service["faq"]:
            full_text += " " + q + " " + a
        words = len(re.sub("<[^>]+>", " ", full_text).split())
        print(f'wrote {out_path} ({words} words in body)')


if __name__ == "__main__":
    main()
