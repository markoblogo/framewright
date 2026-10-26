# ABVX metadata

SEO title: AI Video Production: Repeatable Workflows with Framewright

Slug: ai-video-production-repeatable-workflows-framewright-01

Meta description: How I am developing repeatable AI video workflows with Framewright: photo films, animated stories, precise revisions and a small Blender experiment.

Excerpt: A good first render is only part of making a video. In the first Framewright Studio Notes, I look at three published experiments and the work behind them: keeping decisions, revising individual shots and preparing characters and sets for reuse.

Collection: Framewright Studio Notes
Content type: development-journal-with-production-case-studies
Language: en

Primary topic tags: ai-video-production, framewright, ai-agents, video-workflows, procedural-animation, photo-animation, blender

Additional tags for Book Readiness Radar: agent-directed-production, scene-planning, evidence-led-workflows, precise-video-revisions, reusable-characters, production-case-studies, tool-independent-filmmaking

Cover file: framewright-studio-notes-01-cover.png

Cover alt: A cinematic miniature studio with a camera, repeated arch-and-sphere scenes and amber lighting, beside the headline Making AI Video Production Repeatable.

---

# Making AI Video Production Repeatable

*Framewright Studio Notes #1 — 26 October 2026*

A request as small as “change the light in this shot” can become surprisingly complicated in an AI-assisted video project. The camera should stay where it was. The action should keep its timing. The sound should still land on the same moment. And the version I already accepted should remain available.

That is the practical problem behind my recent work on [Framewright](https://github.com/markoblogo/framewright), an open-source toolkit I am developing for a video studio run with an AI agent. I use it to plan productions, keep sources and decisions together, try tools and prepare finished publication packages.

This is the first in a weekly series about that work. I will use actual videos to show what the methods can do, explain what changed and keep the remaining limitations visible.

## Six photographs become a small film

One recent experiment began with six photographs of a calligraphic installation by Pokras Lampas. I wanted a short art film with camera movement, depth and atmosphere.

The resulting thirty-second study uses a staged scene, protected image layers and a planned camera path. Preserving the supplied calligraphy was part of the brief. The soundtrack also needed a revision: the first piano treatment felt too generic for the object. A quieter, bell-toned electronic atmosphere worked better.

[Watch: Seals of Good Intentions](https://youtu.be/6c3JXdIiosg)

The reusable part is the sequence of decisions: inspect the photographs, establish what must remain intact, plan the camera, test the framing, then shape the sound around the image. Another photo series will need its own choices, but that process can carry over.

## A small dog exposes a useful production problem

Another short film follows a dog through a forest toward a light. Its first extended ending did not work: an extra bright object appeared without a clear cause, and the running looked as though the dog was staying in place.

The correction connected the events. A small light falls in the distance. Its impact gradually illuminates the forest and changes the music. The dog turns, runs toward that location and disappears into the glow.

[Watch: A Dog Follows a Falling Light](https://youtu.be/B4zdWfFIkNE)

Making this reliable required attention to the saved animation state. Returning to the same moment needed to reconstruct the same pose. The lesson is useful beyond this film: a clear revision needs an identified defect, a desired change and an explicit description of what must survive the edit.

## What I added to the workbench

The latest local work gives experiments a more consistent structure: a bounded question, common source files, baseline and candidate outputs, recorded checks, and a review package. Technical results and my creative judgement are kept separately.

I then tested a saved-shot workflow in Blender. An original three-second scene was rendered twice; all thirty-six source frames matched. A separately rendered twelve-frame interval matched the corresponding frames from the full shot. Changing one light altered that interval while preserving the tested camera, action and audio timing. A second camera setup reused the saved scene.

This is deliberately narrow evidence: one tiny Cycles CPU scene, one Blender build and one Mac. It demonstrates a controlled local revision. It does not establish that every rig, simulation or machine will behave the same way.

I also prepared versioned “passports” for recurring characters and environments: approved references, proportions, clothing, scale, materials, rig, actions and constraints. A shot can point to one specific version. The current forms are incomplete preparation for future production; they do not automatically recognise a character or certify that a rendered face matches a reference.

The work described here belongs to the experimental v0.4.0 development cycle. The linked films are published production examples; the new helpers retain the narrow test scopes described above.

## The broader workflow

For a short introduction to the production approach, I made a two-host explanation using real examples:

[Watch: How an AI Agent Turns an Idea into a Finished Video](https://youtu.be/n1wuySSYQcQ)

It also has an unfinished edge worth keeping in view: I accepted the explanation and voices, while the photographic presenters’ facial motion still needs improvement. A finished upload can supply both a useful example and a specific next task.

The direction I want to develop is straightforward: retain the sources, turn the idea into scenes, keep picture and sound on a shared timeline, make controlled revisions and check the final export.

I am collecting this experience for a future practical book about working with AI-assisted video production. Framewright will be one implementation and a source of case studies. The methods should also be usable with other tools, including a manually maintained production folder and an ordinary editor.

The next useful step is to apply the saved-shot and continuity work to a real recurring character and environment. That will test how well these preparations survive an actual film.

[Explore Framewright on GitHub](https://github.com/markoblogo/framewright)
