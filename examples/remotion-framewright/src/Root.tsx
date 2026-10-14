import { Composition, Folder } from "remotion";
import { FramewrightFilm } from "./Composition";
import { Opening } from "./Opening";
import { Choose } from "./Choose";
import { Chain } from "./Chain";
import { Evidence } from "./Evidence";
import { Closing } from "./Closing";
export function RemotionRoot() {
  return (
    <>
      <Composition
        id="Framewright"
        component={FramewrightFilm}
        durationInFrames={900}
        fps={30}
        width={1920}
        height={1080}
      />
      <Folder name="Scenes">
        <Composition
          id="Identity"
          component={Opening}
          durationInFrames={180}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Choose"
          component={Choose}
          durationInFrames={180}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Chain"
          component={Chain}
          durationInFrames={180}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Evidence"
          component={Evidence}
          durationInFrames={180}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Closing"
          component={Closing}
          durationInFrames={180}
          fps={30}
          width={1920}
          height={1080}
        />
      </Folder>
    </>
  );
}
