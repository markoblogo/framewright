import {
  Interactive,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Stage, headline, body, amber, ivory, teal, clamp } from "./theme";
export function Evidence() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Stage kicker="03 / KEEP THE EVIDENCE">
      <div
        style={{ display: "grid", gridTemplateColumns: "1.08fr 1fr", gap: 100 }}
      >
        <div>
          <h1 style={headline}>
            Every test.
            <br />
            <span style={{ color: amber }}>A reusable recipe.</span>
          </h1>
          <p style={body}>
            Keep what worked.
            <br />
            Record what did not.
            <br />
            Build on the next experiment.
          </p>
        </div>
        <Interactive.Div
          name="Retained experiment record"
          style={{
            opacity: interpolate(frame, [0.5 * fps, 1.2 * fps], [0, 1], clamp),
            translate: interpolate(
              frame,
              [0.5 * fps, 1.2 * fps],
              ["0px 50px", "0px 0px"],
              clamp,
            ),
            padding: "38px 42px",
            background: "#172a32",
            border: "1px solid #496066",
            marginTop: 18,
          }}
        >
          <div
            style={{
              fontSize: 23,
              letterSpacing: 3,
              color: teal,
              marginBottom: 40,
            }}
          >
            METHODS / EXPERIMENT RECORD
          </div>
          <div style={{ fontSize: 47, color: ivory, lineHeight: 1.6 }}>
            Source & version
            <br />
            Steps to reproduce
            <br />
            Final-file checks
            <br />
            Known limitations
          </div>
          <div style={{ fontSize: 23, color: amber, marginTop: 35 }}>
            SCOPE MATTERS. EVIDENCE STAYS.
          </div>
        </Interactive.Div>
      </div>
    </Stage>
  );
}
