# The World in One Day — Saturday, 21 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261121)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Entry: valid](https://img.shields.io/badge/entry-1024x1024-brightgreen)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page summing up the world's news of
**Saturday, 21 November 2026**, built for the
[make.fun news-image-20261121 bounty](https://make.fun/bounty/news-image-20261121).

## What's on the page

- **Lead — War in Ukraine:** Russia's overnight barrage of 400+ drones and
  110+ missiles; at least 8 killed in Kyiv, three Dnipro bridges damaged;
  two Russian cruise missiles and a suspected drone came down in Poland.
- **Markets:** the AI sell-off drags the S&P 500 and the Dow into correction.
- **Climate — COP31, Antalya:** talks run into overtime, draft deal silent
  on fossil fuels.
- **Health:** daraxonrasib + chemotherapy wipes out detectable tumours in
  1 in 12 advanced pancreatic cancer patients.
- **Europe:** the UK and EU sign their biggest post-Brexit deals.
- **Also today:** Gen Z protests in 25 European countries, Iran downs a US
  MQ-9 drone, Myanmar rejects the world court's genocide ruling, FBI
  database reportedly hacked.

## How it is built

`render.py` draws the whole page with Pillow (vector art + DejaVu type,
no network, no randomness) and writes `entry.png` (1024×1024).
`main.ts` verifies the PNG against the competition's gate (PNG magic,
≤ 1 MiB, ≤ 1024×1024) and copies it to the output directory.

```sh
python3 render.py                 # rebuild entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

AP, Reuters, The New York Times, BBC, Human Rights Watch, Amnesty
International — all events of 21 November 2026.
