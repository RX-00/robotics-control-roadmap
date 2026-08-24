# Interactive Website

The website in `website/` is a deliberately small, static interactive version of the radial roadmap. It is built with React, TypeScript, and Vite and is intended for GitHub Pages at `https://rx-00.github.io/robotics-control-roadmap/`.

## Architecture

`robotics-control-roadmap.drawio` remains the canonical source for all roadmap topology, geometry, node labels, visual styling, and relationships. The browser never parses Draw.io.

```text
robotics-control-roadmap.drawio + topics-and-references.md
                         |
                         v
              scripts/sync_from_drawio.py
                         |
                         v
        website/src/generated/roadmap.json
                         |
                         v
              React + SVG interactive atlas
```

The generated data includes the canvas, rings, group hubs, topic positions and styles, visible atlas edges, and the complete direct prerequisite graph. `visibleEdges` is intentionally separate from `prerequisiteEdges`: the former is rendered on the atlas, while the latter drives the selected topic's prerequisite and next-topic lists. Cross-track detail edges therefore remain hidden visually, as they are in the original roadmap.

Topic resource links are extracted from the stable topic-ID blocks in `topics-and-references.md`. The site surfaces only existing curated links; it does not manufacture descriptions or recommendations. Future human-curated fields can be added to that Markdown/source-generation path without duplicating any graph data in React.

## Local development

Use a current Node.js LTS release (the deployment workflow uses Node 24) and Python 3.

```bash
python scripts/sync_from_drawio.py
cd website
npm install
npm run dev
```

Vite prints the local URL. The development server still uses the GitHub Pages project base path, so open the URL Vite reports rather than assuming `/`.

Useful checks are:

```bash
python scripts/sync_from_drawio.py --check
python -m unittest discover -s tests -v
cd website && npm run typecheck
cd website && npm run build
```

`npm run build` writes the deployable static files to `website/dist/`. That directory is deliberately not committed or manually copied into the repository.

## Safely modifying the roadmap

1. Edit `robotics-control-roadmap.drawio` in diagrams.net and preserve semantic IDs such as `F1`, `R6`, and `hub-R`.
2. Keep within-track edges on the visible **Radial atlas** layer. Put entry and cross-track prerequisite edges on the hidden **Detailed cross-domain prerequisites** layer.
3. Update resources below the matching `<!-- roadmap-topic:ID -->` marker in `topics-and-references.md` when appropriate.
4. Run `python scripts/sync_from_drawio.py`. This refreshes `website/src/generated/roadmap.json` as well as the SVG, Mermaid graph, and synchronized Markdown blocks.
5. Run the checks above and inspect the interactive map after a meaningful geometry or style change.

Do not hand-edit `website/src/generated/roadmap.json`; the synchronization check will replace or reject stale generated data. React components should consume the generated data rather than adding a separate list of topics, coordinates, or edges.

## Deployment

`.github/workflows/deploy-pages.yml` runs on every push to `main` and can also be started manually. It verifies synchronized artifacts, runs Python tests, installs the locked frontend dependencies, type-checks, builds Vite, and deploys `website/dist` with the official GitHub Pages actions. The Vite base is `/robotics-control-roadmap/`, which keeps production asset URLs correct for the project-site URL.

The repository's GitHub Pages settings must use **GitHub Actions** as the deployment source once. No custom domain or committed build output is required.
