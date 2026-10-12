"""Render the static portfolio from the reviewed GitHub snapshot (no dependencies)."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/portfolio.json').read_text())
profile = data['profile']


def esc(value):
    return escape(str(value), quote=True)


def link(url, label, css=''):
    return f'<a class="{css}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>'


def photo(src, alt, css=''):
    return f'<a class="photo {css}" href="{esc(src)}" data-lightbox aria-label="View image: {esc(alt)}"><img src="{esc(src)}" alt="{esc(alt)}" loading="lazy" decoding="async"></a>'


def chips(items):
    return '<ul class="chips">' + ''.join(f'<li>{esc(item)}</li>' for item in items) + '</ul>'


experiences = []
for item in data['experiences']:
    photos = ''.join(photo(f'assets/github/showcase/experience/{item["id"]}/{filename.replace(".jpg", ".webp")}', f'{item["organization"]} · {item["title"]} · photo {i + 1}') for i, filename in enumerate(item['photos']))
    experiences.append(f'''<article class="experience-card" id="{esc(item['id'])}">
      <div class="experience-summary"><p class="eyebrow">{esc(item['focus'])} / {esc(item['period'])}</p>
      <h3>{esc(item['title'])}</h3><p class="organization">{esc(item['organization'])}</p>
      <p>{esc(item['description'])}</p>{chips(item['tags'])}</div>
      <div class="photo-strip" aria-label="Photos of {esc(item['organization'])}">{photos}</div>
    </article>''')

achievements = ''.join(f'''<article class="achievement-card">
    {photo('assets/github/showcase/achievements/' + filename.replace('.jpg', '.webp'), award + ' · ' + competition + ' · ' + year)}
    <div><p class="eyebrow">{esc(year)}</p><h3>{esc(award)}</h3><p>{esc(competition)}</p></div>
  </article>''' for filename, award, competition, year in data['achievements'])

projects = []
for item in data['projects']:
    notes = ''
    if item['repo'] == 'tomato-vision':
        notes = 'Research prototype; visual classification is not a food-safety assessment.'
    elif item['repo'] == 'BUNDA-SIAGA':
        notes = 'Prototype; clinical rules are drafts and have not been clinically validated.'
    elif item['repo'] == 'CAPIRA':
        notes = 'Research prototype; not a validated medical device. Screens show synthetic data.'
    elif item['repo'] == 'Batch-Aman':
        notes = 'Default thresholds are not yet expert-verified; field validation is pending.'
    shots = ''.join(photo('assets/github/' + path.removeprefix('/images/'), item['alt'] + f' · image {i + 1}') for i, path in enumerate(item['shots']))
    details = ''.join(f'<div><dt>{label}</dt><dd>{esc(item[key])}</dd></div>' for key, label in [('problem', 'The idea'), ('role', 'Role'), ('outcome', 'What’s built')] if item.get(key))
    links = link('https://github.com/sellebeww/' + item['repo'], 'Source on GitHub')
    if item.get('homepage'):
        links += link(item['homepage'], 'Open demo')
    if item.get('evidence'):
        links += link(item['evidence'], 'Read the details')
    projects.append(f'''<article class="project-card" data-project data-search="{esc(' '.join([item['title'], item['summary'], item['kind'], *item['stack']]).lower())}">
      <div class="project-photos photo-strip">{shots}</div><div class="project-copy">
      <p class="eyebrow">{esc(item['kind'])}{' / ' + esc(item['context']) if item.get('context') else ''}</p>
      <h3>{esc(item['title'])}</h3><p>{esc(item['summary'])}</p>{chips(item['stack'])}
      <details><summary>About this project</summary><dl>{details}</dl></details>
      {f'<p class="project-note">{esc(notes)}</p>' if notes else ''}
      <div class="card-links">{links}</div></div></article>''')

featured = {item['repo'] for item in data['projects']}
other_repos = []
for repo in data['repos']:
    if repo['name'] in featured:
        continue
    description = repo['description'] or ('GitHub profile and introduction.' if repo['name'] == 'sellebeww' else 'This website’s source.')
    other_repos.append(f'<article class="repo-card" data-project data-search="{esc((repo["name"] + " " + description + " " + (repo["language"] or "")).lower())}"><p class="eyebrow">{esc(repo["language"] or "Profile")}</p><h3>{link(repo["url"], repo["name"])}</h3><p>{esc(description)}</p></article>')

chapters = [('home', 'Home'), ('experience', 'Experiences'), ('about', 'About Me'), ('achievements', 'Achievements'), ('projects', 'Projects'), ('contact', 'Contact')]
nav = ''.join(f'<a href="#{key}">{label}</a>' for key, label in chapters)
side_nav = ''.join(f'<a href="#{key}"><span class="nav-number">{i:02}</span><span class="nav-label">{label}</span></a>' for i, (key, label) in enumerate(chapters, 1))
socials = ''.join(link(profile[key], label) for key, label in [('github', 'GitHub'), ('linkedin', 'LinkedIn'), ('instagram', 'Instagram'), ('whatsapp', 'WhatsApp')])
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Vassel Goleyu — Portfolio</title>
  <meta name="description" content="Vassel Goleyu — Informatics student and full-stack developer at Universitas Multimedia Nusantara. Explore projects, campus leadership, health initiatives, and achievements.">
  <meta name="author" content="Vassel Goleyu">
  <meta name="theme-color" content="#0c0c0c">
  <meta property="og:title" content="Vassel Goleyu — Portfolio">
  <meta property="og:description" content="Technology, community, and a curiosity for what comes next. Explore my work and experiences.">
  <meta property="og:type" content="website">
  <link rel="icon" href="assets/img/logo.png">
  <link rel="stylesheet" href="assets/css/portfolio.css">
  <script src="assets/js/portfolio.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="perspective"><div class="stage" id="stage">
  <header class="header"><a class="brand" href="#home"><img src="assets/img/logo.png" width="30" height="28" alt=""><span>Vassel Goleyu</span></a>
    <a class="header-cta button" href="#chat">Chat? →</a>
    <button class="menu-toggle" type="button" aria-label="Open navigation menu" aria-expanded="false" aria-controls="menu-panel" hidden><span></span><span></span><span></span></button>
  </header>
  <nav class="side-nav" aria-label="Section navigation">{side_nav}</nav>
  <noscript><nav class="fallback-nav" aria-label="Main navigation">{nav}</nav></noscript>
  <main id="main">
    <section class="hero section" id="home" aria-labelledby="hero-title">
      <div class="hero-banner"><div class="hero-copy">
        <h1 id="hero-title">Vassel Goleyu<br>Portfolio<br>Website</h1>
        <p class="hero-role">{esc(profile['role'])}</p>
        <div class="hero-actions"><a class="button" href="#chat">Chat? <span aria-hidden="true">→</span></a><a class="text-link" href="#projects">Explore projects ↗</a></div>
      </div>
      <img class="hero-image" src="assets/img/introduction-visual.png" alt="Vassel Goleyu" fetchpriority="high"></div>
    </section>
    <section class="section" id="experience" aria-labelledby="experience-title"><div class="section-heading"><div><p class="eyebrow">02 / People & purpose</p><h2 id="experience-title">My experience<span class="blue">.</span></h2></div></div><div class="experience-list">{''.join(experiences)}</div></section>
    <section class="section" id="about" aria-labelledby="about-title"><div class="about-layout"><div><p class="eyebrow">03 / A little about me</p><h2 id="about-title">I love<br>technology<br>and science<span class="blue">.</span></h2><p>{esc(profile['bio'])}</p><p>I build for the web and care about the little design details. My curiosity also extends to PLC and automation.</p>{link(profile['github'], 'Meet me on GitHub')}</div>
      <div class="stack-panel"><img class="about-portrait" src="assets/github/profile/vassel.webp" alt="Vassel Goleyu in his UMN jacket" loading="lazy"><h3>Things I build with</h3>{chips(['Node.js', 'TypeScript', 'React', 'Docker', 'Kotlin', 'Unity', 'TensorFlow'])}</div></div>
    </section>
    <section class="section" id="achievements" aria-labelledby="achievements-title"><div class="section-heading"><div><p class="eyebrow">04 / Milestones</p><h2 id="achievements-title">Always learning<span class="blue">.</span></h2></div><p>Leadership, science, language, and a little curiosity.</p></div><div class="achievement-grid">{achievements}</div></section>
    <section class="section" id="projects" aria-labelledby="projects-title"><div class="section-heading"><div><p class="eyebrow">05 / From idea to code</p><h2 id="projects-title">Projects<span class="blue">.</span></h2></div><p>Real projects and screenshots from my GitHub portfolio.</p></div>
      <div class="project-search" hidden><label for="project-search">Find a project or technology</label><input id="project-search" type="search" placeholder="Try Kotlin, health, or a project name" aria-describedby="project-count"><p id="project-count" role="status"></p></div>
      <div class="project-grid">{''.join(projects)}</div><h3 class="archive-heading">More from my GitHub</h3><div class="repo-grid">{''.join(other_repos)}</div><p id="no-results" hidden>No projects match your search. Try a different name or technology.</p>
      <p class="source-note">GitHub snapshot · 12 October 2026 · {len(data['repos'])} public repositories. {link(profile['github'] + '?tab=repositories', 'View latest on GitHub')}</p>
    </section>
    <section class="section contact-section" id="contact" aria-labelledby="contact-title"><div class="contact-layout"><div><p class="eyebrow">06 / Let’s connect</p><h2 id="contact-title">Have something<br>in mind<span class="blue">?</span></h2><p>Let’s talk about a project, a collaboration, or a new idea.</p><a class="contact-email" href="mailto:{esc(profile['email'])}">{esc(profile['email'])}</a><p>{esc(profile['location'])}</p><div class="social-links">{socials}</div><a class="button contact-chat" href="#chat">Start a conversation →</a></div></div>
      <div class="chat-layout" id="chat" aria-labelledby="chat-title"><p class="eyebrow">Let’s talk</p><h2 id="chat-title">Let’s make it happen<span class="blue">.</span></h2>
      <form id="contact-form"><h3>Start a conversation</h3><label for="name">Your name</label><input id="name" name="name" autocomplete="name" required maxlength="100"><label for="email">Your email</label><input id="email" name="email" type="email" autocomplete="email" required maxlength="254"><label for="message">What would you like to discuss?</label><textarea id="message" name="message" rows="4" required maxlength="2000"></textarea><button class="button" type="submit" disabled>Open email draft ↗</button><p class="form-note">Opens your email app with a draft. You review and send it there.</p><p id="contact-status" role="status"></p><noscript><p>Enable JavaScript to prepare a draft, or use the email link above.</p></noscript></form></div>
    </section>
  </main>
  <div class="section-controls" hidden><i class="pressure" aria-hidden="true"></i><button type="button" id="previous-section" aria-label="Previous section">↑</button><span id="section-position" role="status">01 / 06 — Home</span><button type="button" id="next-section" aria-label="Next section">↓</button></div>
  </div>
  <div class="menu-panel" id="menu-panel" role="dialog" aria-modal="true" aria-label="Navigation menu" hidden>
    <button class="menu-backdrop" type="button" aria-label="Return to portfolio"></button>
    <button class="menu-close" type="button" aria-label="Close navigation menu">Close ×</button>
    <nav id="navigation" class="outer-nav" aria-label="Main navigation">{nav}</nav>
  </div></div>
  <dialog id="image-dialog" aria-label="Image viewer"><button type="button" class="dialog-close" aria-label="Close image viewer">Close ×</button><img alt=""><p></p></dialog>
</body>
</html>
'''
(ROOT / 'index.html').write_text('\n'.join(line.rstrip() for line in html.splitlines()) + '\n')
print(f'Rendered {len(experiences)} experiences, {len(data["achievements"])} achievements, {len(projects)} featured projects, and {len(other_repos)} other repositories.')
