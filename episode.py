#!/usr/bin/env python3
"""Gera um episódio infantil ilustrado, narrado e montado com FFmpeg."""
from pathlib import Path
import math, subprocess, shutil, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
OUT = Path("build")
OUT.mkdir(exist_ok=True)

SCENES = [
("Era uma vez, numa floresta muito alegre, três amigos inseparáveis: Tico, o leão curioso; Lili, a coelhinha esperta; e Bento, o urso mais engraçado da região.", "forest"),
("Numa noite tranquila, uma estrela brilhante caiu devagarinho do céu e pousou entre as árvores. Tico arregalou os olhos: Nossa! Uma estrela perdida!", "starfall"),
("Lili se aproximou com cuidado. A estrelinha tremia e parecia triste. Estou longe da minha casa, sussurrou ela. Precisamos ajudar!, disse Lili.", "friends"),
("Bento teve uma ideia. Vamos levá-la até o alto da colina! Lá de cima, ela poderá encontrar o caminho de volta. Os três amigos seguiram juntos.", "journey"),
("A subida foi difícil. Bento escorregou numa pedra e caiu sentado. Pof! Todos riram, até a estrelinha dar uma risadinha e brilhar mais forte.", "hill"),
("No topo, os amigos ergueram a estrelinha. Ela subiu como um foguete luminoso e voltou a brilhar no céu. Obrigada pela amizade! E os três aprenderam: juntos, podemos ajudar a iluminar qualquer caminho.", "ending"),
]

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def gradient():
    im = Image.new("RGB", (W,H))
    p=im.load()
    for y in range(H):
        t=y/H
        c=(int(16+35*t), int(34+75*t), int(76+55*t))
        for x in range(W): p[x,y]=c
    return im

def tree(d,x,y,s):
    d.rectangle((x-12*s,y-5*s,x+12*s,y+100*s),fill="#75452e")
    for ox,oy,r,col in [(0,-45,65,"#247447"),(-35,-10,48,"#2d8a50"),(35,-8,48,"#1e6b43")]:
        d.ellipse((x+(ox-r)*s,y+(oy-r)*s,x+(ox+r)*s,y+(oy+r)*s),fill=col)

def character(d,x,y,kind,scale=1):
    colors={"lion":"#e9a83b","rabbit":"#f4eee5","bear":"#8b5a3c"}
    c=colors[kind]; r=68*scale
    d.ellipse((x-r,y-r,x+r,y+r),fill=c,outline="#3b2b25",width=5)
    if kind=="lion":
        d.ellipse((x-r-18,y-r-18,x+r+18,y+r+18),outline="#c87924",width=19)
        d.ellipse((x-43*scale,y-18*scale,x-25*scale,y+2*scale),fill="#2b2522")
        d.ellipse((x+25*scale,y-18*scale,x+43*scale,y+2*scale),fill="#2b2522")
        d.ellipse((x-14*scale,y+10*scale,x+14*scale,y+28*scale),fill="#3b2922")
    elif kind=="rabbit":
        d.ellipse((x-53*scale,y-150*scale,x-5*scale,y-35*scale),fill=c,outline="#3b2b25",width=4)
        d.ellipse((x+5*scale,y-150*scale,x+53*scale,y-35*scale),fill=c,outline="#3b2b25",width=4)
        d.ellipse((x-38*scale,y-18*scale,x-22*scale,y+1*scale),fill="#292323")
        d.ellipse((x+22*scale,y-18*scale,x+38*scale,y+1*scale),fill="#292323")
        d.ellipse((x-10*scale,y+12*scale,x+10*scale,y+27*scale),fill="#e88d9c")
    else:
        d.ellipse((x-68*scale,y-65*scale,x-25*scale,y-20*scale),fill=c,outline="#3b2b25",width=4)
        d.ellipse((x+25*scale,y-65*scale,x+68*scale,y-20*scale),fill=c,outline="#3b2b25",width=4)
        d.ellipse((x-38*scale,y-18*scale,x-22*scale,y+1*scale),fill="#292323")
        d.ellipse((x+22*scale,y-18*scale,x+38*scale,y+1*scale),fill="#292323")
        d.ellipse((x-14*scale,y+12*scale,x+14*scale,y+30*scale),fill="#30231f")
    d.arc((x-25*scale,y+12*scale,x+25*scale,y+48*scale),0,180,fill="#30231f",width=4)

def star(d,cx,cy,r,color="#ffe76a"):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5
        rr=r if i%2==0 else r*.43
        pts.append((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
    d.polygon(pts,fill=color,outline="#fff4b0")

def make_scene(kind,idx):
    im=gradient(); d=ImageDraw.Draw(im)
    # ground and forest
    d.ellipse((-120,500,1400,900),fill="#1d6848")
    for x in range(-20, W+100, 190): tree(d,x,420,1.0 if x%2 else .8)
    if kind in ("forest","starfall","friends","journey","hill","ending"):
        character(d,400,500,"lion",.82); character(d,620,505,"rabbit",.78); character(d,840,505,"bear",.85)
    if kind=="starfall": star(d,1010,250,65)
    if kind=="friends": star(d,1010,340,48)
    if kind=="journey":
        d.polygon([(850,530),(1050,260),(1240,530)],fill="#397b50")
        star(d,1040,250,35)
    if kind=="hill":
        d.polygon([(0,590),(500,350),(1280,590)],fill="#347e51")
        star(d,1040,300,45)
    if kind=="ending":
        star(d,640,180,85)
        for x,y in [(160,180),(300,100),(980,120),(1120,220),(800,80)]:
            star(d,x,y,13,"#fff4a3")
    d.rounded_rectangle((35,35,1245,112),radius=24,fill="#102744",outline="#ffe58a",width=3)
    title="TICO E O MISTÉRIO DA ESTRELA PERDIDA"
    d.text((W//2,74),title,font=font(30,True),fill="white",anchor="mm")
    im.save(OUT/f"scene_{idx:02d}.png")

def run(cmd):
    subprocess.run(cmd,check=True)

def main():
    if not shutil.which("espeak-ng") or not shutil.which("ffmpeg"):
        raise SystemExit("Dependências ausentes: espeak-ng e ffmpeg são necessários.")
    clips=[]
    for i,(text,kind) in enumerate(SCENES,1):
        make_scene(kind,i)
        wav=OUT/f"voice_{i:02d}.wav"
        run(["espeak-ng","-v","pt-br","-s","145","-p","48","-a","175","-w",str(wav),text])
        duration=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(wav)],text=True).strip())
        video=OUT/f"clip_{i:02d}.mp4"
        frames=max(1,math.ceil(duration*25))
        # Movimento suave de aproximação em cada ilustração.
        run(["ffmpeg","-y","-loop","1","-i",str(OUT/f"scene_{i:02d}.png"),"-i",str(wav),
             "-vf",f"zoompan=z='min(zoom+0.00035,1.035)':d={frames}:s=1280x720:fps=25,format=yuv420p",
             "-t",str(duration),"-c:v","libx264","-preset","veryfast","-crf","24","-c:a","aac","-b:a","128k","-shortest",str(video)])
        clips.append(video)
    listing=OUT/"concat.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in clips),encoding="utf-8")
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-c","copy","-movflags","+faststart","O_Misterio_da_Estrela_Perdida.mp4"])
    print("EPISODIO GERADO: O_Misterio_da_Estrela_Perdida.mp4")

if __name__=="__main__": main()
