"""Builds index.html (EN) and fr/index.html (FR) from one template.

Run from the repository root:  python3 _src/build.py .
"""
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

PLUS = ('<svg class="plus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>')

LAMP = """<button class="lamp" id="lamp" type="button" aria-label="{label}">
      <svg width="44" height="96" viewBox="0 0 44 96" aria-hidden="true">
        <g class="swing">
        <line class="cord" x1="22" y1="0" x2="22" y2="34"/>
        <g class="hang">
          <ellipse class="glow" cx="22" cy="62" rx="20" ry="14" filter="url(#lamp-blur)"/>
          <rect class="shade" x="19" y="33" width="6" height="5" rx="1.5"/>
          <path class="shade" d="M9 52 C9 43 14.5 37 22 37 C29.5 37 35 43 35 52 Z"/>
          <circle class="bulb" cx="22" cy="54" r="4.5"/>
        </g>
        </g>
        <defs><filter id="lamp-blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter></defs>
      </svg>
    </button>"""


def stage(d):
    """The material recovery app, drawn to Stageshow's rules: real words only on
    the decisions and the total, filler bars for the item names, one big number."""
    s = d["stage"]
    rows = "".join(
        f'<div class="r"><div class="bar" style="width:{w}%"></div><div class="bar" style="width:{q}%"></div>'
        f'<span class="chip{" scrap" if k == "scrap" else ""}">{s[k]}</span></div>'
        for w, q, k in [(62, 70, "site"), (45, 50, "scrap"), (72, 60, "ret"), (54, 80, "site")])
    rows += '<div class="r"><div class="bar" style="width:48%"></div><div class="bar" style="width:55%"></div><span></span></div>'
    ones = "".join(f"<b>{n}</b>" for n in list(range(10)) + [0])
    tens = "".join(f"<b>{n}</b>" for n in range(10))
    return f"""<div class="stage" role="img" aria-label="{s['aria']}">
            <div class="win">
              <div class="win-bar"><i></i><i></i><i></i><span>{s['title']}</span></div>
              <div class="win-body">
                <div class="win-rows">{rows}</div>
                <div class="win-total">
                  <span class="lbl">{s['label']}</span>
                  <span class="num"><span class="cur">EGP</span><span class="digits"><span class="dg"><span data-to="1">{tens}</span></span><span class="dg"><span data-to="10">{ones}</span></span><span>M</span></span></span>
                  <span class="sub">{s['sub']}</span>
                </div>
              </div>
            </div>
          </div>"""


def wt(text):
    return f'<span class="wt"><span class="ghost" aria-hidden="true">{text}</span><span class="live">{text}</span></span>'


def item(i, title, org, when, summary, bullets, extra=""):
    org_html = f' <span class="org">· {org}</span>' if org else ""
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""        <li>
          <button class="item-head" type="button" aria-expanded="false" aria-controls="p{i}">
            <span class="t">{wt(title)}{org_html}</span><time>{when}</time>{PLUS}
            <span class="sum">{summary}</span>
          </button>
          <div class="panel" id="p{i}"><div><div class="panel-in">
            <ul>{lis}</ul>{extra}
          </div></div></div>
        </li>"""


EN = dict(
    lang="en", base="", title="Alain Halbouny · Mechanical Engineer",
    desc="Alain Halbouny: mechanical engineer (McGill), MEP engineer at Rowad Modern Engineering and co-founder of IQASE.",
    role="Mechanical Engineer",
    lede="MEP engineer at Rowad in Cairo and co-founder of IQASE. I design hardware and build the software around it with AI.",
    cv="cv/Alain_Halbouny_CV.pdf", lamp="Pull the cord to switch light and dark", en_href="./", fr_href="fr/",
    h_exp="Experience", h_proj="Projects", h_edu="Education", h_skills="Skills",
    stage=dict(title="Aging stock", site="To site", scrap="Scrap", ret="Return", label="Recovered",
               sub="First 20% of 1,400 SKUs, 2× book value",
               aria="The material recovery app: each idle item gets a decision, to site, scrap or return, and the recovered total reaches EGP 10M."),
    exp=[
        ("MEP Engineer", "Rowad Modern Engineering", "2026 – now",
         "Arena pre-construction, MEP site work, and EGP 10M recovered from idle stock.",
         ["Pre-construction of a large indoor multipurpose arena: MEP planning, design coordination, procurement and submittal review.",
          "Site work across HVAC, fire-fighting, plumbing and electrical: inspections, QC, commissioning and handover.",
          "Aging material recovery: 1,400 SKUs idle in the main warehouse. EGP 10M recovered from the first 20%, twice book value, through scrap sales, site use and supplier returns.",
          "Built the multi-user web app that runs it with Claude: inventory, QC, decisions, audit trail and dashboards. 1,600+ commits in 6 weeks with an AI agent workflow; live ERP data and a company-wide rollout next.",
          "Member of the Supply Chain Committee."], True),
        ("Co-Founder", "IQASE", "2025 – now",
         "Phone accessories, from CAD and manufacturing to market.",
         ["Designed the products and production-ready CAD; prototyping a new line.",
          "Managing manufacturing with suppliers in China; the mold for the first run is being cut.",
          "Built the financial model (unit cost, pricing, margins) and run the budget and P&amp;L.",
          "Leading go-to-market across MENA: branding, digital marketing, distribution."], False),
    ],
    earlier="<b>Earlier:</b> V12 F1 Store, Montreal (2023) · GVI, Costa Rica (2019) · ABB &amp; GTAT, Cairo (2019) · GoPro at ABM, Dubai (2017)",
    proj=[
        ("Laser-Powered Rocket", "", "2024", "Laser thermal propulsion rig: 50 bar, 15,000 K plasma, measurable thrust.",
         ["Aluminum ionization chamber rated for 50 bar, run on a 350&nbsp;W continuous laser for up to 30&nbsp;s.",
          "First-principles heat transfer study for the plasma core: heat sinks and regenerative cooling.",
          "DFMA CAD and GD&amp;T drawings in SolidWorks; led prototyping and machining.",
          "Delivered in 6 months on budget; passed structural tests and produced thrust."]),
        ("Machine Learning", "", "2025 – now", "Neural network from scratch in NumPy; now a small transformer.",
         ["Multi-layer perceptron written from scratch in NumPy, trained on MNIST handwritten digits.",
          "Now building a small transformer language model to learn attention from the ground up."]),
        ("Transmission Box", "", "2022", "AGMA spur gearbox for a small aircraft.",
         ["Double-reduction spur gear transmission to the AGMA standard.",
          "Force, stress and fatigue analysis; shafts, bearings and keys sized over their life.",
          "Iterated the design with Python scripts and custom spreadsheets."]),
        ("Structural Bracket", "", "2022", "FEA-optimized acrylic bracket in Abaqus.",
         ["Lightweight 2D acrylic bracket for maximum strength at a target stiffness.",
          "FEA in Abaqus calibrated with material test data; DXF files for laser cutting."]),
    ],
    edu=("B.Eng. Mechanical Engineering", "McGill University", "2020 – 2025", "GPA 3.6, two scholarships.",
         ["Professor Bill Williams Memorial and John Howard Ambrose Scholarships, 2020–2021.",
          "Coursework: thermodynamics, mechanical design, fluid mechanics, DFMA, GD&amp;T, heat transfer, subsonic aerodynamics."]),
    skills=[
        "<b>Engineering:</b> SolidWorks, Mastercam, Abaqus, DFMA, GD&amp;T, CNC, 3D printing",
        "<b>Software:</b> Python, MATLAB, AI agent workflows (Claude)",
        "<b>Languages:</b> French, English, Arabic",
    ],
)

FR = dict(
    lang="fr", base="../", title="Alain Halbouny · Ingénieur mécanique",
    desc="Alain Halbouny : ingénieur mécanique (McGill), ingénieur MEP chez Rowad Modern Engineering et co-fondateur d'IQASE.",
    role="Ingénieur mécanique",
    lede="Ingénieur MEP chez Rowad au Caire et co-fondateur d'IQASE. Je conçois du matériel et je développe les logiciels autour, avec l'IA.",
    cv="../cv/Alain_Halbouny_CV_FR.pdf", lamp="Tirez le cordon pour passer du clair au sombre", en_href="../", fr_href="./",
    h_exp="Expérience", h_proj="Projets", h_edu="Formation", h_skills="Compétences",
    stage=dict(title="Stocks dormants", site="Chantier", scrap="Ferraille", ret="Retour", label="Récupérés",
               sub="Premiers 20&nbsp;% de 1&nbsp;400 références, 2× la valeur comptable",
               aria="L'application de valorisation des stocks : chaque article reçoit une décision, chantier, ferraille ou retour, et le total récupéré atteint 10&nbsp;M&nbsp;EGP."),
    exp=[
        ("Ingénieur MEP", "Rowad Modern Engineering", "2026 – présent",
         "Pré-construction d'une arène, travaux MEP sur chantier et 10&nbsp;M&nbsp;EGP récupérés sur des stocks dormants.",
         ["Pré-construction d'une grande arène intérieure polyvalente : planification MEP, coordination, achats et soumissions.",
          "Chantier en CVC, incendie, plomberie et électricité : inspections, contrôle qualité, mise en service et remise.",
          "Valorisation des stocks dormants : 1&nbsp;400 références immobilisées dans l'entrepôt principal. 10&nbsp;M&nbsp;EGP récupérés sur les premiers 20&nbsp;%, deux fois la valeur comptable : ferraille, envoi sur chantier et retours fournisseurs.",
          "Création avec Claude de l'application web multi-utilisateurs qui pilote le projet : stocks, QC, décisions, audit et tableaux de bord. 1&nbsp;600+ commits en 6&nbsp;semaines avec des agents IA ; données ERP en direct et généralisation à toute l'entreprise à venir.",
          "Membre du comité Supply Chain."], True),
        ("Co-fondateur", "IQASE", "2025 – présent",
         "Accessoires pour téléphones, de la CAO à la fabrication et à la mise sur le marché.",
         ["Conception des produits et CAO prête pour la production ; prototypage d'une nouvelle gamme.",
          "Gestion de la fabrication avec des fournisseurs en Chine ; moule en cours d'usinage pour la première production.",
          "Modèle financier (coût unitaire, prix, marges), gestion du budget et du compte de résultat.",
          "Mise sur le marché dans la région MENA : image de marque, marketing digital, distribution."], False),
    ],
    earlier="<b>Avant :</b> Boutique V12 F1, Montréal (2023) · GVI, Costa Rica (2019) · ABB et GTAT, Le Caire (2019) · GoPro chez ABM, Dubaï (2017)",
    proj=[
        ("Fusée à propulsion laser", "", "2024", "Banc de propulsion thermique laser : 50&nbsp;bars, plasma à 15&nbsp;000&nbsp;K, poussée mesurable.",
         ["Chambre d'ionisation en aluminium dimensionnée pour 50&nbsp;bars, avec un laser continu de 350&nbsp;W pendant 30&nbsp;s.",
          "Étude de transfert de chaleur par premiers principes : dissipateurs et refroidissement régénératif.",
          "CAO DFMA et dessins GD&amp;T sous SolidWorks ; direction du prototypage et de la fabrication.",
          "Livré en 6&nbsp;mois dans le budget ; tests structurels réussis et poussée mesurée."]),
        ("Machine Learning", "", "2025 – présent", "Réseau de neurones codé de zéro avec NumPy ; maintenant un petit transformeur.",
         ["Perceptron multicouche codé de zéro avec NumPy, entraîné sur les chiffres manuscrits MNIST.",
          "Développement d'un petit modèle de langage à transformeurs pour comprendre l'attention."]),
        ("Boîte de transmission", "", "2022", "Boîte à engrenages droits AGMA pour un petit aéronef.",
         ["Transmission à engrenages droits à double réduction, norme AGMA.",
          "Analyse des efforts, contraintes et fatigue ; arbres, roulements et clavettes dimensionnés sur leur cycle de vie.",
          "Optimisation itérative avec des scripts Python et des feuilles de calcul."]),
        ("Support structurel", "", "2022", "Support en acrylique optimisé par éléments finis sous Abaqus.",
         ["Support 2D en acrylique léger, résistance maximale pour une rigidité cible.",
          "Analyse EF sous Abaqus calibrée avec des essais matériaux ; fichiers DXF pour la découpe laser."]),
    ],
    edu=("Baccalauréat en génie mécanique", "Université McGill", "2020 – 2025", "GPA 3,6, deux bourses.",
         ["Bourses commémoratives du Professeur Bill Williams et John Howard Ambrose, 2020–2021.",
          "Cours : thermodynamique, conception mécanique, mécanique des fluides, DFMA, GD&amp;T, transfert de chaleur, aérodynamique subsonique."]),
    skills=[
        "<b>Ingénierie :</b> SolidWorks, Mastercam, Abaqus, DFMA, GD&amp;T, CNC, impression 3D",
        "<b>Logiciels :</b> Python, MATLAB, workflows d'agents IA (Claude)",
        "<b>Langues :</b> français, anglais, arabe",
    ],
)


def attr(s):
    return s.replace('"', "&quot;")


def page(d):
    n = 0
    exp = []
    for t, o, w, s, b, has_stage in d["exp"]:
        n += 1
        exp.append(item(n, t, o, w, s, b, stage(d) if has_stage else ""))
    proj = []
    for t, o, w, s, b in d["proj"]:
        n += 1
        proj.append(item(n, t, o, w, s, b))
    et, eo, ew, es, eb = d["edu"]
    n += 1
    edu = item(n, et, eo, ew, es, eb)
    skills = "\n".join(f'      <p class="plain">{s}</p>' for s in d["skills"])
    b = d["base"]
    en_cur = ' aria-current="page"' if d["lang"] == "en" else ""
    fr_cur = ' aria-current="page"' if d["lang"] == "fr" else ""
    nl = "\n"
    return f"""<!DOCTYPE html>
<html lang="{d['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{d['title']}</title>
  <meta name="description" content="{attr(d['desc'])}">
  <link rel="alternate" hreflang="en" href="https://a-hal.github.io/">
  <link rel="alternate" hreflang="fr" href="https://a-hal.github.io/fr/">
  <meta property="og:title" content="{d['title']}">
  <meta property="og:description" content="{attr(d['desc'])}">
  <meta property="og:image" content="https://a-hal.github.io/linkedin.png">
  <script>document.documentElement.classList.add("js");try{{var t=localStorage.getItem("theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{b}assets/style.css">
</head>
<body>
<div class="wrap">

  <nav class="top">
    <span class="lang">
      <a href="{d['en_href']}" hreflang="en"{en_cur}>{wt("EN")}</a>
      <a href="{d['fr_href']}" hreflang="fr"{fr_cur}>{wt("FR")}</a>
    </span>
    {LAMP.format(label=attr(d['lamp']))}
  </nav>

  <main class="reveal">
    <header class="intro">
      <div class="who">
        <img src="{b}linkedin.png" alt="Alain Halbouny" width="56" height="56">
        <div>
          <h1>Alain Halbouny</h1>
          <p class="role">{d['role']}</p>
        </div>
      </div>
      <p class="lede">{d['lede']}</p>
      <div class="links">
        <a class="cv" href="{d['cv']}" download>CV</a>
        <a href="mailto:alainhalbouny@gmail.com">Email</a>
        <a href="https://www.linkedin.com/in/alain-halbouny" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://wa.me/15144431307" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </header>

    <section>
      <h2>{d['h_exp']}</h2>
      <ul class="list">
{nl.join(exp)}
      </ul>
      <p class="note">{d['earlier']}</p>
    </section>

    <section>
      <h2>{d['h_proj']}</h2>
      <ul class="list">
{nl.join(proj)}
      </ul>
    </section>

    <section>
      <h2>{d['h_edu']}</h2>
      <ul class="list">
{edu}
      </ul>
    </section>

    <section>
      <h2>{d['h_skills']}</h2>
{skills}
    </section>
  </main>

  <footer>© 2026 Alain Halbouny</footer>

</div>
<script src="{b}assets/main.js"></script>
</body>
</html>
"""


with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(page(EN))
os.makedirs(os.path.join(ROOT, "fr"), exist_ok=True)
with open(os.path.join(ROOT, "fr", "index.html"), "w", encoding="utf-8") as f:
    f.write(page(FR))
print("built")
