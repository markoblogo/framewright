import {
  Interactive,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Stage, headline, body, amber, teal, clamp } from "./theme";
export function Choose() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Stage kicker="01 / START WITH THE TASK">
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 90,
          alignItems: "center",
        }}
      >
        <div>
          <h1 style={headline}>
            One brief.
            <br />
            <span style={{ color: amber }}>A better route.</span>
          </h1>
          <p style={body}>
            Choose a method for the
            <br />
            film you want to make.
          </p>
        </div>
        <div style={{ display: "grid", gap: 22, paddingTop: 15 }}>
          <Interactive.Div
            name="Software launch"
            style={{
              opacity: interpolate(
                frame,
                [0.4 * fps, 0.9 * fps],
                [0, 1],
                clamp,
              ),
              translate: interpolate(
                frame,
                [0.4 * fps, 0.9 * fps],
                ["50px 0px", "0px 0px"],
                clamp,
              ),
              borderBottom: "1px solid #435358",
              padding: "20px 0",
            }}
          >
            <div style={{ fontSize: 23, color: teal }}>SOFTWARE</div>
            <div style={{ fontSize: 52, marginTop: 8 }}>Launch a product.</div>
          </Interactive.Div>
          <Interactive.Div
            name="Book trailer"
            style={{
              opacity: interpolate(frame, [1 * fps, 1.5 * fps], [0, 1], clamp),
              translate: interpolate(
                frame,
                [1 * fps, 1.5 * fps],
                ["50px 0px", "0px 0px"],
                clamp,
              ),
              borderBottom: "1px solid #435358",
              padding: "20px 0",
            }}
          >
            <div style={{ fontSize: 23, color: teal }}>BOOKS</div>
            <div style={{ fontSize: 52, marginTop: 8 }}>Tell a story.</div>
          </Interactive.Div>
          <Interactive.Div
            name="React interface"
            style={{
              opacity: interpolate(
                frame,
                [1.6 * fps, 2.1 * fps],
                [0, 1],
                clamp,
              ),
              translate: interpolate(
                frame,
                [1.6 * fps, 2.1 * fps],
                ["50px 0px", "0px 0px"],
                clamp,
              ),
              borderBottom: "1px solid #435358",
              padding: "20px 0",
            }}
          >
            <div style={{ fontSize: 23, color: teal }}>REACT UI</div>
            <div style={{ fontSize: 52, marginTop: 8 }}>
              Move through the interface.
            </div>
          </Interactive.Div>
        </div>
      </div>
    </Stage>
  );
}
