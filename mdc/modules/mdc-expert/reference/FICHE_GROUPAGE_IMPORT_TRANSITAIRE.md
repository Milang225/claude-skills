# FICHE — GROUPAGE / IMPORT VIA TRANSITAIRE (juridique + fiscal + comptable)
> Sources : Niamba (TVA/Bénéfices), Kadouamai (Traitement op.), Doumbia (Compta), CGI CI, OHADA. Capitalisé juin 2026.

## QUALIFICATION JURIDIQUE (OHADA)
- **Commissionnaire de transport / groupeur** : agit EN SON NOM PROPRE pour le compte du commettant (AUDCG, intermédiaires de commerce). Garant de la bonne fin (responsable du fait des transporteurs substitués). Obligation de résultat.
- **Transitaire (mandataire)** : agit AU NOM et POUR LE COMPTE du client (mandat). Tenu de ses seules fautes prouvées. Obligation de moyens.
- **Commissionnaire en douane agréé** : statut réglementé (Code des douanes), agrément ; responsabilité solidaire douane/AIRSI.
- **Courtier** : met en relation, juridiquement indépendant, ne conclut pas.
- Transport : **AUTMR** (Acte Uniforme contrats de transport de marchandises par route, 22/03/2003) — lettre de voiture, responsabilité de plein droit du transporteur (perte/avarie/retard) sauf causes exonératoires, limitation d'indemnité, **prescription 1 an** (art. 25 AUTMR).
- Vente + transfert propriété/risques : **AUDCG vente commerciale** + **Incoterms** (EXW/FOB/CIF/DDP...) déterminent qui paie le transport/assurance et quand les risques passent.
- **Réserve de propriété** : opposable si écrite avant livraison (AUDCG + SYSCOHADA révisé).

## FISCAL (CGI CI)
- Commissionnaire EN SON NOM → TVA sur la TOTALITÉ refacturée (déduit TVA amont) : il est réputé avoir personnellement reçu et fourni les services (CGI art. 342). Les frais accessoires (commission, transport, assurance…) demandés au client entrent dans la base (art. 358-1°).
- Mandataire → TVA sur la COMMISSION seulement ; débours hors TVA si mandat + note de débours + factures originales + reddition de compte.
  - ⚠️ **Corrigé le 10/10/2026 — fondement.** L'**art. 358-2°** du CGI 2026 vise les ristournes, remises et rabais, **pas les débours** : ne plus le citer. **Aucun article du CGI 2026 n'exclut expressément les débours** de la base de TVA. L'exclusion repose sur : (1) la **preuve** que les frais ont été engagés **au nom et pour le compte du client** (mandat, facture du tiers au nom du client, refacturation au centime, reddition de compte) — à défaut, l'art. 358-1° les fait entrer dans la base comme frais accessoires ; (2) la **doctrine fiscale DGI 2026**, qui écarte les « remboursements de frais ou débours » du calcul du prorata de déduction (DOCTRINE_FISCALE_2026_TEXTE.txt, p. 154) et les débours de la base de la retenue à la source sur les rémunérations de prestations visée à l'art. 92 (p. 183). Ces deux passages confirment la logique, mais aucun ne vise directement la base de la TVA collectée.
  - « **Note DGI 2404/2018** » : **NON VÉRIFIÉE** — introuvable dans le corpus local (CGI 2026, doctrine 2026, bulletin officiel 2026). Ne pas la citer dans un livrable avant d'en avoir obtenu le texte.
- Territorialité transport : lieu de destination (Art 352) ; transport marchandises imposable de plein droit (AF 2024 art 3).
- Transit international / transbordement / export = exonérés / suspensifs (Art 356, 389, 390).
- Commissions/courtages = cpte 6322, déclarables Art 108-1° (≥ 50 000/an/bénéficiaire). Charges > 250 000 espèces non déductibles (Art 18 bis).

## COMPTABLE — CÔTÉ IMPORTATEUR (sa marchandise)
Coût d'acquisition = prix d'achat (cours du jour) + frais accessoires (douane + transit/groupage + transport + commission + assurance) − réductions (SYSCOHADA Art 36-37).
- TVA récupérable à part (4452/4453/4454) ; TVA NON déductible → ajoutée au coût.
- Devises : coût figé au cours du jour ; écarts au règlement → 676 perte / 776 gain (n'affectent pas le coût).
Écriture : D 6011 (prix) + D 6015 (frais accessoires) + D 4452/4453 (TVA) / C 401 fournisseur étranger + C 401 transitaire (ou 521). Entrée en stock 31, valorisation CMP/PEPS (LIFO interdit).
Anomalie d'audit classique : passer le transit en charge isolée → minore le stock, gonfle les charges, fausse le triangle CMV.
