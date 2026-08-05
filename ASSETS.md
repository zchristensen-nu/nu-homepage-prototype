# northeastern.edu homepage redesign — asset manifest

Gathered 2026-07-23 for the high-fidelity prototype. Sources: brand.northeastern.edu, live www.northeastern.edu markup, news.northeastern.edu REST API.

## Brand: color (brand.northeastern.edu/design-and-experiences/color/)

Core: Black `#000000` + White `#FFFFFF` are the primary pair.
Red (PMS 186): `#C8102E` — accent only, **must stay under 25% of any design** (more allowed for athletics).
Bold Gold (PMS 871 metallic): `#A4804A`; Light Gold: `#C8A978` — prestige accents, ~5% max.
Digital greys (live-site tokens): dark `#111111`, light `#FAFAFA`, neutral-1..6 `#F5F5F5 #E5E5E5 #D4D4D4 #A3A3A3 #737373 #404040`.
Accessibility: WCAG 2.1 AA minimum (4.5:1 body, 3:1 large text/UI).

## Brand: typography

Primary: **FF Real Head** (fallback stack on live site: `FF Real Head, Lato, Arial, sans-serif`). Secondary: Lato (only where Real Head unavailable).
Live-site heading scale: h1 128px w400 ls-0.02em lh1 · h2 56-67 w400 · h3 44-56 w400 · h4 28-44 w300 · h6 uppercase 16-24 w300. Body 18-28, weight-light aesthetic overall.
Webfont files (woff2, ~64KB each) downloaded to scratchpad `nu-assets/fonts/`:
- Light(200)/Semilight(300)/Regular(400)/Medium(600)/Bold(700) from
  `https://www.northeastern.edu/wp-content/themes/nu-start-child/fonts/FFRealHead<Weight>_normal_normal.woff2`

## Brand: logos

- Header wordmark "Northeastern University" SVG (248×22) extracted from the global-elements header bundle → scratchpad `nu-assets/nu-wordmark-header.svg`.
- N monogram: `https://brand.northeastern.edu/global/assets/favicon/apple-touch-180x180.png` (scratchpad `nu-assets/nu-monogram-180.png`).
- Logo system tiers (brand.northeastern.edu/logos/): wordmark (preferred) · monogram (casual/large-format) · seal (formal) · spirit marks · athletic marks. Download portal is gated; SVG sources above are from public site markup.

## Video (hosted on live site, hotlinkable)

- Co-op hero: `https://www.northeastern.edu/wp-content/uploads/The-Co-Op-Experience_Video-2-Fusion-v3.mp4` (13.5MB, 1920×1080)
- Campus/profile: `https://www.northeastern.edu/wp-content/uploads/Jamie-Wong-Video-Fade.mp4` (9.7MB, 3840×2160)

## Globe/map data

- Co-op placements: 4,705 Fall 2026 placements in 519 locations **with lat/lng** already inlined in `prototypes/northeastern-homepage.html` (`DATA.dots[*].lat/lng`) — reusable for the globe.
- Campuses (13): Boston · Oakland · London · Arlington VA · Burlington MA · Charlotte · Miami · Nahant MA · Portland ME · Seattle · Silicon Valley · Toronto · Vancouver. (Verify against northeastern.edu/campuses at build time.)
- N.U.in Fall 2026 (nuin.northeastern.edu/getting-started/program-locations/): Prague (UNYP) · Germany/CIEE (Berlin) · Thessaloniki (ACT) · Dublin (UCD) · Italy/John Cabot (Rome) · Belfast (QUB) · Glasgow (UofG) · Madrid (SLU).

## NGN stories with verified-strong imagery

Eyeballed and confirmed spectacular (downloaded to scratchpad `nu-assets/story-images/`):

| Use | Story | Image |
|---|---|---|
| Hero/co-op | [NASA co-op — SpaceX Dragon docking the ISS](https://news.northeastern.edu/2023/05/03/nasa-engineering-intern/) | `uploads/2023/04/NASA1400.jpg` |
| Co-op | [Aquarium co-op — harbor seal nose-to-lens](https://news.northeastern.edu/2023/04/25/new-england-aquarium-co-op-boston/) | `uploads/2023/04/041923_AS_Isabella_Welch_022.jpg` |
| Research/AI | [Spot robot walking with students at EXP](https://news.northeastern.edu/2025/10/01/walking-the-future/) | `uploads/2025/09/093025_MM_Field_Robotos_Lab_033.jpg` |
| Admissions/finale | [Fenway commencement, fireworks aerial](https://news.northeastern.edu/2025/05/09/fenway-park-commencement-2025/) | `uploads/2025/05/1400-thumbnail-v2.png` |

Additional candidates from the API sweep (alt/caption evidence, not yet eyeballed):

**Globe stories:** Cambodia landmine-relief co-op (`uploads/2023/04/CAMBODIA_coop1400.jpg`) · Cambodia Harpswell dorm mentor (`2023/11/Cecile-Doehrty_1400.jpg`) · Vienna finance co-op café (`2023/09/Vienna1400.jpg`) · Geneva Dialogue, flags backdrop (`2023/11/Dialogue-of-Civilization_1400.jpg`) · Antarctica chinstrap penguins (`2020/02/IMG_20200123_130319.jpg`) · Greece human-rights co-op (`2021/10/mary-ajibade.jpg`) · undersea Proteus station rendering (`2023/05/Proteus1400.jpg`) · JPL co-op video story (`2024/03/JPL_1400x932.png`).

**Research & AI:** EXP snake robot lab (`2023/11/081423_MM_EXP_Robots_048.jpg`, verified good) · Physical AI launch 2026 (`2026/05/052126_MM_Physical_AI_Research_Initiative_Event_001.jpg`) · Gov. Healey selfie with InnovateMA co-ops (`2024/06/062624_MM_Maura_Healey_014.jpg`) · Hydrilla Hunter robotic boat (`2023/12/120723_MM_Agricultural_Experiment_Station_006.jpg`) · world's-fastest-drone video (`2026/01/drone-thumbnail.jpg`) · AI speech synthesis (`2023/10/101123_MM_AI_Seminar_007.jpg`).

**Student life & athletics:** Baseball Beanpot trophy at Fenway (`2025/04/JIM28826.jpg`, verified good) · men's hockey Beanpot at TD Garden (`2024/02/021224_MM_M_beanpot_083.jpg`) · MVP eating cereal from the trophy (`2024/02/021324_MM_beanpot_cele_015.jpg`) · convocation confetti (`2023/09/Convocation1400.jpg`) · Paws rock-paper-scissors orientation (`2025/07/070125_AS_RPS_orientation_004.jpg`).

**Student voices/quotes:** concert-audio co-op backstage with Shania Twain tour (`2023/08/Liam_Martley_001.jpeg`) · "A letter to myself" 2023 grad video (`2024/04/Clara-Wu_1400.jpg`) · best friends from India, flags backdrop (`2023/05/050523_AS_best_friends_-1400.jpg`).

All image paths are under `https://news.northeastern.edu/wp-content/`.

Caveats: no usable CERN co-op story exists on NGN (the current prototype's CERN card is invented — swap for NASA/JPL). Antarctica student-profile coverage is thin; best real options are the Detrich program story and the penguins-drones story.
