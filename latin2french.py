# -*- coding: utf-8 -*-

import re
import math

class Word:
  def __init__(self, word, language):
    self.__language = language
    self.__word = word
    
  def get_language(self):
    return self.__language
  
  def get_word(self):
    return self.__word
  
  def print(self):
    return self.get_word()+" ("+self.__language+")"
  
  def transform(self, target_language, accept_all=True):
    word = self.get_word()
    print("Starting from "+word)
    # conn = sqlite3.connect('ma_base.db')
    # cursor = conn.cursor()
    # command = """ SELECT * FROM rules WHERE language_from = ? AND language_to = ? """
    # cursor.execute(command, (self.get_language(), target_language))
    # rules = cursor.fetchall()
    # conn.close()
    #protected = [False] * len(word)
    for i in range(len(rules)):
        for case in re.finditer(rules[i][0], word):
          if not accept_all:
            txt = input("Use the rule " + rules[i][2] + " y/n")
            print("rule "+ rules[i][2] +" activated")
            if txt == "n":
              continue
          #if True in protected[case.start():case.end()]:
           # continue
          word = re.sub(rules[i][0], rules[i][1], word)
         # protected = protected[0:case.start()]+[True]*len(rules[i][1])+protected[case.end():len(protected)]
          print("rule n°"+str(i) +" : at "+ str(rules[i][3]) +" "+ rules[i][2] + " => " + word)
    return Word(word = word, language = target_language)

classic_latin_vowels="\u0101\u0103\u014d\u014f\u0113\u0115\u012d\u012b\u016D\u016B"
consonants="pbtdkgmnfvszljr\u03b4" # to continue
vowels="aeoui\u025b\u0254\u0259"+classic_latin_vowels

rules=[
  ## passage en phonétique du Latin
   ["c", "k",	"Latin phonetic c>k",	-math.inf],
   ["v", "w",	"Latin phonetic v>w",	-math.inf],
   ["qu", "k\u02b7",	"Latin phonetic qu>k\u02b7",	-math.inf],
   ["gu", "g\u02b7",	"Latin phonetic gu>g\u02b7",	-math.inf],
   ["^h","","intial h> zero", 0],
  # vulgar Latin vowels   -- > au -> o p18
  # 2.2.1
   ["oe", "e",	"oe>e",	0],
   ["ae",	"\u025b",	"ae>\u025b",	100],
   ["au",	"\u0254",	"au>\u0254",	490],
   ["\u0113",	"e",  "\u0113>e",	100],
   ["\u0115",	"\u025b",	"\u0115>\u025b",	100],
   ["\u014d",	"o",	"\u014d>o",	100],
   ["\u014f",	"\u0254",	"\u014f>\u0254",	100],
   ["\u012d",	"e",	"\u012d>e",	200], 
   ["\u016D\\B",	"o",	"internal \u016D>o",	300],
   ["\u016D\\b",	"o",	"final \u016D>o",	400],
   ["\u012b",	"i",	"\u012b>i",	200],
   ["\u0101",	"a",	"\u0101>a",	200],
   ["\u0103",	"a",	"\u0103>a",	200],
   ["\u016B",	"u",	"\u016B>u",	200],
  # unaccented short vowels in hiatus  
  # 2.2.3
   ["[\u012d\u0115](?=["+classic_latin_vowels+"])",	"j",	"unaccentuated and hiatus \u012d and \u0115>j",	-100],
   ["\u016D(?=["+classic_latin_vowels+"])",	"w",	"unaccentuated and hiatus \u016D>w",	-100],
  # prophetic vowel
  #2.2.4
   ["(?=^s[ptkmn])",	"\u012d",	"prophetic vowel \u012d before s+occlusive",	100],
  # accentuated vowels in closed syllable
  #4.1
   ["\u0254\u0301(?=s["+consonants+"])",	"o\u0301",	"accentuated \u0254 before s+consonant> o",	1100],
   ["o\u0301(?=[rs]["+consonants+"])",	"u\u0301",	"accentuated o in closed syllable> u",	1100],
   ["\u0254\u0301(?=[sz]["+consonants+"]?)",	"u\u0301",	"accentuated \u0254 before s,z> u",	1100],
   ## miss one open o before e p25
  # roman diphtongaison
  #4.3.1
   ["\u025b\u0301(?=["+consonants+"]?r?["+vowels+"]|$)",	"i\u0301\u025b",	"accentuated \u025b open syllable> i\u0301\u025b",	300],
   ["i\u0301\u025b(?=["+consonants+"]?r?["+vowels+"]|$)",	"i\u0301e",	"open syllable i\u0301\u025b>i\u0301e",	600],
   ["i\u0301e(?=["+consonants+"]?r?["+vowels+"]|$)",	"je\u0301",	"open syllable i\u0301e>je\u0301",	1200],
   ["e(?=["+consonants+"])", "\u025b",	"position law e>\u025b before consonant",	1600],
   #4.3.2
   ["\u0254\u0301(?=["+consonants+"]?r?["+vowels+"]|$)",	"u\u0301\u0254",	"accentuated \u0254 open syllable> u\u0301\u0254",	300],
   ["u\u0301\u0254(?=["+consonants+"]?r?["+vowels+"]|$)",	"u\u0301o",	"open syllable u\u0301\u0254>u\u0301o",	600],
   ["u\u0301o(?=["+consonants+"]?r?["+vowels+"]|$)",	"u\u0301e",	"open syllable u\u0301o>u\u0301e",	1100],
   ["u\u0301e(?=["+consonants+"]?r?["+vowels+"]|$)",	"y\u0301\u00f8",	"open syllable u\u0301e>y\u0301\u00f8",	1150],
   ["y\u0301\u00f8(?=["+consonants+"]?r?["+vowels+"]|$)",	"\u00f8\u0301",	"open syllable y\u0301\u00f8>\u00f8\u0301",	1200],
   ["\u00f8(?=["+consonants+"])", "\u0153",	"position law \u00f8>\u0153 before consonant",	1600],
  # French diphtongaison
  #4.4.1
   ["e\u0301(?=["+consonants+"]?r?["+vowels+"]|$)",	"e\u0301i\u032f",	"open syllable e\u0301>e\u0301i\u032f",	500],
   ["e\u0301i\u032f(?=["+consonants+"]?r?["+vowels+"]|$)",	"\u0254\u0301i\u032f",	"open syllable e\u0301i\u032f>\u0254\u0301i\u032f",	1100],
   ["\u0254\u0301i\u032f(?=["+consonants+"]?r?["+vowels+"]|$)",	"u\u0301e",	"open syllable \u0254\u0301i\u032f>u\u0301e",	1150],
   ["u\u0301e(?=["+consonants+"]?r?["+vowels+"]|$)",	"we\u0301",	"open syllable u\u0301e>we\u0301",	1200],
   ["we\u0301(?=["+consonants+"]?r?["+vowels+"]|$)",	"wa\u0301",	"open syllable we\u0301>wa\u0301",	1250],
   #4.4.2
   ["o\u0301(?=["+consonants+"]?r?["+vowels+"]|$)",	"o\u0301u\u032f",	"open syllable o\u0301>o\u0301u\u032f",	500],
   ["o\u0301u\u032f(?=["+consonants+"]?r?["+vowels+"]|$)",	"e\u0301u\u032f",	"open syllable o\u0301u\u032f>e\u0301u\u032f",	1050],
   ["e\u0301u\u032f(?=["+consonants+"]?r?["+vowels+"]|$)",	"\u00f8\u0301u\u032f",	"open syllable e\u0301u\u032f>\u00f8\u0301u\u032f",	1100],
   ["\u00f8\u0301u\u032f(?=["+consonants+"]?r?["+vowels+"]|$)",	"\u00f8\u0301",	"open syllable \u00f8\u0301u\u032f>\u00f8\u0301",	1200],
   # 4.5
   ["a\u0301(?=["+consonants+"]?r?["+vowels+"]|$)",	"a\u0301\u025b\u032f",	"open syllable a\u0301>a\u0301\u025b\u032f",	500],
   ["a\u0301\u025b\u032f(?=["+consonants+"]?r?["+vowels+"]|$)",	"\u025b\u0301",	"open syllable a\u0301\u025b\u032f>\u025b\u0301",	600],
   ["\u025b\u0301(?=["+consonants+"]?r?["+vowels+"]|$)",	"e\u0301",	"open syllable \u025b\u0301>e\u0301",	1000],
   ["e(?=["+consonants+"])", "\u025b",	"position law e>\u025b before consonant",	1700],
   # 5.2.1
   ["\u025b\u0301(?=j["+consonants+"])",	"i\u0301\u025b\u032f",	"\u025b\u0301+j closed syllable> i\u0301\u025b\u032f",	350],
   ["i\u0301\u025b\u032f(?=j["+consonants+"])",	"i\u0301e\u032f",	"i\u0301\u025b\u032f+j closed syllable>i\u0301e\u032f",	600],
   ["i\u0301e\u032fj(?=["+consonants+"])",	"i\u0301",	"i\u0301e\u032fj closed syllable>i\u0301",	800],
   ["\u0254\u0301(?=j["+consonants+"])",	"u\u0301\u0254\u032f",	"\u0254\u0301+j closed syllable> u\u0301\u0254\u032f",	350],
   ["u\u0301\u0254\u032f(?=j["+consonants+"])",	"u\u0301o\u032f",	"u\u0301\u0254\u032f+j closed syllable>u\u0301o\u032f",	600],
   ["u\u0301o\u032fj(?=["+consonants+"])",	"y\u0301i\u032f",	"u\u0301o\u032fj closed syllable>y\u0301i\u032f",	800],
   ["y\u0301i\u032f(?=["+consonants+"])",	"\u0265i\u0301",	"y\u0301i\u032f>\u0265i\u0301",	1200],
   # 5.2.2  l palatal ?
   # 5.3
   # 6.1.1  to continue
   #["a(?<=[kg])\u0301(?=["+consonants+"]["+vowels+"])", "e\u0301", "a\u0301 open syllable after k,g> e\u0301", ],
    # 7.1.1
   ["(^k)a(?=["+consonants+"]r?["+vowels+"])", "\\1e", "inital palatal+unaccentuated a open syllable > e", 500],
   ["(^k)e(?=["+consonants+"]r?["+vowels+"])", "\\1\u0259", "inital palatal+unaccentuatede open syllable > \u0259", 1000], 
   ["(^["+consonants+"])a(?=["+vowels+"])", "\\1\u0259", "a in hiatus initial unaccentuated syllable>\u0259", 1000],
   ["(^["+consonants+"])\u0259(?=["+vowels+"])", "\\1", "\u0259 in hiatus initial unaccentuated syllable>zero", 1300],
   # 7.1.2
   ["(^["+consonants+"])\u025b(?!\u0301)", "\\1e", "\u025b>e initial unaccentuated syllable", 300],
   ["(^["+consonants+"])\u0254(?!\u0301)", "\\1o", "\u0254>e initial unaccentuated syllable", 300],
   ["(^["+consonants+"])\u0254(?!\u0301)", "\\1o", "\u0254>e initial unaccentuated syllable", 500],
   # 7.2
   ["(\u0301["+consonants+"]+["+vowels+"]["+consonants+"]+)[eou\u025b\u0254]$","\\1\u0259", "final vowel other than a >\u0259 in proparoxyton", 200],
   ["(["+consonants+"][lrmn])[eou\u025b\u0254]$","\\1\u0259", "final vowel other than a >\u0259 after consonant+l,r,m,n", 200],
   ["([bp]j)[eou\u025b\u0254]$","\\1\u0259", "final vowel other than a >\u0259 after b, p+j", 200],
   ["([bp]j)[eou\u025b\u0254]$","\\1\u0259", "final vowel other than a >\u0259 after b, p+j", 200],
   ["(jr)[eou\u025b\u0254]$","\\1\u0259", "final vowel other than a >\u0259 after jr", 200],
   ["a$","\u0259", "final a>\u0259", 600],
   ["[eou\u025b\u0254]$","", "final vowel other than a>zero", 600],
   ["\u0259$","\u0153", "final \u0259>\u0153", 1400],
   ["\u0153$","", "final \u0153>zero", 1600],
   # 7.3
   ["(["+vowels+"]["+consonants+"]+)a(?=["+consonants+"]r?["+vowels+"]\u0301)","\\1\u0259", "internal a before accentuated syllable>\u0259", 500],
   ["(["+vowels+"][rns]?["+consonants+"]+)[eou\u025b\u0254](?=["+consonants+"]r?["+vowels+"]\u0301)","(\\1)", "internal vowels other than a before accentuated syllable>zero", 500],
   ["(["+vowels+"][rns]?["+consonants+"]r+)[eou\u025b\u0254](?=["+consonants+"]r?["+vowels+"]\u0301)","(\\1)\u0259", "internal vowels other than a before accentuated syllable and after 2 consonants>\u0259", 500],
   # 7.4
   ["(?<=k)\u016D(?=l[\u016D\u016B]$)", "", "ending in -k\u016Dlu > -klu", 190],
   ["(?<=[lr])["+classic_latin_vowels+"](?=["+consonants+"]["+vowels+"]$)", "", "l,r + unaccentuated penultieme vowel > zero", 190],
   ["(?<=[ns])["+classic_latin_vowels+"](?=[td]["+vowels+"]$)", "", "n,s + unaccentuated penultieme vowel + t,d > zero", 190],
   ["(?<=[ns])["+classic_latin_vowels+"](?=[td]["+vowels+"]$)", "", "n,s + unaccentuated penultieme vowel + t,d > zero", 190],
   ["(["+vowels+"]\u0301["+consonants+"]+)[\u025b\u0254](?=["+consonants+"]+["+vowels+"])", "\\1", "unaccentuated penultieme vowel \u025b, \u0254 > zero", 249],
   ["(["+vowels+"]\u0301["+consonants+"]+)["+vowels+"](?=["+consonants+"]+["+vowels+"])", "\\1", "unaccentuated penultieme vowel > zero", 400],

   #8.1.1
   ["a(?=[nm])",	"a\u0303",	"a+n,m > a\u0303",	1000],
   ["a\u0303(?=[nm]["+vowels+"])", "a",	"open syllable a\u0303 > a", 1600],
   #8.1.2
   ["e(?=[nm])",	"e\u0303",	"e+n,m > e\u0303",	1000],
   ["e\u0303",	"a\u0303",	"e\u0303 > a\u0303",	1050],
   #8.1.3
   ["o(?=[nm])",	"o\u0303",	"o+n,m > o\u0303",	1150],
   ["o\u0303",	"\u0254\u0303",	"o\u0303 > \u0254\u0303",	1200],
   #8.1.4
   ["i(?=[nm](?!["+vowels+"]))",	"i\u0303",	"i+n,m closed syllable> i\u0303",	1200],
   ["i\u0303",	"e\u0303",	"i\u0303 > e\u0303",	1300],
   ["y(?=[nm](?!["+vowels+"]))",	"y\u0303",	"y+n,m closed syllable> y\u0303",	1200],
   ["y\u0303",	"\u0153\u0303",	"y\u0303 > \u0153\u0303",	1300],
   # 8.2...
   # 9.1.1
   # 10.1
   ["(.*["+classic_latin_vowels+"].*["+ classic_latin_vowels+"])m$","\\1","final m> zero except monosyllabic", -100],
   ["m$", "n", "final m>n in monosyllabic", 900],
   # 10.2
   ["(["+vowels+"]\u0301?\u032f?)[t\u03b8]$","\\1","final t or \u03b8 after vowel>zero",800],
   ["(["+consonants+"])t$","\\1","final t after consonant>zero",1150],
   # 10.3
   ["s$","","final s>zero",1150],
   # 10.4
   ["b$","p","final b>p", 650],
   ["d$","t","final d>t", 650],
   ["g$","k","final g>k", 650],
   ["\u03b4$","\u03b8","final \u03b4>\u03b8", 650],
   ["v$","f","final v>f", 650],
   ["z$","s","final z>s", 650],
   # 10.5
   ["(.*"+vowels+".*"+ vowels+")["+re.sub("r","",consonants)+"]$","","final consonant other than r>zero except monosyllabic",1190],
   ["(.*"+vowels+".*"+ vowels+")r$","","final r>zero except monosyllabic",1300],
   #11.1
   ["(["+vowels+"]\u0301?\u032f?)p(?=["+vowels+"])", "\\1b",	"intervocalic p>b",	390],
   ["(["+vowels+"]\u0301?\u032f?)b(?=["+vowels+"])", "\\1\u03b2",	"intervocalic b>\u03b2",	400],
   ["(["+vowels+"]\u0301?\u032f?)\u03b2(?=["+vowels+"])", "\\1v",	"intervocalic \u03b2>v",	450],
   ["(["+vowels+"]\u0301?\u032f?)[bw](?=["+vowels+"])", "\\1\u03b2",	"intervocalic b, w>\u03b2",	0],
   ["([aie\u025b]\u0301?\u032f?)\u03b2(?=["+vowels+"])", "\\1v",	"intervocalic \u03b2>v",	200],
   ["([uo\u0254]\u0301?\u032f?)\u03b2(?=["+vowels+"])", "\\1",	"intervocalic \u03b2>zero",	200],
   ["(["+vowels+"]\u0301?\u032f?)pr(?=["+vowels+"])", "\\1br",	"intervocalic pr>br",	350],
   ["(["+vowels+"]\u0301?\u032f?)br(?=["+vowels+"])", "\\1\u03b2r",	"intervocalic br>\u03b2r",	0],
   ["(["+vowels+"]\u0301?\u032f?)br(?=["+vowels+"])", "\\1\u03b2r",	"intervocalic br>\u03b2r",	400],
   ["(["+vowels+"]\u0301?\u032f?)\u03b2r(?=["+vowels+"])", "\\1vr",	"intervocalic \u03b2r>vr",	200],
   ["(["+vowels+"]\u0301?\u032f?)\u03b2r(?=["+vowels+"])", "\\1vr",	"intervocalic \u03b2r>vr",	401],
   #11.2
   ["(["+vowels+"]\u0301?\u032f?)t(?=["+vowels+"])", "\\1d",	"intervocalic t>d",	390],
   ["(["+vowels+"]\u0301?\u032f?)d(?=["+vowels+"])", "\\1\u03b4",	"intervocalic d>\u03b4",	500],
   ["(["+vowels+"]\u0301?\u032f?)\u03b4(?=["+vowels+"])", "\\1",	"intervocalic \u03b4>zero",	800],
   ["(["+vowels+"]\u0301?\u032f?)tr(?=["+vowels+"])", "\\1dr",	"intervocalic tr>dr",	350],
   ["(["+vowels+"]\u0301?\u032f?)dr(?=["+vowels+"])", "\\1\u03b4r",	"intervocalic dr>\u03b4r",	500],
   ["(["+vowels+"]\u0301?\u032f?)\u03b4r(?=["+vowels+"])", "\\1r",	"intervocalic \u03b4r>r",	800],
   #11.3
   ["(["+vowels+"]\u0301?\u032f?)s(?=["+vowels+"])", "\\1z",	"intervocalic s>z",	390],
   #11.4
   ["(["+vowels+"]\u0301?\u032f?)k(?=["+vowels+"])", "\\1g",	"intervocalic k>g",	350],
   ["(["+vowels+"]\u0301?\u032f?)g(?=["+vowels+"])", "\\1\u03b3",	"intervocalic g>\u03b3",	300],
   ["(["+vowels+"]\u0301?\u032f?)g(?=["+vowels+"])", "\\1\u03b3",	"intervocalic g>\u03b3",	400],
   ["(["+vowels+"]\u0301?\u032f?)\u03b3(?=[ou\u0254])", "\\1",	"intervocalic \u03b3>zero before o,u",	450],
   ["([ei\u025b]\u0301?\u032f?)\u03b3(?=a)", "\\1j",	"intervocalic \u03b3>j before a and after e, i",	450],
   ["([ou\u0254]\u0301?\u032f?)\u03b3(?=a)", "\\1",	"intervocalic \u03b3>zero before a and after o, u",	450],
   #12.1
   ["w",	"\u03b2",	"w>\u03b2",	0],
   ["\u03b2",	"v",	"\u03b2>v",	200],
   #12.2
   ["w",	"gw",	"w>gw (germanic w)",	400],
   ["gw", "g",	"gw>g (germanic gw)",	1000],
   #12.3
   ["(["+consonants+"]|^)k\?u02b7", "\\1k",	"k\u02b7>k initial or after consonant",	1000],
   ["(["+consonants+"])g\u02b7", "\\1g",	"g\u02b7>g after consonant",	1000],
    #13.1
   ["n(?=sf])",	"",	"disparition of n before s, f",	0],
   #13.2
   ["s(?=[ptkf])",	"",	"disparition of s before mute consonants",	1150],
   ["z(?=[bdgvmln])",	"",	"disparition of z before sonore consonants",	1050],
   #13.3
   ["l(?=["+consonants+"])","l\u02e0","l>l\u02e0 before consonant",200],
   ["l(?=["+consonants+"])","l\u02e0","l>l\u02e0 before consonant",400],
   ["l(?=["+consonants+"])","l\u02e0","l>l\u02e0 before consonant",700],
   ["l\u02e0(?=["+consonants+"])","u\u032f","l\u02e0>u\u032f before consonant",1000],
   #13.4.1
   ["ts$","s","ts>s final",1200],
   ["[d\u03b4]s$","ts","d, \u03b4 before s final>t",600],
   #13.5
   ["[pv](?=[st])","f","p, v before s, t >f", 600],
   ["f(=[st])","","f before s, t >zero", 800],
   ["m(?=[st])","n","m before s, t >n", 600],
   # 14 geminees
   ["(\u0101\u014d\u0113\u012b\u016B)ll", "\\1l", "simplification of double ll after long vowels", 300],
   ["(["+consonants+"])\\1", "\\1", "simplification of double consonants", 600],
   ["(["+vowels+"])j(?=["+vowels+"])", "\\1i\u032f", "diphtongaison of intervocalic j", 800],

  # 15. consonnes épenthétiques
  # 15.1
   ["m(?=[rl])",	"mb",	"m+r,l > mbr or mbl",	300],
   ["n(?=r)",	"nd",	"n+r > ndr",	300],
  #15.2 
   ["s(?=r)",	"st",	"s+r > str",	300],
   ["z(?=r)",	"zd",	"z+r > zdr",	300],
   ["l(?=r)",	"ld",	"l+r > ldr",	300],
  # 16.2.1
   ["k(?=j)",	"k\u032c",	"k+j > k\u032c",	100],
   ["k\u032c",	"t\u032c",	"k\u032c > t\u032c",	110],
   ["t\u032c",	"ts\u032c",	"t\u032c > ts\u032c",	120],
   ["ts\u032c",	"ts",	"ts\u032c > ts",	600],
   ["ts",	"s",	"ts > s",	1200],
   ["("+consonants+")tj",	"\\1t\u032c",	"t+j > t\u032c after consonants",	100],
   ["("+consonants+")k\u032c",	"\\1t\u032c",	"k\u032c > t\u032c after consonants",	110],
   ["("+consonants+")t\u032c",	"\\1ts\u032c",	"t\u032c > ts\u032c after consonants",	120],
   ["("+consonants+")ts\u032c",	"\\1ts",	"ts\u032c > ts after consonants",	600],
   ["("+consonants+")ts",	"\\1s",	"ts > s after consonants",	1200],
   ["("+vowels+")tj(?="+vowels+")",	"\\1jt\u032c",	"intervocalic t+j >jt\u032c",	100],
   ["("+vowels+")jt\u032c(?="+vowels+")",	"\\1jts\u032c",	"intervocalic jt\u032c >jts\u032c",	110],
   ["("+vowels+")jts\u032c(?="+vowels+")",	"\\1jdz\u032c",	"intervocalic jts\u032c >jdz\u032c",	350],
   ["("+vowels+")jdz\u032c(?="+vowels+")",	"\\1i\u032cdz",	"intervocalic jdz\u032c >i\u032cdz",	600],
   ["("+vowels+")i\u032cdz(?="+vowels+")",	"\\1i\u032cz",	"intervocalic i\u032cdz >i\u032cz",	1200],
   # 16.2.2
   ["(["+consonants+"]?)k(?=[ei\u025b\u012d\u012b\u0113\u0115])", "\\1k\u032c",	"k+e,i>k\u032c initial or after consonant",	200],
   ["(["+consonants+"]?)k\u032c(?=[ei\u025b\u012d\u012b\u0113\u0115])",	"\\1t\u032c",	"k\u032c+e,i > t\u032c initial or after consonant",	210],
   ["(["+consonants+"]?)t\u032c(?=[ei\u025b\u012d\u012b\u0113\u0115])",	"\\1ts\u032c",	"t\u032c+e,i > ts\u032c initial or after consonant",	220],
   ["("+vowels+")k(?=[ei\u025b\u012d\u012b\u0113\u0115])",	"\\1k\u032c",	"intervocalic k+e,i >k\u032c",	200],
   ["("+vowels+")k\u032c(?=[ei\u025b\u012d\u012b\u0113\u0115])",	"\\1jt\u032c",	"intervocalic k\u032c+e,i >jt\u032c",	210],
   ["("+vowels+")jt\u032c(?=[ei\u025b\u012d\u012b\u0113\u0115])",	"\\1jts\u032c",	"intervocalic jt\u032c+e,i >jts\u032c",	220],
   ["(["+consonants+"]?)g(?=[ei\u025b\u012d\u012b\u0113\u0115])", "\\1g\u032c",	"g+e,i>g\u032c initial or after consonant",	200],
   ["(["+consonants+"]?)g\u032c(?=[ei\u025b\u012d\u012b\u0113\u0115])",	"\\1d\u032c",	"g\u032c+e,i > d\u032c initial or after consonant",	210],
   ["(["+consonants+"]?)d\u032c(?=[ei\u025b\u012d\u012b\u0113\u0115])",	"\\1d\u0292\u032c",	"d\u032c+e,i > d\u0292\u032c initial or after consonant",	220],
   ["d\u0292\u032c",	"d\u0292",	"d\u0292\u032c > d\u0292",	600],
   ["d\u0292",	"\u0292",	"d\u0292 > \u0292",	1200],
   ["(["+consonants+"]?)k(?=a)", "\\1k\u032c",	"k+a>k\u032c initial or after consonant",	400],
   ["(["+consonants+"]?)k\u032c(?=a)",	"\\1t\u032c",	"k\u032c+a > t\u032c initial or after consonant",	410],
   ["(["+consonants+"]?)t\u032c(?=a)",	"\\1t\u0283\u032c",	"t\u032c+a > t\u0283\u032c initial or after consonant",	420],
   ["t\u0283\u032c",	"t\u0283",	"t\u0283\u032c > t\u0283",	600],
   ["t\u0283",	"\u0283",	"t\u0283 > \u0283",	1200],
   ["(["+consonants+"]?)g(?=a)", "\\1g\u032c",	"g+a>g\u032c initial or after consonant",	400],
   ["(["+consonants+"]?)g\u032c(?=a)",	"\\1d\u032c",	"g\u032c+a > d\u032c initial or after consonant",	410],
   ["(["+consonants+"]?)d\u032c(?=a)",	"\\1d\u0292\u032c",	"d\u032c+a > d\u0292\u032c initial or after consonant",	420]

   # 16.2.3
   
   ]


rules = sorted(rules, key=lambda rules: rules[3])

