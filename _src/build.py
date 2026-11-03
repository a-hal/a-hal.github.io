"""Builds index.html (EN) and fr/index.html (FR) from one template."""
import sys, os

ROOT = sys.argv[1]

SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'

EN = dict(
    lang="en", base="", title="Alain Halbouny · Mechanical Engineer",
    desc="Alain Halbouny: mechanical engineer (McGill), MEP engineer at Rowad Modern Engineering and co-founder of IQASE.",
    role="Mechanical Engineer",
    lede="MEP engineer at Rowad in Cairo and co-founder of IQASE. I design hardware and build the software around it with AI.",
    cv="cv/Alain_Halbouny_CV.pdf", cv_label="CV", toggle="Toggle dark mode", alt="Alain Halbouny",
    en_cls=' class="on" aria-current="page"', fr_cls="", en_href="./", fr_href="fr/",
    h_exp="Experience", h_proj="Projects", h_edu="Education", h_skills="Skills",
    exp=[
        ("MEP Engineer", "Rowad Modern Engineering", "2026 – now",
         "Arena pre-construction and MEP site work. Recovered EGP 10M from idle warehouse stock with an inventory app I built."),
        ("Co-Founder", "IQASE", "2025 – now",
         "Phone accessories, from CAD and manufacturing to market."),
    ],
    earlier="<b>Earlier:</b> V12 F1 Store, Montreal (2023) · GVI, Costa Rica (2019) · ABB &amp; GTAT, Cairo (2019) · GoPro at ABM, Dubai (2017)",
    proj=[
        ("Laser-Powered Rocket", "2024", "Laser thermal propulsion rig: 50-bar chamber, 15,000 K plasma, measurable thrust."),
        ("Machine Learning", "2025 – now", "Neural network from scratch in NumPy; now a small transformer."),
        ("Transmission Box", "2022", "AGMA spur gearbox for a small aircraft."),
        ("Structural Bracket", "2022", "FEA-optimized acrylic bracket in Abaqus."),
    ],
    edu=("B.Eng. Mechanical Engineering", "McGill University", "2020 – 2025", "GPA 3.6 · two scholarships"),
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
    cv="../cv/Alain_Halbouny_CV_FR.pdf", cv_label="CV", toggle="Basculer le mode sombre", alt="Alain Halbouny",
    en_cls="", fr_cls=' class="on" aria-current="page"', en_href="../", fr_href="./",
    h_exp="Expérience", h_proj="Projets", h_edu="Formation", h_skills="Compétences",
    exp=[
        ("Ingénieur MEP", "Rowad Modern Engineering", "2026 – présent",
         "Pré-construction d'une arène et travaux MEP sur chantier. 10 M EGP récupérés sur des stocks dormants grâce à une application que j'ai développée."),
        ("Co-fondateur", "IQASE", "2025 – présent",
         "Accessoires pour téléphones, de la CAO à la fabrication et à la mise sur le marché."),
    ],
    earlier="<b>Avant :</b> Boutique V12 F1, Montréal (2023) · GVI, Costa Rica (2019) · ABB et GTAT, Le Caire (2019) · GoPro chez ABM, Dubaï (2017)",
    proj=[
        ("Fusée à propulsion laser", "2024", "Banc de propulsion thermique laser : chambre de 50 bars, plasma à 15 000 K, poussée mesurable."),
        ("Machine Learning", "2025 – présent", "Réseau de neurones codé de zéro avec NumPy ; maintenant un petit transformeur."),
        ("Boîte de transmission", "2022", "Boîte à engrenages droits AGMA pour un petit aéronef."),
        ("Support structurel", "2022", "Support en acrylique optimisé par éléments finis sous Abaqus."),
    ],
    edu=("Baccalauréat en génie mécanique", "Université McGill", "2020 – 2025", "GPA 3,6 · deux bourses"),
    skills=[
        "<b>Ingénierie :</b> SolidWorks, Mastercam, Abaqus, DFMA, GD&amp;T, CNC, impression 3D",
        "<b>Logiciels :</b> Python, MATLAB, workflows d'agents IA (Claude)",
        "<b>Langues :</b> français, anglais, arabe",
    ],
)


def esc(s):
    return s.replace("'", "&#39;")


def page(d):
    exp = "\n".join(
        f'        <li><div class="row"><span><b>{t}</b> <span class="org">· {o}</span></span><time>{w}</time></div><p>{p}</p></li>'
        for t, o, w, p in d["exp"])
    proj = "\n".join(
        f'        <li><div class="row"><b>{t}</b><time>{w}</time></div><p>{p}</p></li>'
        for t, w, p in d["proj"])
    et, eo, ew, ep = d["edu"]
    skills = "\n".join(f'      <p class="plain">{s}</p>' for s in d["skills"])
    b = d["base"]
    return f"""<!DOCTYPE html>
<html lang="{d['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{d['title']}</title>
  <meta name="description" content="{esc(d['desc'])}">
  <link rel="alternate" hreflang="en" href="https://a-hal.github.io/">
  <link rel="alternate" hreflang="fr" href="https://a-hal.github.io/fr/">
  <meta property="og:title" content="{d['title']}">
  <meta property="og:description" content="{esc(d['desc'])}">
  <meta property="og:image" content="https://a-hal.github.io/linkedin.png">
  <script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{b}assets/style.css">
</head>
<body>
<div class="wrap">

  <nav class="top">
    <a href="{d['en_href']}"{d['en_cls']} hreflang="en">EN</a>
    <span class="sep">/</span>
    <a href="{d['fr_href']}"{d['fr_cls']} hreflang="fr">FR</a>
    <button id="theme-toggle" type="button" aria-label="{d['toggle']}">{SUN}{MOON}</button>
  </nav>

  <header class="intro">
    <div class="who">
      <img src="{b}linkedin.png" alt="{esc(d['alt'])}" width="56" height="56">
      <div>
        <h1>Alain Halbouny</h1>
        <p>{d['role']}</p>
      </div>
    </div>
    <p class="lede">{d['lede']}</p>
    <div class="links">
      <a class="cv" href="{d['cv']}" download>{d['cv_label']}</a>
      <a href="mailto:alainhalbouny@gmail.com">Email</a>
      <a href="https://www.linkedin.com/in/alain-halbouny" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://wa.me/15144431307" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </header>

  <main>
    <section>
      <h2>{d['h_exp']}</h2>
      <ul class="list">
{exp}
      </ul>
      <p class="plain" style="margin-top:8px">{d['earlier']}</p>
    </section>

    <section>
      <h2>{d['h_proj']}</h2>
      <ul class="list">
{proj}
      </ul>
    </section>

    <section>
      <h2>{d['h_edu']}</h2>
      <ul class="list">
        <li><div class="row"><span><b>{et}</b> <span class="org">· {eo}</span></span><time>{ew}</time></div><p>{ep}</p></li>
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


open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page(EN))
os.makedirs(os.path.join(ROOT, "fr"), exist_ok=True)
open(os.path.join(ROOT, "fr", "index.html"), "w", encoding="utf-8").write(page(FR))
print("built")
