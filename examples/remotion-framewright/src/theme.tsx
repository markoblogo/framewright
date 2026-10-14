import type { CSSProperties, ReactNode } from "react";
import {
  AbsoluteFill,
  Interactive,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
export const ink = "#101D24",
  ivory = "#F6EFDB",
  amber = "#E7BA6A",
  teal = "#8DAEB0";
export const font = "'Helvetica Neue', Arial, sans-serif";
export const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;
export function Stage({
  children,
  kicker,
}: {
  children: ReactNode;
  kicker: string;
}) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        backgroundColor: ink,
        color: ivory,
        fontFamily: font,
        padding: "96px 120px",
        overflow: "hidden",
      }}
    >
      <Interactive.Div
        name="Scene entrance"
        style={{
          opacity: interpolate(
            frame,
            [0, 0.35 * fps, 5.7 * fps, 6 * fps],
            [0, 1, 1, 0],
            clamp,
          ),
          translate: interpolate(
            frame,
            [0, 0.6 * fps],
            ["0px 24px", "0px 0px"],
            clamp,
          ),
        }}
      >
        <div
          style={{
            fontSize: 23,
            letterSpacing: 5,
            color: teal,
            marginBottom: 40,
          }}
        >
          {kicker}
        </div>
        {children}
      </Interactive.Div>
      <div
        style={{
          position: "absolute",
          bottom: 72,
          left: 120,
          right: 120,
          height: 2,
          background: "#33454b",
        }}
      >
        <Interactive.Div
          name="Scene progress"
          style={{
            height: 2,
            background: amber,
            width: interpolate(frame, [0, 6 * fps], ["0%", "100%"], clamp),
          }}
        />
      </div>
    </AbsoluteFill>
  );
}
export const headline: CSSProperties = {
  fontSize: 106,
  lineHeight: 1.04,
  fontWeight: 650,
  letterSpacing: -4,
  margin: 0,
};
export const body: CSSProperties = {
  fontSize: 37,
  lineHeight: 1.35,
  color: "#c4d3d3",
};
