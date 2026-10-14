import { Stage, headline, body, amber } from "./theme";
export function Closing() {
  return (
    <Stage kicker="FRAMEWRIGHT / ABVX VIDEO METHODS LAB">
      <h1
        style={{
          ...headline,
          fontFamily: "Georgia, serif",
          fontSize: 160,
          fontWeight: 400,
          marginTop: 15,
        }}
      >
        Craft the cut.
        <br />
        <span style={{ color: amber }}>Keep the evidence.</span>
      </h1>
      <p style={{ ...body, marginTop: 34 }}>
        Video methods, agent skills and lessons from real projects.
      </p>
      <div style={{ fontSize: 37, color: amber, marginTop: 32 }}>
        github.com/markoblogo/framewright
      </div>
    </Stage>
  );
}
