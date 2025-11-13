#!/usr/bin/env python3
# coding: utf-8
"""
bruteforce_rootme_alphabet.py
Version du script adaptée à l'alphabet demandé :
letters (a-zA-Z) + digits (0-9) + the symbols: ! ? ; . { } ( ) = + -
Teste clés de longueur 1..MAX_KEY_LEN (par défaut 1..3).
"""

from itertools import product
from multiprocessing import Pool, cpu_count
import string

# --- Configuration ---
CIPHER = bytes([
    0x71, 0x11, 0x24, 0x59, 0x8d, 0x6d, 0x71, 0x11, 0x35, 0x16, 0x8c, 0x6d, 0x71, 0x0d, 0x39, 0x47,
    0x1f, 0x36, 0xf1, 0x2f, 0x39, 0x36, 0x8e, 0x3c, 0x4b, 0x39, 0x35, 0x12, 0x87, 0x7c, 0xa3, 0x10,
    0x74, 0x58, 0x16, 0xc7, 0x71, 0x56, 0x68, 0x51, 0x2c, 0x8c, 0x73, 0x45, 0x32, 0x5b, 0x8c, 0x2a,
    0xf1, 0x2f, 0x3f, 0x57, 0x6e, 0x04, 0x3d, 0x16, 0x75, 0x67, 0x16, 0x4f, 0x6d, 0x1c, 0x6e, 0x40,
    0x01, 0x36, 0x93, 0x59, 0x33, 0x56, 0x04, 0x3e, 0x7b, 0x3a, 0x70, 0x50, 0x16, 0x04, 0x3d, 0x18,
    0x73, 0x37, 0xac, 0x24, 0xe1, 0x56, 0x62, 0x5b, 0x8c, 0x2a, 0xf1, 0x45, 0x7f, 0x86, 0x07, 0x3e,
    0x63, 0x47
])

# alphabet demandé : lettres (maj+min), chiffres, et les symboles ! ? ; . { } ( ) = + -
ALPHABET = string.ascii_letters + string.digits + "<>!"

# par défaut 1..3 ; augmente à tes risques (complexité = len(ALPHABET)^L)
MAX_KEY_LEN = 6
N_PROCS = max(1, cpu_count() - 0)  # ajuster -1 pour laisser un coeur libre

JS_SUM_TARGET = 8932
FILTER_REQUIRE_SUM = True  # si False, n'applique pas le test de somme du JS

# --- fonctions reproduisant le JS ---


def rotate_left_8(x, y):
    """Rotate left 8-bit value x by y (0<=y)."""
    y = y % 8
    # mask for top y bits (bits 8-y .. 7)
    top_mask = 0
    for i in range(8 - y, 8):
        top_mask += (1 << i)
    part = (x & top_mask) >> (8 - y)
    result = ((part) + ((x << y) & 0xff)) & 0xff
    return result


def decrypt_with_key(cipher_bytes, key_bytes):
    """
    Implémente l'algorithme JS de décryptage :
    - i == 0 : out[0] = c ^ key[0]
    - i > 0  : t = out[i-1] % 2
       if t == 0 -> out[i] = c ^ key[i % keylen]
       if t == 1 -> out[i] = rotate_left_8(c, keybyte)
    """
    out = bytearray()
    klen = len(key_bytes)
    for i, c in enumerate(cipher_bytes):
        kb = key_bytes[i % klen]
        if i == 0:
            cr = c ^ kb
        else:
            t = out[i - 1] % 2
            if t == 0:
                cr = c ^ kb
            else:
                cr = rotate_left_8(c, kb)
        out.append(cr & 0xff)
    return bytes(out)


def is_all_printable(b):
    """Vérifie que tous les octets sont imprimables ASCII (0x20..0x7e)."""
    return all(0x20 <= x <= 0x7e for x in b)


def worker_try_keys(keys_batch):
    """Teste un lot de clés et retourne celles qui donnent du texte imprimable
    (et optionnellement vérifient la somme JS)."""
    matches = []
    for key in keys_batch:
        kb = key.encode('latin1')
        plain = decrypt_with_key(CIPHER, kb)
        if is_all_printable(plain):
            plain_str = plain.decode('latin1')
            if FILTER_REQUIRE_SUM:
                if sum(plain) == JS_SUM_TARGET:
                    matches.append((key, plain_str))
            else:
                matches.append((key, plain_str))
    return matches


def generate_keys(max_len):
    for l in range(1, max_len + 1):
        for tup in product(ALPHABET, repeat=l):
            yield ''.join(tup)


def chunked_iterable(iterable, chunk_size=2000):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= chunk_size:
            yield batch
            batch = []
    if batch:
        yield batch


def main():
    print("Brute-force (alphabet personnalisé)")
    print(f"Alphabet length: {len(ALPHABET)}")
    print(f"Clés testées: longueur 1..{MAX_KEY_LEN}")
    print(f"Workers: {N_PROCS}")
    if FILTER_REQUIRE_SUM:
        print(f"Filtre: somme des codes == {JS_SUM_TARGET}")
    print("Lancement...\n")

    gen = generate_keys(MAX_KEY_LEN)
    batches = chunked_iterable(gen, chunk_size=2000)
    pool = Pool(processes=N_PROCS)
    total = 0
    found_any = False
    try:
        for batch in batches:
            total += len(batch)
            res = pool.apply_async(worker_try_keys, (batch,))
            matches = res.get()
            for key, plain in matches:
                found_any = True
                print("=" * 60)
                print(f"Key : {repr(key)}")
                print(f"Plain: {plain}")
                print("=" * 60)
            # petit rapport périodique
            if total % (2000 * 10) == 0:
                print(f"[~{total} clés testées]")
    except KeyboardInterrupt:
        print("Interrompu par l'utilisateur.")
    finally:
        pool.terminate()
        pool.join()

    if not found_any:
        print("\nAucun résultat imprimable trouvé avec les paramètres actuels.")
        print("Tu peux : augmenter MAX_KEY_LEN, désactiver FILTER_REQUIRE_SUM or restreindre l'alphabet.")


if __name__ == "__main__":
    main()
