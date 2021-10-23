"""
this script contains predefined duck geometries
"""


def horse():
    return '''\\newcommand{\\horse}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\path (0.1,0.1) rectangle (2.7,2.4);
    \\begin{pgfinterruptboundingbox}
      \\begin{scope}[yshift=-6]
        \\clip[rotate=-5] (0.68,2.38) ellipse (0.3 and 0.4);
        \\fill[brown,rotate=-5](0.28,2.26)ellipse (0.3 and 0.4);
      \\end{scope}
      \\duck[
        body=brown,
        mohican=brown!50!black,
        horsetail
      ]
      \\begin{scope}[yshift=-5,xshift=1]
        \\clip[rotate=-5] (0.68,2.38) ellipse (0.3 and 0.4);
        \\fill[brown,rotate=-5](1.06,2.2) ellipse (0.3 and 0.4);
      \\end{scope}
    \\end{pgfinterruptboundingbox}
  \\end{tikzpicture}
}
'''

def unicorn():
    return '''\\newcommand{\\unicorn}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\duck[body=pink,
      unicorn=magenta!60!violet,
      longhair=magenta!60!violet]
  \\end{tikzpicture}
}
'''

def bunny():
    return '''\\newcommand{\\bunny}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\duck[
      body=white!80!brown,
      bill=white!60!brown,
      bunny,
      longhair=white!60!brown
    ]
    \\fill[white!60!brown] (tail) circle (0.2);
  \\end{tikzpicture}
}
'''

def sheep():
    return '''\\newcommand{\\sheep}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\duck[
      body=white!90!brown,
      bill=white!60!brown,
      sheep
    ]
  \\end{tikzpicture}
}
'''

def girl_with_pearl_earring_colours():
    return '''\\definecolor{skin}{RGB}{255,209,181}
\\definecolor{lblue}{RGB}{176,172,188}
\\definecolor{lbrown}{RGB}{236,213,163}
\\definecolor{dbrown}{RGB}{176,134,95}
\\definecolor{billcol}{RGB}{230,132,82}
'''

def girl_with_pearl_earring():
    return '''\\newcommand{\\girlwithpearlearring}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\fill[black] (-0.1,0.4) rectangle (1.9,2.8);
    \\clip (-0.1,0.4) rectangle (1.9,2.8);
    \duck[
      body=skin,
      jacket=dbrown!10!white,
      bill=billcol
    ]
    \\fill[dbrown]  (0.490,1.145) .. controls (0.267, 1.102) and (-0.125,0.657) .. (0.289,0.261) .. controls (0.704,-0.135) and ( 2.863,0.130) .. (1.818,1.419) .. controls (0.880, 0.946) and ( 1.240,1.378) .. (0.46,0.55) -- cycle;
    \\begin{scope}[scale=0.12,xshift=-1.3cm,yshift=3.8cm]
      \\fill[lbrown] (7.7941,13.7509) .. controls (10.8320,13.4186) and (11.7764,12.3930) .. (12.6964,10.9465) .. controls (12.6964,10.9465) and (12.6769,5.6002) .. (12.9122,2.0156) .. controls (13.2041,1.7780) and (13.7523,1.8952) .. (14.0339,2.1451) .. controls (14.2660,2.3512) and (13.9970,2.8707) .. (14.2496,3.0512) .. controls (14.6140,3.3115) and (15.1783,2.7387) .. (15.5871,2.9217) .. controls (15.8312,3.0309) and (16.0169,3.3052) .. (16.0616,3.5688) .. controls (16.0616,3.5688) and (14.7664,8.8740) .. (13.1278,13.5783) .. controls (11.9515,15.3829) and (8.6715,16.0161) .. (7.7941,13.7509) -- cycle;
      \\fill[lblue] (4.9884,10.6533) .. controls (7.4488,14.0291) and (12.6964,7.7969) .. (12.6964,7.7969) .. controls (13.4861,7.8582) and (13.1708,10.7423) .. (12.8259,11.2053) .. controls (10.9927,13.8335) and (9.2448,13.7940) .. (9.2448,13.7940) .. controls (6.4433,14.0475) and (4.8380,11.8428) .. (4.9884,10.6533) -- cycle;
    \\end{scope}
    \\fill[gray!80!white] (1.24,1.35) circle[radius=0.06];
    \\fill[white] (1.225,1.365) ellipse[x radius=0.015, y radius=0.03,rotate=-30];
  \\end{tikzpicture}
}
'''

def queen_uk_colours():
    return '''\\definecolor{qskin}{RGB}{225,219,206}
\\definecolor{qbill}{RGB}{170,123,154}
\\definecolor{qdress}{RGB}{184,209,206}
\\definecolor{qcrown}{RGB}{90,76,183}
'''

def queen_uk():
    return '''\\newcommand{\\queenuk}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\duck[
      body=qskin,
      bill=qbill,
      jacket=qdress,
      tshirt=teal!30!qdress,
      shorthair=gray!60!white,
      necklace=gray!10!white,
      handbag=teal!30!qdress
    ]
    \\fill[gray!60!white,rotate=-30] (0.27,1.23) rectangle (0.37,0.65);
    \\fill[qcrown,scale=0.23,rotate=-20,yshift=82,xshift=38] \\duckpathqueencrown;
    \\fill[qcrown,yshift=3] \\duckpathkingcrown;
  \\end{tikzpicture}
}
'''

def snowman():
    return '''\\newcommand{\\snowman}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\duck[
      snowduck=white
    ]
  \\end{tikzpicture}
}
'''

def overleaf():
    return '''\\newcommand{\\overleaf}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\duck[overleaf]
  \\end{tikzpicture}
}
'''

def ceasar():
    return '''\\newcommand{\\ceasar}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\fill[green!50!brown!80!black, rotate around={-15:(0.47,1.88)}] (0.47,1.88) ellipse (0.055 and 0.023);
    \\fill[green!50!brown!80!black, rotate around={15:(0.47,1.83)}] (0.47,1.83) ellipse (0.055 and 0.023);
    \\duck[jacket=red!30!gray]
    \\begin{pgfinterruptboundingbox}
      \\filldraw[gray!10!white] (0.460,1.140) .. controls (0.267, 1.102) and (-0.125,0.657) .. (0.289,0.261) .. controls (0.704,-0.135) and ( 2.863,0.130) .. (1.818,1.419) .. controls (0.980, 1.000) and ( 1.240,1.378) .. (0.46,0.55) -- cycle;
    \\end{pgfinterruptboundingbox}
    \\draw (1.29,1.82) -- (1.19,1.77) -- (1.1,1.74) -- (1,1.74);
    \\fill[green!50!brown!80!black, rotate around={15:(1,1.72)}] (1,1.72) ellipse (0.055 and 0.023);
    \\fill[green!50!brown!80!black, rotate around={18:(1.1,1.716)}] (1.1,1.716) ellipse (0.055 and 0.023);
    \\fill[green!50!brown!80!black, rotate around={45:(1.2,1.75)}] (1.2,1.75) ellipse (0.055 and 0.023);
    \\fill[green!50!brown!80!black, rotate around={70:(1.3,1.8)}] (1.3,1.8) ellipse (0.055 and 0.023);
    \\fill[green!50!brown!80!black, rotate around={-25:(1,1.76)}] (1,1.76) ellipse (0.055 and 0.023);
    \\fill[green!50!brown!80!black, rotate around={-25:(1.1,1.76)}] (1.1,1.76) ellipse (0.055 and 0.023);
    \\fill[green!50!brown!80!black, rotate around={-20:(1.19,1.79)}] (1.19,1.79) ellipse (0.055 and 0.023);
    \\fill[green!50!brown!80!black, rotate around={10:(1.27,1.84)}] (1.27,1.84) ellipse (0.055 and 0.023);
  \\end{tikzpicture}
}
'''

def ghost_colours():
    return """\colorlet{ghost}{white!98!gray}
"""

def ghost():
    return '''\\newcommand{\\ghost}[1]{
  \\begin{tikzpicture}[scale=#1]
    \\duck[
      body=ghost,
      bill=ghost,
      prison=gray
    ]
    \\fill[ghost,rotate=-17](-0.1,0.7) rectangle (0.15,1.3);
    \\fill[ghost,rotate=17] (1.6,0.7) rectangle (1.81,1.3);
  \\end{tikzpicture}
}
'''

def chess_colours():
    return '''\\colorlet{dark}{black!75!white}
\\colorlet{light}{yellow!70!brown!50!white}
\\colorlet{accent}{orange!50!brown}
\\colorlet{cutline}{green}
'''

def bauer():
    return '''\\newcommand{\\bauer}[2]{%
  \\begin{tikzpicture}[scale=#1*0.75]
    \\duck[body=#2,bill=accent]
  \\end{tikzpicture}
}
'''

def turm():
    return '''\\newcommand{\\turm}[2]{%
  \\begin{tikzpicture}[scale=#1]
    \\begin{scope}[scale=0.38]
      \duck[body=#2,bill=accent]
    \\end{scope}
    \\path[fill=gray,yshift=-45,xshift=-8] (0.0959,0.1866) .. controls (0.0908,0.2574) and (0.0900,0.3748) .. (0.1928,0.3609) .. controls (0.2295,0.3527) and (0.2359,0.3750) .. (0.2326,0.4070) .. controls (0.2337,0.4816) and (0.2438,0.5571) .. (0.2849,0.6214) .. controls (0.3553,0.7835) and (0.3522,0.9650) .. (0.3641,1.1382) .. controls (0.3678,1.2187) and (0.3676,1.2993) .. (0.3675,1.3799) .. controls (0.3183,1.3832) and (0.2443,1.3768) .. (0.2356,1.4412) .. controls (0.2297,1.6004) and (0.2294,1.7604) .. (0.2367,1.9196) .. controls (0.2988,1.9217) and (0.3843,1.9393) .. (0.4339,1.9106) .. controls (0.4300,1.8436) and (0.4255,1.7539) .. (0.5208,1.7857) .. controls (0.5477,1.7857) and (0.5820,1.7785) .. (0.5698,1.8176) .. controls (0.5717,1.8659) and (0.5553,1.9453) .. (0.6308,1.9238) .. controls (0.7009,1.9243) and (0.7710,1.9230) .. (0.8411,1.9226) .. controls (0.8425,1.8787) and (0.8439,1.8348) .. (0.8453,1.7909) .. controls (0.8892,1.7909) and (0.9331,1.7909) .. (0.9770,1.7909) .. controls (0.9784,1.8348) and (0.9798,1.8787) .. (0.9812,1.9226) .. controls (1.0478,1.9226) and (1.1143,1.9226) .. (1.1809,1.9226) .. controls (1.1794,1.7563) and (1.1845,1.5897) .. (1.1771,1.4236) .. controls (1.1574,1.3706) and (1.0943,1.3835) .. (1.0492,1.3790) .. controls (1.0532,1.1475) and (1.0506,0.9124) .. (1.1071,0.6864) .. controls (1.1310,0.6073) and (1.1880,0.5375) .. (1.1819,0.4508) .. controls (1.1864,0.4236) and (1.1780,0.3839) .. (1.1895,0.3637) .. controls (1.2346,0.3602) and (1.3001,0.3702) .. (1.3145,0.3141) .. controls (1.3197,0.2396) and (1.3177,0.1647) .. (1.3193,0.0900) .. controls (0.9114,0.0900) and (0.5036,0.0900) .. (0.0957,0.0900) .. controls (0.0958,0.1222) and (0.0959,0.1544) .. (0.0959,0.1866) -- cycle;
  \\end{tikzpicture}
}
'''

def springer():
    return '''\\newcommand{\\springer}[2]{%
  \\begin{tikzpicture}[scale=#1]
    \\begin{pgfinterruptboundingbox}
      \\begin{scope}[yshift=-6]
        \\clip[rotate=-5] (0.68,2.38) ellipse (0.3 and 0.4);
        \\fill[#2,rotate=-5](0.28,2.26)ellipse (0.3 and 0.4);
      \\end{scope}
    \\end{pgfinterruptboundingbox}
    \\duck[body=#2,bill=accent,horsetail,mohican=accent]
    \\begin{pgfinterruptboundingbox}
      \\begin{scope}[yshift=-5,xshift=1]
        \\clip[rotate=-5] (0.68,2.38) ellipse (0.3 and 0.4);
        \\fill[#2,rotate=-5](1.06,2.2) ellipse (0.3 and 0.4);
      \\end{scope}
    \\end{pgfinterruptboundingbox}
  \\end{tikzpicture}
}
'''

def laeufer():
    return '''\\newcommand{\\laeufer}[2]{%
  \\begin{tikzpicture}[scale=#1]
    \\duck[body=#2,bill=accent,crozier=accent]
    % mita
    \\path[fill=accent] (0.5101,1.8761) .. controls (0.6355,2.4588) and (0.9681,2.6303) .. (0.9681,2.6303) -- (1.0260,2.4101) -- (1.1548,2.6202) .. controls (1.1548,2.6202) and (1.4167,2.2951) .. (1.3398,1.8247) .. controls (1.0829,1.7440) and (0.6286,1.8104) .. (0.5101,1.8761) -- cycle;
  \\end{tikzpicture}
}
'''

def dame():
    return '''\\newcommand{\\dame}[2]{%
  \\begin{tikzpicture}[scale=#1]
    \\duck[body=#2,necklace=gray,longhair=accent,bill=accent]
    \\begin{scope}[yshift=2]
      \\fill[#2] \duckpathqueencrown;
    \\end{scope}
  \\end{tikzpicture}
}
'''

def koenig():
    return '''\\newcommand{\\koenig}[2]{%
  \\begin{tikzpicture}[scale=#1]
    \\duck[body=#2,shorthair=accent,bill=accent]
    \\begin{scope}[yshift=4]
      \\fill[#2] \\duckpathkingcrown;
    \\end{scope}
  \\end{tikzpicture}
}
'''

def yoda_colours():
    return """\\colorlet{yodaskin}{white!45!gray!80!green}
"""

def yoda():
    return '''\\newcommand{\\yoda}[1]{%
  \\begin{tikzpicture}[scale=#1]
    \\duck[lightsaber, body=yodaskin, bill=gray!80!green, tshirt=brown!50!black, jacket=brown!30!gray]
    \\fill[yodaskin,rounded corners=3] (0.44,1.70) -- (0.25,2) -- (0.6,1.95);
    \\fill[yodaskin,rounded corners=3] (1.34,1.60) -- (1.53,1.9) -- (1.16,1.85);
  \\end{tikzpicture}
}%
'''

def vader():
    return '''\\newcommand{\\vader}[1]{%
  \\begin{tikzpicture}[scale=#1]
    \\duck[grumpy, lightsaber=red, cape=black!85!white, body=black!70!white, darthvader=black!85!white]
  \\end{tikzpicture}
}
'''

def leila():
    return '''\\newcommand{\\leila}[1]{%
  \\begin{tikzpicture}[scale=#1]
    \\fill[brown!70!black] (0.5,1.65) circle (0.25);
    \\duck[jacket=white!95!brown, body=brown!50!white, shorthair=brown!70!black, lightsaber=cyan]
    \\fill[brown!70!black] (1.3,1.6) circle (0.25);
  \\end{tikzpicture}
}
'''
