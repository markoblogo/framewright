import {
  Interactive,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Stage, headline, body, amber, teal, clamp } from "./theme";
export function Chain() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Stage kicker="02 / BUILD THE CHAIN">
      <h1 style={headline}>
        The right tools.
        <br />
        <span style={{ color: amber }}>Working together.</span>
      </h1>
      <div
        style={{
          position: "relative",
          display: "flex",
          gap: 38,
          marginTop: 65,
        }}
      >
        <Interactive.Div
          name="Picture tool"
          style={{
            opacity: interpolate(frame, [0.3 * fps, 0.7 * fps], [0, 1], clamp),
            width: 525,
            borderTop: "4px solid #E7BA6A",
            paddingTop: 26,
          }}
        >
          <div style={{ fontSize: 24, color: teal }}>01 / PICTURE</div>
          <div style={{ fontSize: 49, marginTop: 18 }}>Render the idea.</div>
          <div style={{ ...body, fontSize: 29 }}>Brag · Flute · Remotion</div>
        </Interactive.Div>
        <Interactive.Div
          name="Sound tool"
          style={{
            opacity: interpolate(frame, [1.1 * fps, 1.5 * fps], [0, 1], clamp),
            width: 525,
            borderTop: "4px solid #8DAEB0",
            paddingTop: 26,
          }}
        >
          <div style={{ fontSize: 24, color: teal }}>02 / SOUND</div>
          <div style={{ fontSize: 49, marginTop: 18 }}>Give it a voice.</div>
          <div style={{ ...body, fontSize: 29 }}>
            Local narration · original music
          </div>
        </Interactive.Div>
        <Interactive.Div
          name="Finish tool"
          style={{
            opacity: interpolate(frame, [1.9 * fps, 2.3 * fps], [0, 1], clamp),
            width: 525,
            borderTop: "4px solid #F6EFDB",
            paddingTop: 26,
          }}
        >
          <div style={{ fontSize: 24, color: teal }}>03 / FINISH</div>
          <div style={{ fontSize: 49, marginTop: 18 }}>Check the result.</div>
          <div style={{ ...body, fontSize: 29 }}>
            Encoded video · audio · thumbnail
          </div>
        </Interactive.Div>
      </div>
      <p style={{ ...body, fontSize: 28, marginTop: 50 }}>
        Combine tools when the brief needs it. Verify each new combination.
      </p>
    </Stage>
  );
}
