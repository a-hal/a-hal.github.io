"""Builds index.html (EN) and fr/index.html (FR) from one template.

Run from the repository root:  python3 _src/build.py .

Content comes from CV 3.2 (the one-page and full versions). Each section is a
short story rather than a CV line: what the work was, how it was done, what came
of it. Nothing here should claim more than the CV does.
"""
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

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

# Lucide icons (ISC), one stroke weight, one size.
ICON = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "down": '<path d="M12 5v14M6 13l6 6 6-6"/>',
    "copy": '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
}


def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')


def stage(s):
    """The material recovery app, drawn to Stageshow's rules: real words only on
    the decisions and the total, filler bars for the item names, one big number."""
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


def stats(items):
    cells = "".join(f'<div><b>{n}</b><span>{label}</span></div>' for n, label in items)
    return f'<div class="stats">{cells}</div>'


def paras(ps):
    return "\n".join(f"        <p>{p}</p>" for p in ps)


def nudge(text, label):
    return f'<p class="nudge"><a href="#contact">{text} {icon("arrow")}</a></p>' if text else ""


# ─────────────────────────────────────────────────────────────────────────────
EN = dict(
    lang="en", base="", title="Alain Halbouny · Mechanical Engineer",
    desc="Alain Halbouny: mechanical engineer (McGill), MEP engineer at Rowad Modern Engineering and co-founder of IQASE. Get in touch.",
    lamp="Pull the cord to switch light and dark", en_href="./", fr_href="fr/", cv="cv/Alain_Halbouny_CV.pdf",
    nav=[("rowad", "Rowad"), ("iqase", "IQASE"), ("projects", "Projects"), ("background", "Background"), ("contact", "Contact")],
    nav_label="Sections",
    hello="Hi, I'm Alain.",
    lede="I'm a mechanical engineer from McGill. By day I coordinate MEP systems for construction in Cairo; the rest of the time I'm building IQASE, a phone accessory company, and the software behind my work with AI agents.",
    facts="Cairo, Egypt · Egyptian-French · UAE resident · Canada work permit · French, English, Arabic",
    cta="Get in touch", cv_label="Download CV", scroll="See what I'm working on",
    rowad=dict(
        title="Construction, and the stock nobody was using",
        meta="MEP Engineer · Rowad Modern Engineering · Cairo · Feb 2026 – now",
        intro=["I rotate between site and headquarters, supporting senior engineers across disciplines in a fast-paced construction environment.",
               "In pre-construction for a large indoor multipurpose arena, I work on MEP planning, design coordination, procurement and submittal review: reading drawings, specs, submittals and contracts, and keeping consultants, contractors and suppliers aligned.",
               "On site, I cover HVAC, fire-fighting, plumbing and electrical: inspections, quality control, commissioning and handover."],
        sub="Aging material recovery", sub_meta="Aug 2026 – now",
        story=["The company's main warehouse held 1,400 SKUs that had been sitting idle. I started with the data: the ERP records were messy, so I cleaned them up with physical counts and on-site brand checks alongside the warehouse staff.",
               "Then I set up QC inspections to decide, item by item, whether to scrap it, send it to a site or return it to the supplier, and matched what was left to requests from active sites."],
        stats=[("EGP 10M", "recovered so far"), ("2×", "the book value"), ("20%", "of items handled"), ("1,400", "idle SKUs")],
        app=["To run it, I built a multi-user web app with Claude: inventory, QC records, decisions, audit trail and dashboards. An AI agent workflow develops and tests it, and shipped 1,600+ commits in 6 weeks.",
             "Live ERP data is being integrated now, ahead of a company-wide rollout and a mobile app. I'm also a member of the Supply Chain Committee, working on inventory, logistics and procurement strategy."],
        nudge="Sitting on idle stock or a process that needs a better tool? Tell me about it",
    ),
    stage=dict(title="Aging stock", site="To site", scrap="Scrap", ret="Return", label="Recovered",
               sub="First 20% of 1,400 SKUs, 2× book value",
               aria="The material recovery app: each idle item gets a decision, to site, scrap or return, and the recovered total reaches EGP 10M."),
    iqase=dict(
        title="A phone accessory startup, from CAD to market",
        meta="Co-Founder · IQASE · Oct 2025 – now",
        intro="I co-founded IQASE to take products from concept to market, across engineering, manufacturing, sales, marketing and distribution.",
        rows=[("Design", "I designed the products and their production-ready CAD models, and I'm prototyping a new product line now."),
              ("Manufacturing", "I manage manufacturing with suppliers in China. The mold for the first production run is being cut."),
              ("Business", "I built the financial and profit models (unit cost, pricing, margins) and manage the budget and P&amp;L."),
              ("Go-to-market", "I lead branding, digital marketing and distribution across MENA."),
              ("AI", "AI is part of how we work: Claude, Lovable and Higgsfield for marketing, CAD, finance and documentation.")],
        nudge="Want to talk manufacturing, or follow the launch? Get in touch",
    ),
    projects=dict(
        title="Things I've built",
        meta="Team and personal projects, McGill and after",
        items=[
            dict(name="Laser-powered rocket", meta="Team project · Nov 2023 – Apr 2024",
                 stats=[("50 bar", "chamber rating"), ("350 W", "continuous laser"), ("15,000 K", "plasma core"), ("6 months", "on time, on budget")],
                 ps=["A fully functional laser thermal propulsion test apparatus for research. I designed the aluminum ionization chamber, rated for 50 bar with a 350 W continuous laser running for up to 30 seconds.",
                     "The hard part was heat. A first-principles heat transfer study sized the heat sinks and regenerative cooling around a 15,000 K plasma core. I made the production-ready DFMA CAD models, GD&amp;T drawings and assemblies in SolidWorks, and led 3D printing, prototyping and high-precision manufacturing of the main components in-house at McGill.",
                     "I also managed the budget and procurement of outsourced parts. We delivered on a tight 6-month timeline, within budget, passed structural integrity tests and produced measurable thrust."]),
            dict(name="Machine learning from first principles", meta="Personal project · May 2025 – ongoing", stats=[],
                 ps=["I build machine learning models from scratch to understand how they really work. I implemented a multi-layer perceptron in NumPy to classify the MNIST handwritten digits, without a framework.",
                     "Now I'm developing a small transformer-based language model to explore foundational NLP and attention mechanisms. It sits alongside the Machine Learning Specialization from Stanford."]),
            dict(name="Auxiliary transmission box", meta="Team project · Mar – Apr 2022", stats=[],
                 ps=["A double-reduction spur gear transmission for a small aircraft, to the AGMA standard. We sized a compact gear set to hit the required reduction ratio under strict dimensional constraints, then ran AGMA force, stress and fatigue analysis so the gears would last.",
                     "Shafts were engineered with free-body, shear and bending moment diagrams; bearings and keys were selected for fit and load capacity over their lifecycle. Python scripts and custom spreadsheets drove each design iteration."]),
            dict(name="Structural bracket", meta="Team project · Sep – Dec 2022", stats=[],
                 ps=["A lightweight 2D acrylic bracket designed for maximum strength at a target stiffness. FEA in Abaqus, calibrated with material test data, guided every change.",
                     "I optimized a triangular mesh within a 1,000-node limit by focusing on the critical stress areas, and refined the geometry to cut weight while keeping its structural integrity. The final CAD and DXF files from SolidWorks went straight to the laser cutter."]),
        ],
    ),
    background=dict(
        title="Where I come from",
        meta="Education, earlier work and the tools I use",
        edu_h="Education",
        edu=("B.Eng. Mechanical Engineering, McGill University", "Montreal · Sep 2020 – Feb 2025 · GPA 3.6",
             "Awarded the Professor Bill Williams Memorial and John Howard Ambrose Scholarships in 2020–2021. Coursework in thermodynamics, mechanical and conceptual design, fluid mechanics, DFMA, GD&amp;T, numerical methods, dynamics, mechanics of deformable solids, electric machinery, heat transfer and subsonic aerodynamics."),
        cert_h="Certificates",
        certs="Machine Learning Specialization (Stanford) · KDB+/q developer level 3 (Kx)",
        earlier_h="Earlier",
        earlier=[("V12 Trackside F1 Store, Formula 1 Grand Prix", "Montreal · Jun 2023",
                  "Sold merchandise at the 2023 Montreal Grand Prix: diverse crowds, brand promotion and inventory in a fast-paced, high-energy setting."),
                 ("GVI, supervised voluntary work", "Quepos, Costa Rica · Jul 2019",
                  "Helped build a recreation and learning center for underprivileged children on the island of El Cocal. Teamwork and communication were what got it done."),
                 ("ABB and GT Advanced Technologies", "Cairo · Jul 2019",
                  "At ABB, hands-on exposure to electrical engineering projects, project management and supply chain operations across departments. At GTAT, intensive training on solar energy and semiconductor materials."),
                 ("GoPro at ABM, internship", "Dubai · Feb 2017",
                  "With the tech team of what was then the leading GoPro distributor in MENA and the GCC: advertising, market research, technical support, maintenance and inventory.")],
        skills_h="Tools",
        skills=[("Engineering", "SolidWorks (CAD), Mastercam (CAM), Abaqus (FEA)"),
                ("Manufacturing and design", "CNC machining, 3D printing, rapid prototyping, DFMA, GD&amp;T"),
                ("Software", "Python, MATLAB, Claude (TypeScript, Next.js, React, PostgreSQL, Docker, Git), Higgsfield, Microsoft Office"),
                ("AI development", "Apps and websites, workflow automation with AI agents, content creation, AI-assisted CAD"),
                ("Languages", "French, English and Arabic, fluent; Spanish, basic")],
        fun_h="Off the clock",
        fun="Basketball, tennis, padel and skiing. Photography and video editing. The stock market, and whatever AI does next.",
    ),
    contact=dict(
        title="Let's talk",
        ps=["If you're hiring, building a product, or have a process that could use a sharper tool, I'd like to hear about it. A short message is plenty.",
            "I'm based in Cairo, with residency in the UAE and a work permit in Canada, and I work in French, English and Arabic."],
        copy="Copy email", copied="Copied", email_btn="Email me",
    ),
    footer="© 2026 Alain Halbouny",
)

FR = dict(
    lang="fr", base="../", title="Alain Halbouny · Ingénieur mécanique",
    desc="Alain Halbouny : ingénieur mécanique (McGill), ingénieur MEP chez Rowad Modern Engineering et co-fondateur d'IQASE. Écrivez-moi.",
    lamp="Tirez le cordon pour passer du clair au sombre", en_href="../", fr_href="./", cv="../cv/Alain_Halbouny_CV_FR.pdf",
    nav=[("rowad", "Rowad"), ("iqase", "IQASE"), ("projects", "Projets"), ("background", "Parcours"), ("contact", "Contact")],
    nav_label="Sections",
    hello="Bonjour, je suis Alain.",
    lede="Ingénieur mécanique diplômé de McGill. Le jour, je coordonne les lots MEP de chantiers au Caire ; le reste du temps, je construis IQASE, une marque d'accessoires pour téléphones, et les logiciels de mon travail avec des agents IA.",
    facts="Le Caire, Égypte · Franco-Égyptien · Résident ÉAU · Permis de travail canadien · Français, anglais, arabe",
    cta="Écrivez-moi", cv_label="Télécharger le CV", scroll="Voir ce sur quoi je travaille",
    rowad=dict(
        title="Le chantier, et le stock que personne n'utilisait",
        meta="Ingénieur MEP · Rowad Modern Engineering · Le Caire · Fév 2026 – présent",
        intro=["J'alterne entre le chantier et le siège, en soutien aux ingénieurs seniors de toutes les disciplines, dans un environnement de construction dynamique.",
               "En pré-construction d'une grande arène intérieure polyvalente, je travaille sur la planification MEP, la coordination, les achats et les soumissions : plans, cahiers des charges, soumissions et contrats, en lien avec les consultants, entrepreneurs et fournisseurs.",
               "Sur le chantier, je couvre la CVC, la protection incendie, la plomberie et l'électricité : inspections, contrôle qualité, mise en service et remise."],
        sub="Valorisation des stocks dormants", sub_meta="Août 2026 – présent",
        story=["L'entrepôt principal de l'entreprise comptait 1&nbsp;400 références immobilisées. J'ai commencé par les données : l'ERP était désordonné, je l'ai fiabilisé avec des comptages physiques et l'identification des marques sur site, avec les magasiniers.",
               "J'ai ensuite lancé des inspections qualité pour trier le stock article par article : ferraille, envoi sur chantier ou retour fournisseur, puis rapprochement avec les demandes des chantiers."],
        stats=[("10&nbsp;M EGP", "récupérés à ce jour"), ("2×", "la valeur comptable"), ("20&nbsp;%", "des articles traités"), ("1&nbsp;400", "références dormantes")],
        app=["Pour piloter le projet, j'ai créé avec Claude une application web multi-utilisateurs : stocks, QC, décisions, audit et tableaux de bord. Un workflow d'agents IA la développe et la teste : 1&nbsp;600+ commits en 6&nbsp;semaines.",
             "L'intégration des données ERP en direct est en cours, avant sa généralisation à toute l'entreprise et une version mobile. Je suis aussi membre du comité Supply Chain, sur la stratégie de stocks, de logistique et d'achats."],
        nudge="Du stock dormant ou un processus qui mérite un meilleur outil ? Parlons-en",
    ),
    stage=dict(title="Stocks dormants", site="Chantier", scrap="Ferraille", ret="Retour", label="Récupérés",
               sub="Premiers 20&nbsp;% de 1&nbsp;400 références, 2× la valeur comptable",
               aria="L'application de valorisation des stocks : chaque article reçoit une décision, chantier, ferraille ou retour, et le total récupéré atteint 10 M EGP."),
    iqase=dict(
        title="Une startup d'accessoires, de la CAO au marché",
        meta="Co-fondateur · IQASE · Oct 2025 – présent",
        intro="J'ai co-fondé IQASE pour mener des produits de la conception à la commercialisation : ingénierie, fabrication, vente, marketing et distribution.",
        rows=[("Conception", "J'ai conçu les produits et leurs modèles CAO prêts pour la production, et je prototype une nouvelle gamme."),
              ("Fabrication", "Je gère la fabrication avec des fournisseurs en Chine. Le moule de la première production est en cours d'usinage."),
              ("Gestion", "J'ai construit les modèles financiers et de rentabilité (coût unitaire, prix, marges) et je gère le budget et le compte de résultat."),
              ("Mise sur le marché", "Je pilote l'image de marque, le marketing digital et la distribution dans la région MENA."),
              ("IA", "L'IA fait partie de notre façon de travailler : Claude, Lovable et Higgsfield pour le marketing, la CAO, la finance et la documentation.")],
        nudge="Envie de parler fabrication, ou de suivre le lancement ? Écrivez-moi",
    ),
    projects=dict(
        title="Ce que j'ai construit",
        meta="Projets d'équipe et personnels, à McGill et après",
        items=[
            dict(name="Fusée à propulsion laser", meta="Projet d'équipe · Nov 2023 – Avr 2024",
                 stats=[("50&nbsp;bars", "tenue de la chambre"), ("350&nbsp;W", "laser continu"), ("15&nbsp;000&nbsp;K", "cœur de plasma"), ("6&nbsp;mois", "délais et budget tenus")],
                 ps=["Un banc d'essai de propulsion thermique laser entièrement fonctionnel, à des fins de recherche. J'ai conçu la chambre d'ionisation en aluminium, dimensionnée pour 50&nbsp;bars avec un laser continu de 350&nbsp;W pendant 30&nbsp;secondes.",
                     "Le défi, c'était la chaleur. Une étude de transfert thermique par premiers principes a dimensionné les dissipateurs et le refroidissement régénératif autour d'un plasma à 15&nbsp;000&nbsp;K. J'ai réalisé les modèles CAO DFMA, les dessins GD&amp;T et les assemblages sous SolidWorks, et dirigé l'impression 3D, le prototypage et la fabrication de précision des pièces principales, en interne à McGill.",
                     "J'ai aussi géré le budget et les achats de pièces externalisées. Le projet a été livré en 6&nbsp;mois, dans le budget, a réussi les tests d'intégrité structurelle et produit une poussée mesurable."]),
            dict(name="Le machine learning par les fondamentaux", meta="Projet personnel · Mai 2025 – en cours", stats=[],
                 ps=["Je construis des modèles d'apprentissage automatique de zéro pour comprendre vraiment leur fonctionnement. J'ai implémenté un perceptron multicouche avec NumPy, sans framework, pour classer les chiffres manuscrits MNIST.",
                     "Je développe maintenant un petit modèle de langage à base de transformeurs pour explorer le TAL et les mécanismes d'attention, en complément de la Machine Learning Specialization de Stanford."]),
            dict(name="Boîte de transmission auxiliaire", meta="Projet d'équipe · Mar – Avr 2022", stats=[],
                 ps=["Une transmission à engrenages droits à double réduction pour un petit aéronef, selon la norme AGMA. Nous avons dimensionné un jeu d'engrenages compact pour atteindre le rapport de réduction sous de fortes contraintes d'encombrement, puis mené l'analyse AGMA des efforts, contraintes et fatigue.",
                     "Les arbres ont été conçus avec diagrammes de corps libre, d'effort tranchant et de moment fléchissant ; roulements et clavettes ont été choisis pour l'ajustement et la charge sur leur cycle de vie. Des scripts Python et des feuilles de calcul ont piloté chaque itération."]),
            dict(name="Support structurel", meta="Projet d'équipe · Sep – Déc 2022", stats=[],
                 ps=["Un support 2D en acrylique léger, conçu pour une résistance maximale à rigidité cible. L'analyse par éléments finis sous Abaqus, calibrée avec des essais matériaux, a guidé chaque modification.",
                     "J'ai optimisé un maillage triangulaire limité à 1&nbsp;000 nœuds en ciblant les zones de contraintes critiques, et affiné la géométrie pour réduire la masse sans perdre en intégrité. Les fichiers CAO et DXF sous SolidWorks sont partis directement à la découpe laser."]),
        ],
    ),
    background=dict(
        title="D'où je viens",
        meta="Formation, expériences passées et outils",
        edu_h="Formation",
        edu=("Baccalauréat en génie mécanique, Université McGill", "Montréal · Sep 2020 – Fév 2025 · GPA 3,6",
             "Lauréat des bourses commémoratives du Professeur Bill Williams et John Howard Ambrose en 2020–2021. Cours de thermodynamique, conception mécanique, mécanique des fluides, DFMA, GD&amp;T, méthodes numériques, dynamique, mécanique des solides déformables, machines électriques, transfert de chaleur et aérodynamique subsonique."),
        cert_h="Certifications",
        certs="Machine Learning Specialization (Stanford) · Développeur KDB+/q niveau 3 (Kx)",
        earlier_h="Avant",
        earlier=[("Boutique V12 Trackside F1, Grand Prix de Formule 1", "Montréal · Juin 2023",
                  "Vente de produits dérivés au Grand Prix de Montréal 2023 : publics variés, promotion de la marque et gestion des stocks dans un environnement intense."),
                 ("GVI, travail bénévole supervisé", "Quepos, Costa Rica · Juil 2019",
                  "Construction d'un centre de loisirs et d'apprentissage pour des enfants défavorisés sur l'île d'El Cocal. Le travail d'équipe et la communication ont fait la différence."),
                 ("ABB et GT Advanced Technologies", "Le Caire · Juil 2019",
                  "Chez ABB, découverte concrète des projets d'ingénierie électrique, de la gestion de projet et de la supply chain, entre plusieurs départements. Chez GTAT, formation intensive sur l'énergie solaire et les matériaux semi-conducteurs."),
                 ("GoPro chez ABM, stage", "Dubaï · Fév 2017",
                  "Avec l'équipe technique de ce qui était alors le premier distributeur GoPro de la région MENA et du CCG : publicité, études de marché, support technique, maintenance et stocks.")],
        skills_h="Outils",
        skills=[("Ingénierie", "SolidWorks (CAO), Mastercam (FAO), Abaqus (EF)"),
                ("Fabrication et conception", "Usinage CNC, impression 3D, prototypage rapide, DFMA, GD&amp;T"),
                ("Logiciels", "Python, MATLAB, Claude (TypeScript, Next.js, React, PostgreSQL, Docker, Git), Higgsfield, Microsoft Office"),
                ("Développement IA", "Applications et sites web, automatisation par agents IA, création de contenu, CAO assistée par IA"),
                ("Langues", "Français, anglais et arabe courants ; espagnol, notions")],
        fun_h="En dehors du travail",
        fun="Basketball, tennis, padel et ski. Photographie et montage vidéo. La bourse, et ce que l'IA fera ensuite.",
    ),
    contact=dict(
        title="Parlons-en",
        ps=["Que vous recrutiez, que vous construisiez un produit ou qu'un de vos processus mérite un meilleur outil, j'aimerais en entendre parler. Un message court suffit.",
            "Je suis basé au Caire, résident aux Émirats et titulaire d'un permis de travail au Canada, et je travaille en français, en anglais et en arabe."],
        copy="Copier l'e-mail", copied="Copié", email_btn="M'écrire",
    ),
    footer="© 2026 Alain Halbouny",
)

EMAIL = "alainhalbouny@gmail.com"


def attr(s):
    return s.replace('"', "&quot;")


def page(d):
    b = d["base"]
    en_cur = ' aria-current="page"' if d["lang"] == "en" else ""
    fr_cur = ' aria-current="page"' if d["lang"] == "fr" else ""
    nav = "\n".join(f'          <a href="#{i}" data-spy="{i}">{t}</a>' for i, t in d["nav"])
    r, q, p, bg, c = d["rowad"], d["iqase"], d["projects"], d["background"], d["contact"]

    iq_rows = "\n".join(f'          <div class="row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in q["rows"])
    projects = []
    for it in p["items"]:
        projects.append(f"""      <article class="proj">
        <h3>{it['name']}</h3>
        <p class="meta">{it['meta']}</p>
        {stats(it['stats']) if it['stats'] else ''}
{paras(it['ps'])}
      </article>""")
    earlier = "\n".join(
        f'          <div class="row"><dt>{n}<span>{w}</span></dt><dd>{t}</dd></div>' for n, w, t in bg["earlier"])
    skills = "\n".join(f'          <div class="row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in bg["skills"])
    nl = "\n"

    return f"""<!DOCTYPE html>
<html lang="{d['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
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

<header class="topbar" id="top">
  <div class="topbar-in">
    <a class="me" href="#hero" aria-label="Alain Halbouny"><img src="{b}linkedin.png" alt="" width="28" height="28"><span>Alain Halbouny</span></a>
    <nav class="sections" aria-label="{d['nav_label']}">
      <div class="track">
        <span class="pill" aria-hidden="true"></span>
{nav}
      </div>
    </nav>
    <span class="lang">
      <a href="{d['en_href']}" hreflang="en"{en_cur}>EN</a>
      <a href="{d['fr_href']}" hreflang="fr"{fr_cur}>FR</a>
    </span>
  </div>
  <div class="progress" aria-hidden="true"><span></span></div>
</header>

<main>
  <section class="hero" id="hero">
    <div class="wrap">
      {LAMP.format(label=attr(d['lamp']))}
      <div class="hero-text">
      <img class="portrait" src="{b}linkedin.png" alt="Alain Halbouny" width="88" height="88">
      <h1>{d['hello']}</h1>
      <p class="lede">{d['lede']}</p>
      <p class="facts">{d['facts']}</p>
      <div class="ctas">
        <a class="btn primary" href="#contact">{d['cta']} {icon('arrow')}</a>
        <a class="btn" href="{d['cv']}" download>{d['cv_label']} {icon('down')}</a>
        <a class="btn" href="https://www.linkedin.com/in/alain-halbouny" target="_blank" rel="noopener">LinkedIn</a>
      </div>
      <a class="scroll-cue" href="#rowad">{d['scroll']} {icon('down')}</a>
      </div>
      <figure class="hero-photo"><img src="{b}linkedin.png" alt="" width="420" height="420"></figure>
    </div>
  </section>

  <section class="chapter" id="rowad">
    <div class="wrap">
      <div class="ch-head"><h2>{r['title']}</h2>
      <p class="meta">{r['meta']}</p></div>
      <div class="ch-body">
{paras(r['intro'])}
      <h3>{r['sub']}</h3>
      <p class="meta">{r['sub_meta']}</p>
{paras(r['story'])}
      {stats(r['stats'])}
      {stage(d['stage'])}
{paras(r['app'])}
      {nudge(r['nudge'], '')}
      </div>
    </div>
  </section>

  <section class="chapter" id="iqase">
    <div class="wrap">
      <div class="ch-head"><h2>{q['title']}</h2>
      <p class="meta">{q['meta']}</p></div>
      <div class="ch-body">
      <p>{q['intro']}</p>
      <dl class="rows">
{iq_rows}
      </dl>
      {nudge(q['nudge'], '')}
      </div>
    </div>
  </section>

  <section class="chapter" id="projects">
    <div class="wrap">
      <div class="ch-head"><h2>{p['title']}</h2>
      <p class="meta">{p['meta']}</p></div>
      <div class="ch-body">
{nl.join(projects)}
      </div>
    </div>
  </section>

  <section class="chapter" id="background">
    <div class="wrap">
      <div class="ch-head"><h2>{bg['title']}</h2>
      <p class="meta">{bg['meta']}</p></div>
      <div class="ch-body">
      <h3 class="first">{bg['edu_h']}</h3>
      <p><b>{bg['edu'][0]}</b><br><span class="muted">{bg['edu'][1]}</span></p>
      <p>{bg['edu'][2]}</p>
      <p><b>{bg['cert_h']}:</b> {bg['certs']}</p>
      <h3>{bg['earlier_h']}</h3>
      <dl class="rows stacked">
{earlier}
      </dl>
      <h3>{bg['skills_h']}</h3>
      <dl class="rows">
{skills}
      </dl>
      <h3>{bg['fun_h']}</h3>
      <p>{bg['fun']}</p>
      </div>
    </div>
  </section>

  <section class="chapter contact" id="contact">
    <div class="wrap">
      <div class="ch-head"><h2>{c['title']}</h2></div>
      <div class="ch-body">
{paras(c['ps'])}
      <div class="mail">
        <a class="address" href="mailto:{EMAIL}">{EMAIL}</a>
        <button class="copy" type="button" data-email="{EMAIL}" data-copied="{attr(c['copied'])}" aria-label="{attr(c['copy'])}">
          <span class="swap">{icon('copy', 'ic a')}{icon('check', 'ic b')}</span><span class="copy-label">{c['copy']}</span>
          <span class="sr" aria-live="polite"></span>
        </button>
      </div>
      <div class="ctas">
        <a class="btn primary" href="mailto:{EMAIL}">{c['email_btn']} {icon('arrow')}</a>
        <a class="btn" href="https://www.linkedin.com/in/alain-halbouny" target="_blank" rel="noopener">LinkedIn</a>
        <a class="btn" href="https://wa.me/15144431307" target="_blank" rel="noopener">WhatsApp</a>
        <a class="btn" href="{d['cv']}" download>{d['cv_label']} {icon('down')}</a>
      </div>
      </div>
    </div>
  </section>
</main>

<footer><div class="wrap">{d['footer']}</div></footer>

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
