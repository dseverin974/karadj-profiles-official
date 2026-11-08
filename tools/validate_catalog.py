#!/usr/bin/env python3
"""Vérifie catalog.json (schéma + SHA-256 des profils). La signature Ed25519 est vérifiée par openssl dans le workflow."""
import hashlib, json, os, re, sys

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors = []
    with open(os.path.join(root, "catalog.json"), encoding="utf-8") as f:
        cat = json.load(f)
    if cat.get("format") != "karadj-midi-profile-catalog":
        errors.append("format invalide")
    if cat.get("version") != 1:
        errors.append("version doit valoir 1")
    if not isinstance(cat.get("profiles"), list):
        errors.append("profiles doit être une liste")
    ids = set()
    for i, p in enumerate(cat.get("profiles", [])):
        tag = f"profiles[{i}]"
        for k in ("id", "file", "sha256", "license"):
            if not p.get(k):
                errors.append(f"{tag}: champ manquant: {k}")
        if p.get("id") in ids:
            errors.append(f"{tag}: id en double: {p.get('id')}")
        ids.add(p.get("id"))
        if not re.fullmatch(r"[0-9a-f]{64}", p.get("sha256", "")):
            errors.append(f"{tag}: sha256 invalide")
        rel = p.get("file", "")
        if not rel.startswith("profiles/") or ".." in rel:
            errors.append(f"{tag}: file doit être sous profiles/")
            continue
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            errors.append(f"{tag}: fichier absent: {rel}")
            continue
        data = open(path, "rb").read()
        if hashlib.sha256(data).hexdigest() != p.get("sha256"):
            errors.append(f"{tag}: sha256 ne correspond pas à {rel}")
        try:
            prof = json.loads(data)
            if prof.get("format") != "karadj-midi-profile" or prof.get("version") != 1:
                errors.append(f"{tag}: {rel} n'est pas un karadj-midi-profile v1")
        except ValueError:
            errors.append(f"{tag}: {rel} n'est pas du JSON valide")
    for e in errors:
        print("ERREUR:", e)
    print(f"{len(cat.get('profiles', []))} profil(s), {len(errors)} erreur(s)")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
