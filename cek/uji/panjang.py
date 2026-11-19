# File uji fitur 2: ada satu fungsi yang lebih dari 30 baris.

def salam_singkat(nama):
    return f"halo {nama}"


def proses_data(daftar):
    hasil = []
    indeks = 0
    while indeks < len(daftar):
        item = daftar[indeks]
        if item is None:
            indeks += 1
            continue
        if isinstance(item, str):
            item = item.strip()
            item = item.lower()
        if isinstance(item, (int, float)):
            if item < 0:
                item = 0
            elif item > 100:
                item = 100
        if isinstance(item, dict):
            item = dict(item)
            item["diproses"] = True
        if isinstance(item, list):
            item = list(item)
            item.reverse()
        if item == "":
            indeks += 1
            continue
        if item == 0:
            indeks += 1
            continue
        hasil.append(item)
        indeks += 1
    total = 0
    for x in hasil:
        total += 1
    if total == 0:
        return []
    rata = total / len(hasil)
    if rata > 10:
        return hasil
    return hasil
