import os, struct, zlib, math
W=H=1024
PAPER=(242,235,218); INK=(22,32,43); NAVY=(17,34,53); WHITE=(249,246,235)
FONT={
'A':['01110','10001','10001','11111','10001','10001','10001'],'B':['11110','10001','10001','11110','10001','10001','11110'],'C':['01111','10000','10000','10000','10000','10000','01111'],'D':['11110','10001','10001','10001','10001','10001','11110'],'E':['11111','10000','10000','11110','10000','10000','11111'],'F':['11111','10000','10000','11110','10000','10000','10000'],'G':['01111','10000','10000','10111','10001','10001','01111'],'H':['10001','10001','10001','11111','10001','10001','10001'],'I':['11111','00100','00100','00100','00100','00100','11111'],'J':['00111','00010','00010','00010','10010','10010','01100'],'K':['10001','10010','10100','11000','10100','10010','10001'],'L':['10000','10000','10000','10000','10000','10000','11111'],'M':['10001','11011','10101','10101','10001','10001','10001'],'N':['10001','11001','10101','10011','10001','10001','10001'],'O':['01110','10001','10001','10001','10001','10001','01110'],'P':['11110','10001','10001','11110','10000','10000','10000'],'Q':['01110','10001','10001','10001','10101','10010','01101'],'R':['11110','10001','10001','11110','10100','10010','10001'],'S':['01111','10000','10000','01110','00001','00001','11110'],'T':['11111','00100','00100','00100','00100','00100','00100'],'U':['10001','10001','10001','10001','10001','10001','01110'],'V':['10001','10001','10001','10001','10001','01010','00100'],'W':['10001','10001','10001','10101','10101','10101','01010'],'X':['10001','10001','01010','00100','01010','10001','10001'],'Y':['10001','10001','01010','00100','00100','00100','00100'],'Z':['11111','00001','00010','00100','01000','10000','11111'],
'0':['01110','10001','10011','10101','11001','10001','01110'],'1':['00100','01100','00100','00100','00100','00100','01110'],'2':['01110','10001','00001','00010','00100','01000','11111'],'3':['11110','00001','00001','01110','00001','00001','11110'],'4':['00010','00110','01010','10010','11111','00010','00010'],'5':['11111','10000','10000','11110','00001','00001','11110'],'6':['01110','10000','10000','11110','10001','10001','01110'],'7':['11111','00001','00010','00100','01000','01000','01000'],'8':['01110','10001','10001','01110','10001','10001','01110'],'9':['01110','10001','10001','01111','00001','00001','01110'],
'.':['00000','00000','00000','00000','00000','00110','00110'],',':['00000','00000','00000','00000','00110','00110','00100'],':':['00000','00110','00110','00000','00110','00110','00000'],';':['00000','00110','00110','00000','00110','00110','00100'],'!':['00100','00100','00100','00100','00100','00000','00100'],'?':['01110','10001','00001','00010','00100','00000','00100'],"'":['00100','00100','00010','00000','00000','00000','00000'],'-':['00000','00000','00000','11111','00000','00000','00000'],'/':['00001','00010','00010','00100','01000','01000','10000'],'(':['00010','00100','01000','01000','01000','00100','00010'],')':['01000','00100','00010','00010','00010','00100','01000'],'%':['11001','11010','00100','01000','10110','00110','00000'],'&':['01100','10010','10100','01000','10101','10010','01101'],'+':['00000','00100','00100','11111','00100','00100','00000'],'=':['00000','11111','00000','11111','00000','00000','00000'],'$':['00100','01111','10100','01110','00101','11110','00100'],' ':['00000']*7}
rows=[bytearray(W*3) for _ in range(H)]
def rect(x,y,w,h,c):
 x0=max(0,int(x)); x1=min(W,int(x+w)); y0=max(0,int(y)); y1=min(H,int(y+h))
 if x0>=x1 or y0>=y1:return
 span=bytes(c)*(x1-x0)
 for yy in range(y0,y1): rows[yy][x0*3:x1*3]=span
def line(x0,y0,x1,y1,c,t=2):
 dx=abs(x1-x0); sx=1 if x0<x1 else -1; dy=-abs(y1-y0); sy=1 if y0<y1 else -1; err=dx+dy
 while True:
  rect(x0-t//2,y0-t//2,t,t,c)
  if x0==x1 and y0==y1:break
  e=2*err
  if e>=dy:err+=dy;x0+=sx
  if e<=dx:err+=dx;y0+=sy
def circle(cx,cy,r,c):
 for yy in range(max(0,cy-r),min(H,cy+r+1)):
  d=r*r-(yy-cy)*(yy-cy)
  if d>=0:
   dx=int(d**.5);rect(cx-dx,yy,2*dx+1,1,c)
def poly(points,c):
 for yy in range(max(0,min(y for x,y in points)),min(H-1,max(y for x,y in points))+1):
  xs=[]
  for i,(x1,y1) in enumerate(points):
   x2,y2=points[(i+1)%len(points)]
   if y1!=y2 and min(y1,y2)<=yy<max(y1,y2):xs.append(int(x1+(yy-y1)*(x2-x1)/(y2-y1)))
  xs.sort()
  for i in range(0,len(xs)-1,2):rect(xs[i],yy,xs[i+1]-xs[i]+1,1,c)
def text_width(s,scale):return max(0,len(s)*6*scale-scale)
def draw_text(x,y,s,scale,c):
 for ch in s.upper():
  for ry,pat in enumerate(FONT.get(ch,FONT[' '])):
   for rx,b in enumerate(pat):
    if b=='1':rect(x+rx*scale,y+ry*scale,scale,scale,c)
  x+=6*scale
def wrap(s,maxw,scale,maxlines=2):
 out=[];cur=''
 for word in s.upper().split():
  trial=(cur+' '+word).strip()
  if text_width(trial,scale)<=maxw:cur=trial
  elif cur:out.append(cur);cur=word
  else:cur=word
 if cur:out.append(cur)
 while len(out)>maxlines:out.pop()
 if out and text_width(out[-1],scale)>maxw:out[-1]=out[-1][:max(1,maxw//(6*scale))]
 return out
stories=[
('GULF','Iran hits Kuwait base and Bahrain after US strike','US aircraft had struck an Iranian missile site on Qeshm Island.','GULF'),
('UKRAINE','Kerch Bridge arch falls after Ukrainian attack','One arch fell into the strait as a drone and missile attack partly collapsed the bridge.','UKRAINE'),
('ASIA','Xi and Putin meet before planned Trump talks','At APEC, Xi spoke against trade protectionism before planned three-way talks with Trump.','ASIA'),
('USA','Peltola win gives Democrats Senate majority','Democrats hold a 56 to 44 majority in the incoming Senate.','USA'),
('HEALTH','Congo Ebola outbreak passes 11,000 cases','About three in four infected children under five do not survive.','HEALTH'),
('TECH','Nvidia reports record $115.8 billion revenue','The board rejected Jensen Huang offer to return as chief executive.','TECH')]
def scene(i,x,y):
 if i==0:
  rect(x,y,488,120,(12,43,64));rect(x,y+72,488,48,(21,70,91));poly([(x,y+82),(x+74,y+59),(x+121,y+69),(x+166,y+47),(x+209,y+62),(x+250,y+48),(x+294,y+66),(x+352,y+54),(x+420,y+71),(x+488,y+61),(x+488,y+120),(x,y+120)],(188,164,125))
  for px in (x+136,x+365):rect(px-18,y+72,36,10,(43,48,49));circle(px,y+68,5,(243,202,105))
  line(x+52,y+25,x+136,y+67,(255,199,107),2);line(x+52,y+25,x+113,y+52,(255,199,107),2);line(x+435,y+18,x+365,y+64,(255,199,107),2);line(x+435,y+18,x+391,y+47,(255,199,107),2)
  for px,py in ((x+136,y+67),(x+365,y+64)):
   for dx,dy in ((0,-11),(0,11),(-11,0),(11,0),(-8,-8),(8,8)):line(px,py,px+dx,py+dy,(255,228,156),2)
  draw_text(x+18,y+12,'KUWAIT',1,WHITE);draw_text(x+342,y+12,'BAHRAIN',1,WHITE)
 elif i==1:
  rect(x,y,488,120,(47,125,164));rect(x,y+88,488,32,(31,82,116))
  for k in range(7):line(x+18+k*72,y+99,x+60+k*72,y+99,(99,167,187),1)
  line(x+18,y+43,x+192,y+43,(229,217,181),8);line(x+296,y+43,x+470,y+43,(229,217,181),8);line(x+192,y+43,x+226,y+70,(229,217,181),8);line(x+226,y+70,x+257,y+66,(229,217,181),8);line(x+257,y+66,x+296,y+43,(229,217,181),8)
  for px in (x+82,x+165,x+322,x+405):line(px,y+47,px,y+104,(205,198,170),5);line(px-25,y+104,px+25,y+104,(205,198,170),4)
  for px,py,r in ((x+214,y+26,14),(x+233,y+20,18),(x+253,y+28,12)):circle(px,py,r,(107,112,110))
  circle(x+238,y+22,8,(128,127,119))
 elif i==2:
  rect(x,y,488,120,(231,201,145));rect(x,y+81,488,39,(143,161,151))
  for px,wid,ht,col in ((18,43,62,(54,91,110)),(69,52,83,(45,81,101)),(132,40,54,(73,104,113)),(184,64,96,(38,71,92)),(266,48,70,(52,91,104)),(326,55,88,(40,75,94)),(397,45,61,(61,97,103)),(448,31,77,(44,79,93))):
   rect(x+px,y+81-ht,wid,ht,col)
   for wy in range(y+89-ht,y+76,14):
    for wx in range(x+px+8,x+px+wid-4,12):rect(wx,wy,4,4,(235,205,139))
  line(x+115,y+18,x+115,y+75,(48,54,54),2);rect(x+117,y+20,34,21,(188,55,45));circle(x+125,y+26,2,(246,215,113));line(x+365,y+12,x+365,y+75,(48,54,54),2);rect(x+367,y+15,42,22,(248,245,230));rect(x+367,y+22,42,7,(57,82,143));rect(x+367,y+30,42,7,(201,61,53))
 elif i==3:
  rect(x,y,488,120,(189,211,224));rect(x,y+86,488,34,(110,142,160));poly([(x+125,y+57),(x+244,y+20),(x+363,y+57)],(57,78,91));rect(x+135,y+57,218,8,(57,78,91))
  for px in range(x+150,x+344,32):rect(px,y+64,15,37,(234,230,209));rect(px-3,y+100,21,5,(57,78,91))
  rect(x+123,y+105,244,7,(57,78,91));circle(x+244,y+23,19,(57,78,91));rect(x+238,y+5,12,18,(57,78,91))
  for px,py in ((x+85,y+24),(x+401,y+20),(x+431,y+39),(x+77,y+52)):circle(px,py,2,(250,247,229))
  rect(x+391,y+75,64,37,(122,79,53));rect(x+400,y+82,46,23,(228,215,183));rect(x+420,y+81,5,16,(57,78,91))
 elif i==4:
  rect(x,y,488,120,(212,224,207));poly([(x+176,y+14),(x+214,y+8),(x+246,y+18),(x+271,y+17),(x+285,y+37),(x+274,y+53),(x+267,y+77),(x+247,y+107),(x+232,y+113),(x+220,y+89),(x+205,y+72),(x+193,y+52),(x+174,y+40)],(73,121,92));poly([(x+264,y+17),(x+283,y+13),(x+295,y+22),(x+287,y+31)],(73,121,92))
  for px,py in ((x+245,y+54),(x+255,y+61),(x+238,y+67),(x+260,y+73)):circle(px,py,4,(191,55,49))
  circle(x+374,y+59,31,(184,63,56));circle(x+374,y+59,19,(233,132,111))
  for a in range(0,360,45):
   ax=x+374+int(31*math.cos(a*math.pi/180));ay=y+59+int(31*math.sin(a*math.pi/180));bx=x+374+int(43*math.cos(a*math.pi/180));by=y+59+int(43*math.sin(a*math.pi/180));line(ax,ay,bx,by,(184,63,56),4);circle(bx,by,4,(184,63,56))
  for px,py in ((x+367,y+52),(x+381,y+64),(x+370,y+68)):circle(px,py,3,(255,224,184))
  draw_text(x+16,y+15,'DR CONGO',1,INK)
 else:
  rect(x,y,488,120,(35,53,71));rect(x+52,y+19,178,82,(25,34,42));rect(x+64,y+30,154,60,(50,105,76))
  for px in range(x+61,x+224,18):line(px,y+10,px,y+20,(185,193,178),3);line(px,y+101,px,y+111,(185,193,178),3)
  for py in range(y+30,y+100,16):line(x+42,py,x+52,py,(185,193,178),3);line(x+230,py,x+240,py,(185,193,178),3)
  draw_text(x+87,y+53,'NVIDIA',1,(227,241,200))
  for bx,by,bh in ((286,91,19),(324,74,36),(362,54,56),(400,31,79)):rect(x+bx,y+by,27,bh,(91,181,109))
  line(x+276,y+111,x+445,y+111,(214,221,209),2);line(x+287,y+75,x+334,y+61,(191,227,166),3);line(x+334,y+61,x+373,y+43,(191,227,166),3);line(x+373,y+43,x+420,y+22,(191,227,166),3)
def panel(i,story,x,y):
 region,headline,caption,tag=story
 rect(x,y,488,258,(139,127,106));rect(x+1,y+1,486,256,PAPER);scene(i,x,y);rect(x,y+121,488,2,(139,127,106))
 chip={'GULF':(161,91,54),'UKRAINE':(46,111,153),'ASIA':(171,77,54),'USA':(56,91,127),'HEALTH':(59,111,79),'TECH':(70,125,79)}[tag]
 rect(x+12,y+128,84,18,chip);draw_text(x+18,y+133,tag,1,WHITE)
 heads=wrap(headline,464,2,2);hy=y+153
 rect(x+4,hy,3,34,chip)
 for j,s in enumerate(heads):draw_text(x+12,hy+j*17,s,2,INK)
 caps=wrap(caption,464,1,2);cy=hy+len(heads)*17+5
 for j,s in enumerate(caps):draw_text(x+12,cy+j*9,s,1,(58,65,67))
rect(0,0,W,H,PAPER);rect(0,0,W,140,NAVY)
draw_text((W-text_width('THE WORLD IN ONE IMAGE',6))//2,18,'THE WORLD IN ONE IMAGE',6,WHITE)
draw_text((W-text_width('WEDNESDAY 18 NOVEMBER 2026',4))//2,91,'WEDNESDAY 18 NOVEMBER 2026',4,(233,214,166))
rect(16,145,992,2,(165,151,124))
for i,(story,(x,y)) in enumerate(zip(stories,[(16,156),(520,156),(16,426),(520,426),(16,696),(520,696)])):panel(i,story,x,y)
rect(16,966,992,1,(166,153,127));footer='SOURCES: REUTERS - AP - AFP - 18 NOVEMBER 2026';draw_text((W-text_width(footer,1))//2,976,footer,1,(60,65,65))
def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
raw=b''.join(b'\0'+bytes(row) for row in rows)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
out=os.environ.get('MAKEFUN_OUTPUT_DIR','/output');os.makedirs(out,exist_ok=True)
with open(os.path.join(out,'entry.png'),'wb') as f:f.write(png)
