from pathlib import Path
import manimgx as m

m.config.pixel_width=1920
m.config.pixel_height=1080
m.config.frame_rate=30
m.config.background_color='#081522'
GOLD='#D9B56B'; WHITE='#F6F3E9'; TEAL='#69C4C1'; MUTED='#93A7B7'; PANEL='#142B3B'
B=Path(__file__).parent

def txt(text,size=34,color=WHITE,pos=(0,0,0)):
    return m.Text(text,font='sans-serif',font_size=size,color=color).move_to(pos)

def card(label,pos,color=GOLD):
    box=m.RoundedRectangle(width=2.65,height=1.15,corner_radius=.12,color=color,fill_color=PANEL,fill_opacity=1,stroke_width=2)
    title=txt(label,27).move_to(box)
    return m.VGroup(box,title).move_to(pos)

def compass(center=(0,0,0),scale=1):
    ring=m.Circle(radius=.7,color=GOLD,stroke_width=2)
    points=m.VGroup(*[m.Polygon([0,1.2,0],[.2,.2,0],[0,0,0],[-.2,.2,0],color=GOLD,fill_color=GOLD,fill_opacity=1,stroke_width=0).rotate(a*m.DEGREES,about_point=m.ORIGIN) for a in (0,90,180,270)])
    return m.VGroup(ring,points).scale(scale).move_to(center)

class MN7RGuide(m.Scene):
    def construct(self):
        brand=txt('MN7R  /  COMMODITY BROKERAGE LIBRARY',16,MUTED,(-2.8,3.52,0))
        footer=txt('ILLUSTRATIVE WORKFLOW · PUBLIC PRODUCT GUIDE',18,MUTED,(0,-3.62,0))
        self.add(brand,footer)
        title=txt('A DEAL IS ONLY\nTHE BEGINNING.',49,WHITE,(-2.65,.6,0))
        mark=compass((4.3,.6,0),1.15)
        self.play(m.FadeIn(title,shift=m.UP*.3),m.Create(mark),run_time=.8)
        sub=txt('One workspace. A connected process.',25,MUTED,(-2.7,-1.05,0))
        self.play(m.FadeIn(sub),m.Rotate(mark,angle=m.PI/2),run_time=.8)
        self.wait(1.4)
        # 3–8s: scattered tasks become a connected workflow, no fabricated data.
        self.play(m.FadeOut(title),m.FadeOut(sub),m.FadeOut(mark),run_time=.6)
        heading=txt('FROM CONTACT TO EXECUTION',38,GOLD,(0,2.65,0))
        cs=[card('CLIENTS',(-4.6,.2,0)),card('OFFERS',(-1.5,-1.1,0)),card('DEALS',(1.5,.7,0)),card('EXECUTION',(4.6,-.7,0))]
        self.play(m.FadeIn(heading),*[m.FadeIn(c,shift=m.DOWN*.3) for c in cs],run_time=.6)
        self.play(*[c.animate.move_to((x,0,0)) for c,x in zip(cs,[-4.8,-1.6,1.6,4.8])],run_time=1)
        arrows=m.VGroup(*[m.Arrow([x+1.34,0,0],[x+1.86,0,0],buff=0,color=TEAL,stroke_width=3) for x in [-4.8,-1.6,1.6]])
        self.play(m.Create(arrows),run_time=.8)
        flow_note=txt('Shared context. Visible handoffs.',27,MUTED,(0,-1.65,0))
        signal=m.Dot([-4.8,-.85,0],radius=.085,color=TEAL)
        self.add(signal)
        self.play(m.FadeIn(flow_note),signal.animate.move_to([4.8,-.85,0]),run_time=1.5)
        self.play(m.FadeOut(signal),m.Indicate(cs[-1],color=TEAL,scale_factor=1.04),run_time=.5)
        # 8–12s: explicit roles, with human ownership.
        self.play(m.FadeOut(flow_note),m.FadeOut(arrows),*[c.animate.scale(.72).shift(m.UP*.6) for c in cs],m.Transform(heading,txt('CLARITY FOR EVERY ROLE',38,GOLD,(0,2.65,0))),run_time=.6)
        roles=m.VGroup(card('BROKER',(-3.4,-1.15,0),TEAL),card('TEAM LEAD',(0,-1.15,0),TEAL),card('OPERATOR',(3.4,-1.15,0),TEAL))
        self.play(m.FadeIn(roles,shift=m.UP*.3),run_time=.9)
        connectors=m.VGroup(*[m.Line([x,-.4,0],[x,.05,0],color=TEAL,stroke_width=2) for x in [-3.4,0,3.4]])
        self.play(m.Create(connectors),run_time=1.4)
        self.wait(1.1)
        # 12–15s: AI support, without promising unattended authority.
        self.play(*[m.FadeOut(x) for x in [heading,roles,connectors,*cs]],run_time=.6)
        ai=compass((-3.7,.25,0),.9)
        aititle=txt('OPERATING DISCIPLINE.\nAI SUPPORT.',42,WHITE,(1.4,.65,0))
        ainote=txt('Understand the workflow and role model.',25,MUTED,(.7,-1.35,0))
        self.play(m.Create(ai),m.FadeIn(aititle),run_time=.7)
        self.play(m.FadeIn(ainote),m.Rotate(ai,angle=m.PI/2),run_time=.7)
        self.wait(1)
        # 15–20s: real owner cover, readable title and source-backed free CTA.
        self.play(m.FadeOut(ai),m.FadeOut(aititle),m.FadeOut(ainote),run_time=.5)
        cover=m.ImageMobject(str(B/'assets/owner-cover.jpeg')).scale_to_fit_height(5.65).move_to((4.15,0,0))
        hero=txt('MN7R\nPRODUCT GUIDE',48,WHITE,(-2.45,1.2,0))
        self.play(m.FadeIn(cover,shift=m.RIGHT*.25),m.FadeIn(hero,shift=m.UP*.2),run_time=.8)
        small=txt('A public guide to the\ncommodity brokerage workspace.',25,MUTED,(-2.45,-.45,0))
        cta=txt('FREE ENGLISH EDITION',26,GOLD,(-2.45,-1.65,0))
        address=txt('PDF + EPUB  ·  ABVX.XYZ',23,WHITE,(-2.45,-2.3,0))
        self.play(m.FadeIn(small),m.FadeIn(cta),m.FadeIn(address),run_time=.7)
        self.wait(3)
