import { Audio } from "@remotion/media";
import { TransitionSeries } from "@remotion/transitions";
import { staticFile, useVideoConfig } from "remotion";
import { Opening } from "./Opening";
import { Choose } from "./Choose";
import { Chain } from "./Chain";
import { Evidence } from "./Evidence";
import { Closing } from "./Closing";
export function FramewrightFilm() {
  const { fps } = useVideoConfig();
  return (
    <>
      <Audio
        src={staticFile("framewright-score.wav")}
        premountFor={fps}
        volume={0.85}
      />
      <TransitionSeries>
        <TransitionSeries.Sequence
          name="Identity"
          durationInFrames={6 * fps}
          premountFor={fps}
        >
          <Opening />
        </TransitionSeries.Sequence>
        <TransitionSeries.Sequence
          name="Choose a route"
          durationInFrames={6 * fps}
          premountFor={fps}
        >
          <Choose />
        </TransitionSeries.Sequence>
        <TransitionSeries.Sequence
          name="Build the chain"
          durationInFrames={6 * fps}
          premountFor={fps}
        >
          <Chain />
        </TransitionSeries.Sequence>
        <TransitionSeries.Sequence
          name="Keep the evidence"
          durationInFrames={6 * fps}
          premountFor={fps}
        >
          <Evidence />
        </TransitionSeries.Sequence>
        <TransitionSeries.Sequence
          name="Explore Framewright"
          durationInFrames={6 * fps}
          premountFor={fps}
        >
          <Closing />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </>
  );
}
