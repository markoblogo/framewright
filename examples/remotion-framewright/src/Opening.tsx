import {
  AbsoluteFill,
  CanvasImage,
  Interactive,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { clamp, ink } from "./theme";
export function Opening() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: ink }}>
      <Interactive.Div
        name="Framewright cover reveal"
        style={{
          position: "absolute",
          inset: 0,
          opacity: interpolate(
            frame,
            [0, 0.5 * fps, 5.6 * fps, 6 * fps],
            [0, 1, 1, 0],
            clamp,
          ),
          scale: interpolate(frame, [0, 6 * fps], [1, 1.035], clamp),
        }}
      >
        <CanvasImage
          src={staticFile("framewright-cover.png")}
          premountFor={fps}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </Interactive.Div>
    </AbsoluteFill>
  );
}
