# Proposer un profil

1. Ouvrez une issue avec le modèle « Proposer un profil » et collez le contenu produit par KaraDJ (`karadj-midi-profile-submission`).
2. Un mainteneur relit la licence (CC0-1.0, CC-BY-4.0 ou MIT) et l'auteur.
3. Il ajoute `profiles/<id>.json`, met à jour le `sha256` dans `catalog.json`, puis re-signe le catalogue hors ligne.
4. Aucune pull request ne modifie `catalog.json` sans re-signature : la CI refuse une signature invalide.
