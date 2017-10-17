# encoding: utf-8

tests = [
# ~C V~
["tat", "eva", "tad eva"],

# ~V C~
["samyak", "asti", "samyag asti"],

# ~V V~
["rAmasya", "CAtraH", "rAmasya cCAtraH"], # does not work because no rule found in the tables

# homorganic vowels
["mA", "astu", "mAstu"],
["gacCati", "iti", "gacCatIti"],
["guru", "upeti", "gurUpeti"],

# guṇation
["na", "iti", "neti"],
["rAmeRa", "uktaH", "rAmeRoktaH"],
["mahA", "fziH", "maharziH"],

# vṛddhization
["na", "eti", "nEti"],
["mahA", "ozaDiH", "mahOzaDiH"],
["rAmasya", "Ekyam", "rAmasyEkyam"],

# semivowels
["iti", "uvAca", "ityuvAca"],
["devI", "asti", "devyasti"],
["devI", "AgacCati", "devyAgacCati"],
["kuru", "adya", "kurvadya"],
["bahu", "iti", "bahviti"],
["maDu", "admi", "maDvadmi"],
["guru", "Asanam", "gurvAsanam"],

# guṇa vowels
["te", "api", "te 'pi"],
["te", "uvAca", "ta uvAca"],
["gfhe", "uta", "gfha uta"],

# vṛḍdhi vowels
["SriyE", "arTaH", "SriyA arTaH"],
["uBO", "uvAca", "uBAvuvAca"],

# Final: non-palatal stops
["anuzwuB", "", "anuzwup"],
["suhfd", "", "suhft"], # the space stands for an empty string, triggering the final sandhi.

# Final: palatal stops
["vAc", "", "vAk"],
["virAj",  "", "virAw"],
["diS", "", "dik"],

# Final: nasals
["pustakam", "", "pustakam"],
["karman", "", "karman"],

# Final: s and r
["tapas", "", "tapaH"],
["pitar", "", "pitaH"],

# Final: consonant clusters
["Bavant", "", "Bavan"],
["Bavantkgtrnp", "", "Bavan"],

# final dentals
["Bavat", "janma", "Bavaj janma"],
["etat", "Danam", "etad Danam"],
["Bavat", "deham", "Bavad deham"],
["tat", "Saram", "tac Caram"],

# final m
["pustakam", "paWati", "pustakaM paWati"],
["vanam", "gacCAmi", "vanaM gacCAmi"],

# final n
["mahAn", "qamaraH", "mahAR qamaraH"],
["etAn", "cCAtraH", "etAMS cCAtraH"],
["gacCan", "ca", "gacCaMS ca"],
["tAn", "tAn", "tAMs tAn"],
["asmin", "wIkA", "asmiMz wIkA"],  # etAn gacCati changed to cCatraH (n+g = n g, following table)

# before l
["tat", "lokaH", "tal lokaH"],
["tAn", "lokAn", "tAM lokAn"],

# before h
["vAk", "hi", "vAg Gi"],
["tat", "hi", "tad Di"],

# -aḥ sandhi
["rAmaH", "gacCati", "rAmo gacCati"],
["rAmaH", "asti", "rAmo 'sti"],
["rAmaH", "karoti", "rAmaH karoti"],
["rAmaH", "calati", "rAmaS calati"],
["rAmaH", "wIkAm", "rAmaz wIkAm"],
["rAmaH", "tu", "rAmas tu"],
["rAmaH", "patati", "rAmaH patati"],
["rAmaH", "uvAca", "rAma uvAca"],

# -āḥ sandhi
["devAH", "vadanti", "devA vadanti"],
["devAH", "eva", "devA eva"],
["devAH", "kurvanti", "devAH kurvanti"],
["devAH", "patanti", "devAH patanti"],
["devAH", "ca", "devAS ca"],
["devAH", "wIkA", "devAz wIkA"],
["devAH", "tu", "devAs tu"],

# -iḥ -īḥ -uḥ -ūḥ -eḥ -oḥ -aiḥ -auḥ
["muniH", "vadati", "munir vadati"],
["tEH", "uktam", "tEr uktam"],
["BUH", "Buvas", "BUr Buvas"],
["muniH", "karoti", "muniH karoti"],
["agniH", "ca", "agniS ca"],
["muneH", "wIkAm", "munez wIkAm"],
["tEH", "tu", "tEs tu"],
["guruH", "patati", "guruH patati"],

# Exception: punar
["punar", "punar", "punaH punar"],
["punar", "milAmaH", "punar milAmaH"],
["punar", "ramati", "punaH ramati"],
["punar", "uvAca", "punar uvAca"],

# Special cases from the tables
["wordi", "aword", "wordyaword"],
["wordI", "aword", "wordyaword"],
["wordu", "aword", "wordvaword"],
["wordU", "aword", "wordvaword"],
["worde", "aword", "worde 'word"],
["wordo", "Aword", "wordavAword"],
["wordaN", "aword", "wordaNN aword"],
["wordAN", "aword", "wordAN aword"],
["wordan", "aword", "wordann aword"],
["wordAn", "aword", "wordAn aword"],
["wordn", "Sword", "wordY Sword"],
["wordaH", "aword", "wordo 'word"],
["wordaH", "oword", "worda oword"],
["wordiH", "aword", "wordir aword"],
["wordiH", "rword", "wordI rword"],
["wordUH", "rword", "wordU rword"],
["wordaH", "gword", "wordo gword"],
["wordaH", "cword", "wordaS cword"],
["wordAH", "gword", "wordA gword"],
["wordAH", "cword", "wordAS cword"],
["wordiH", "gword", "wordir gword"],
["wordiH", "cword", "wordiS cword"]
]

from cmd_generator import CmdGenerator
generator = CmdGenerator('sanskrit')

tries = []
for num, test in enumerate(tests):
    cmds = generator.find_sandhis_for(test[0], test[1])
    if cmds == None:
        cmds = '{},$/=0'.format(test[0])
    if test[1] != '':
        cmds += '\n{},$/=0'.format(test[1])
    tries.append((num+1, cmds))

for trie in tries:
    with open('../output/tries/{}.txt'.format(trie[0]), 'w') as f:
        f.write(trie[1])
