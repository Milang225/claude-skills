#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
blocs_mdc.py — Helper pour écrire des tableaux chiffrés MDC SANS erreur de total.

RÈGLE : un total ou un montant net n'est JAMAIS saisi en dur. Il est écrit comme
FORMULE Excel vivante qui somme exactement les lignes au-dessus. La déduction
étant stockée en NÉGATIF, `=SUM(...)` fait la soustraction toute seule — il
devient structurellement impossible d'additionner une déduction à la place de la
soustraire (cause de l'erreur TVA du dossier LERO, 24/07/2026).

Le classeur porte `fullCalcOnLoad = True` : Excel recalcule à l'ouverture.
Le convertisseur `xlsx_to_pdf_mdc.py` évalue les =SUM()/±refs pour le PDF.

Usage :
    from blocs_mdc import Bloc
    b = Bloc(ws, col_montant=2)           # colonne B = montants
    b.ligne(6, "TVA collectée sur ventes", 14084030)
    b.ligne(7, "moins TVA déductible",   -3444781)   # déduction EN NÉGATIF
    b.total(8, "= TVA À PAYER")           # écrit =SUM(B6:B7) — soustraction auto
    # -> total garanti = 10 639 249, jamais 17 528 811 (addition)
"""
from openpyxl.utils import get_column_letter


class Bloc:
    def __init__(self, ws, col_montant=2):
        self.ws = ws
        self.col = col_montant
        self.lettre = get_column_letter(col_montant)
        self._debut = None      # 1re ligne de données du groupe courant
        self._fin = None        # dernière ligne de données
        self._refs = []         # lignes de total à ré-agréger (sous-totaux)

    def ligne(self, row, libelle, montant, col_libelle=1):
        """Écrit une ligne de donnée. La déduction se passe en montant NÉGATIF."""
        self.ws.cell(row=row, column=col_libelle, value=libelle)
        self.ws.cell(row=row, column=self.col, value=montant)
        if self._debut is None:
            self._debut = row
        self._fin = row
        return montant

    def total(self, row, libelle, col_libelle=1, sous_totaux=None):
        """Écrit le total comme FORMULE =SUM() sur la plage du groupe.

        `sous_totaux` : liste de lignes de sous-totaux à sommer à la place d'une
        plage continue (pour un total général qui agrège des sous-totaux)."""
        self.ws.cell(row=row, column=col_libelle, value=libelle)
        if sous_totaux:
            formule = "=" + "+".join(f"{self.lettre}{r}" for r in sous_totaux)
        else:
            if self._debut is None:
                raise ValueError("aucune ligne écrite avant le total")
            formule = f"=SUM({self.lettre}{self._debut}:{self.lettre}{self._fin})"
        self.ws.cell(row=row, column=self.col, value=formule)
        # nouveau groupe après un total
        self._debut = self._fin = None
        return row

    def valeur_attendue(self, lignes):
        """Somme de contrôle Python — à comparer par assert après construction."""
        return sum(lignes)


def finaliser(wb):
    """À appeler avant save() : force Excel à recalculer les formules."""
    wb.calculation.fullCalcOnLoad = True
    return wb
