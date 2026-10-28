# Ecosystem and orchestration: assessment, 27 October 2026

Framewright already records production tasks, dependencies, approvals, materials and evidence, and supports bounded, explicit execution for certain adapters. Its project resume is a planning and checkpoint facility, not a general autonomous scheduler. Do not infer successful renders, publication or completed human review from a plan alone.

- [SET](https://github.com/markoblogo/SET): GitHub Action orchestration for the ABVX development stack. Candidate for repository maintenance and review-first checks, not a substitute for a video job scheduler.
- [abvx-agent-skills](https://github.com/markoblogo/abvx-agent-skills): reusable agent practices for scoped execution, verification and handoff. Adapt selectively to production work.
- [AGENTS.md_generator](https://github.com/markoblogo/AGENTS.md_generator): candidate for maintaining concise repository instructions; preserve manual project context and review generated changes.
- [ID](https://github.com/markoblogo/ID): portable, owner-controlled creator preferences and context. Keep private identity separate from public production logs and retain per-project decisions in Framewright.
- [Pomerado](https://github.com/Pomerado/pomerado): MIT core for building website-specific MCP integrations. The vendor requires Node 24.21+ and an OpenAI API key to create and review integrations; model calls may incur charges. Existing integrations run without model calls according to its documentation. Not a replacement for production orchestration. No installation or minting was performed.

## Candidate test

If a free, authorized way to mint becomes available, create one read-only integration against a synthetic or public test page, review the generated source and permissions, run it twice and verify output and behavior after a page change. Record time and cost. Prefer official APIs/connectors where they exist. Authenticated or write operations require a separate scoped review; the project's documentation notes that a write mint performs the action once and that execution does not recheck intent or authority.

## Selection principle

Ecosystem integration is optional. Reuse a specific idea or component only when it solves an actual Framewright need; prefer the simplest existing mechanism, check licence and attribution before copying code, and do not add runtime dependencies solely for ecosystem consistency. Run future experiments sequentially on this machine.
