# One ecosystem, separate responsibilities

| Owner | Relationship to Framewright | Boundary |
| --- | --- | --- |
| [ABVX Agent Skills](https://github.com/markoblogo/abvx-agent-skills) | Discover Framewright as an external companion; opt into its router for a video task | No duplicate skill or automatic inclusion in install-all/profiles |
| [SET](https://github.com/markoblogo/SET) | Optionally plan brief → source review → storyboard → render → QA → delivery | Planning is not rendering, paid API approval or upload permission |
| [AGENTS.md Generator](https://github.com/markoblogo/AGENTS.md_generator) | Optionally maintain commands and lean repo context around production projects | No claim that context generation installs or executes video tools |
| [ABVX Lab](https://github.com/markoblogo/lab.abvx) | Public product page and discovery links | Describes source-owned methods, not a hosted production service |
| [Framewright](https://github.com/markoblogo/framewright) | Own router, method catalogue, recipes and experiment evidence | Does not mirror upstream rendering/audio tools |

These are optional integration contracts, not a claim that a combined SET →
agentsgen → video build has been exercised end to end. Retained video
exports do not qualify these cross-repository integrations.

## Optional handoff

1. Use existing repo context or agentsgen when useful; preserve handwritten rules.
2. Ask Framewright to establish a storyboard for a new multi-shot brief, then select
   recipes per shot/layer. Existing approved shots, recuts and finishing skip the
   extra preparation. Keep actual briefs/assets in the video project.
3. Use SET only when the task benefits from an explicit multi-step plan. A plan can
   name the selected recipe and required evidence without granting new permissions.
4. Run production with the chosen tools and project-specific commands, not SET by inference.
5. Retain encoded-file QA and human-review status; publish only within explicit authority.

Do not add a default video build, schedule, model download, publish hook, or broad
global installation to any companion repository. Add new methods in Framewright;
link from the general ecosystem rather than copying their instructions.
