import json, re
W = json.load(open("work/words.json"))
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
toks = [norm(w[0]) for w in W]
ANCH = [("trump","wants"),("but","iran"),("speaking","to"),("his","reason"),("a","normal"),("in","2018"),("now","iran"),("its","foreign"),("but","first"),("then","iran"),("about","one"),("meanwhile","the"),("on","wednesday"),("kuwait","says"),("and","on"),("trumps","envoys"),("so","a"),("lets","see"),("follow","for")]
idx, k = [], 0
for a, b in ANCH:
    while not (toks[k] == a and toks[k+1] == b): k += 1
    idx.append(k); k += 1
idx.append(len(W))
sents = [[W[i][1], W[j-1][2], j-i] for i, j in zip(idx, idx[1:])]
json.dump(sents, open("work/src_sentences.json", "w"))
for s in sents: print(round(s[0],2), round(s[1],2), round(s[1]-s[0],2), s[2])
print("speech sum", round(sum(s[1]-s[0] for s in sents),2))
