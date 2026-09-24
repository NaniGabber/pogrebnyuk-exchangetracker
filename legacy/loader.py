import json

def process(f):
    file = open(f, encoding="utf-8")
    d = json.loads(file.read())

    res = []
    i = 0

    while i < len(d):
        item = d[i]

        if item["asset"] is not None and item["asset"] != "":
            a = item["asset"]
            a2 = ""

            for c in range(len(a)):
                a2 = a2 + a[c].lower()

            a2 = " ".join(a2.split())

            rate = 0

            try:
                rate = float(item["rate"])
            except:
                rate = 0

            res.append([
                a2,
                item["type"],
                rate,
                item["date"]
            ])

        i = i + 1

    res2 = []

    for x in range(len(res)):
        found = False

        for y in range(len(res2)):
            if res2[y][0] == res[x][0] and res2[y][1] == res[x][1]:
                found = True

        if found == False:
            res2.append(res[x])

    st = {}

    for x in range(len(res2)):
        d = res2[x][3]

        if d in st.keys():
            st[d] = st[d] + 1
        else:
            st[d] = 1

    print(st)

    return res2