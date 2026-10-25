# SSI weekly video input contract

[input.schema.json](input.schema.json) is the proposed JSON Schema 2020-12 input
contract from the accepted SSI-source handoff. It fixes Ukrainian report language,
English video language and exactly three distinct report parts; scene facts carry
claim IDs, units, bases and source periods. Dates/hashes require binding to a real
validated SSI report. No invented runnable example, private report or media is included.

This contract does not implement report extraction, translation, chart rendering,
speech, scheduling or Telegram delivery. The repository's small output-schema
checker is not a general JSON Schema 2020-12 validator; use a full validator in the
receiving project, then check claims against its saved report snapshot.

[Transfer procedure](../../docs/external-project-handoff.md) ·
[SSI case](../../docs/experiments/ssi-brand-profiles.md).
