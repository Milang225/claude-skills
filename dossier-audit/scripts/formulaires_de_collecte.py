# -*- coding: utf-8 -*-
"""Les formulaires de collecte d'un dossier d'audit : un classeur, neuf feuilles, chacune
un VRAI formulaire a remplir, avec ses colonnes propres, ses listes de choix et ses lignes
vides — pre-rempli de ce que l'Atelier du diagnostic porte deja.

  python3 formulaires_de_collecte.py LBTECH "<dossier d'audit>"
  python3 formulaires_de_collecte.py LBTECH --etat     (l'etat des besoins, sans produire)
"""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from donnees_dossier import charger, pivots, f
from squelettes_audit import exercices

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter
except ImportError:
    raise SystemExit("Les formulaires ont besoin d'openpyxl. Installer : python3 -m pip install openpyxl")

NAVY, GRIS, OR, CREME, ROUGE = "1A1A2E", "EEF0F4", "8A6D1F", "FBF7F0", "FDE9E7"
FIN = Side(style="thin", color="B8BCC6")
BORD = Border(left=FIN, right=FIN, top=FIN, bottom=FIN)
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]

# ── les besoins, pour l'etat et pour la feuille de tete
BESOINS = [
 ("F1", "Raison sociale, NCC, RCCM, forme juridique, capital", "Tous les livrables", "client.raison_sociale", "Secrétariat"),
 ("F1", "Exercices couverts par la mission", "Tous les livrables", "client.exercices", "Superviseur"),
 ("F1", "Nom, qualité et formule d'appel du dirigeant", "Tous les livrables", "client.dirigeant", "Secrétariat"),
 ("F1", "Régime fiscal effectif, et l'avis qui l'établit", "Rapport, chiffrage, note au comptable", "l01.regime", "Juridico-Fiscal"),
 ("F1", "Activité réelle, et activité déclarée si elle diffère", "Rapport, constat", "l01.activite", "Juridico-Fiscal"),
 ("F2", "Inventaire des pièces applicables, une ligne par pièce", "Audit documentaire", "l02.documents", "Coordination"),
 ("F2", "Pour chaque pièce absente : pourquoi, et ce que l'absence coûte", "Audit documentaire, plan d'action", "l02.documents", "Juridico-Fiscal"),
 ("F2", "Pièces sans objet, à écarter du score", "Audit documentaire", "l02.domaines", "Coordination"),
 ("F3", "Grille déclarative : nature d'impôt × période, déclaré et payé", "Rapport, synthèse, tableau", "l03.mensuel", "Juridico-Fiscal"),
 ("F3", "Avis émis : numéro, montant, base, date, paiements imputés", "Note de chiffrage, tableau", "l03.fiscal", "Juridico-Fiscal"),
 ("F3", "Procédures de l'administration : mise en demeure, ATD, contrôle", "Rapport, constat, plan d'action", "l03.fiscal", "Juridico-Fiscal"),
 ("F3", "Obligations sociales déclarées et payées, mois par mois", "Rapport, synthèse", "l03.social_mensuel", "Comptabilité"),
 ("F4", "Relevés bancaires complets de la période, compte par compte", "Rapport, chiffrage, trésorerie", "l05.argent_entre", "Comptabilité"),
 ("F4", "Catégorisation des entrées et des sorties, pièce par pièce", "Note de chiffrage, matrices", "l05.argent_sort", "Comptabilité"),
 ("F4", "Encaissements en espèces : carnets de reçus, numéros, montants", "Droit de timbre, CA reconstitué", "l05.ce_qui_pese", "Comptabilité"),
 ("F4", "Sommes remises au dirigeant, et la pièce de chacune", "Compte courant, IRVM, exposition", "l06.lignes", "Comptabilité"),
 ("F5", "Effectif réel, par exercice, avec dates d'entrée et de sortie", "Rapport, exposition salaires", "l11.categories", "Comptabilité"),
 ("F5", "Rémunérations versées, par salarié et par mois", "Exposition salaires, note au comptable", "l11.constats", "Comptabilité"),
 ("F5", "Contrats, bulletins, registre d'employeur : tenus ou non", "Constat, plan d'action, actes", "l11.registre", "Juridico-Fiscal"),
 ("F5", "Immatriculation à la caisse de prévoyance sociale, et numéro", "Exposition cotisations", "l11.obligations", "Comptabilité"),
 ("F6", "Sujets que le dirigeant demande d'arrêter", "Le point et les bons usages", "—", "Superviseur"),
 ("F6", "Assiette retenue pour le compte courant, et sa justification", "Le point, exposition, actes", "—", "Direction"),
 ("F6", "Arbitrages déjà rendus par la Direction, avec leur date", "Rapport, le point", "—", "Direction"),
 ("F6", "Questions du dirigeant appelant une note particulière", "Note particulière au dossier", "—", "Superviseur"),
 ("F7", "Conventions existantes, et conventions manquantes", "Rapport, modèles d'actes", "l09.domaines", "Juridico-Fiscal"),
 ("F7", "Biens inscrits à l'actif au nom d'un tiers ou du dirigeant", "Séparation des patrimoines, actes", "l09.domaines", "Juridico-Fiscal"),
 ("F7", "Baux, et leur enregistrement", "Exposition, plan d'action", "l09.siege", "Juridico-Fiscal"),
 ("F7", "Procès-verbaux et registres sociaux tenus", "Constat, plan d'action", "l09.rapport", "Juridico-Fiscal"),
 ("F8", "Date, lieu et participants de l'entretien de restitution", "Script de restitution", "l10.date_heure", "Coordination"),
 ("F8", "Ce qui va bien dans le dossier, à dire en ouverture", "Script de restitution", "l10.avant", "Superviseur"),
 ("F8", "Points sensibles à ne pas dire, et pourquoi", "Script de restitution", "l10.points", "Superviseur"),
 ("F8", "Ce que l'Agence attend du dirigeant", "Script, plan d'action", "l10.points", "Superviseur"),
]
NOMS = {"F1": "F1 Identité et cadrage", "F2": "F2 Pièces du client", "F3": "F3 Obligations et paiements",
        "F4": "F4 Flux et espèces", "F5": "F5 Paie et social", "F6": "F6 Décisions du dirigeant",
        "F7": "F7 Actes et conventions", "F8": "F8 Restitution"}


def valeur(D, chemin):
    if chemin.startswith("—"):
        return None
    cur = D
    for bout in chemin.split("."):
        if not isinstance(cur, dict) or bout not in cur:
            return None
        cur = cur[bout]
    if cur in (None, "", [], {}):
        return None
    if isinstance(cur, list):
        return "%d entrée(s)" % len(cur)
    if isinstance(cur, dict):
        return "%d champ(s)" % len(cur)
    return str(cur)[:70]


def etat(D):
    return [(c, q, l, ch, qui, valeur(D, ch)) for c, q, l, ch, qui in BESOINS]


# ─────────────────────────── mise en forme ───────────────────────────
class Classeur:
    def __init__(self, p):
        self.wb = openpyxl.Workbook(); self.wb.remove(self.wb.active)
        self.p = p
        self.sous = ("Client : %s (NCC %s)    |    Exercices %s    |    Référence : MC-COL-%s-%d-001    |    "
                     "Établi le %s" % (p["raison_sociale"], p["ncc"], p["exercices"], p["secteur"],
                                       datetime.date.today().year, datetime.date.today().strftime("%d/%m/%Y")))

    def feuille(self, nom, titre, pourquoi, qui):
        ws = self.wb.create_sheet(nom[:31]); ws.sheet_view.showGridLines = False
        ws["A1"] = "LA MAISON DE LA CONFORMITE — FORMULAIRE DE COLLECTE"
        ws["A1"].font = Font(bold=True, size=12, color="FFFFFF")
        ws["A2"] = self.sous; ws["A2"].font = Font(size=9, color=OR)
        for r in (1, 2):
            for c in range(1, 14):
                ws.cell(r, c).fill = PatternFill("solid", fgColor=NAVY)
        ws["A4"] = titre; ws["A4"].font = Font(bold=True, size=11, color=NAVY)
        ws["A5"] = "Ce formulaire sert à : %s" % pourquoi
        ws["A5"].font = Font(size=9, italic=True)
        ws["A6"] = "Rempli par : %s. Une case laissée vide est une donnée qui manquera au livrable." % qui
        ws["A6"].font = Font(size=9, italic=True, color=OR)
        return ws

    def tableau(self, ws, r, head, widths, rows=(), vides=12, choix=None):
        for j, h in enumerate(head, 1):
            c = ws.cell(r, j, h)
            c.font = Font(bold=True, size=9, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor=NAVY)
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
            c.border = BORD
        ws.row_dimensions[r].height = 30
        debut = r + 1
        for i, ligne in enumerate(rows):
            for j, x in enumerate(ligne, 1):
                c = ws.cell(debut + i, j, x)
                c.font = Font(size=9)
                c.alignment = Alignment(wrap_text=True, vertical="top")
                c.border = BORD
                c.fill = PatternFill("solid", fgColor=GRIS)
        for i in range(len(rows), len(rows) + vides):
            for j in range(1, len(head) + 1):
                c = ws.cell(debut + i, j)
                c.border = BORD
                c.fill = PatternFill("solid", fgColor=CREME)
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
        if choix:
            for col, options in choix.items():
                dv = DataValidation(type="list", formula1='"%s"' % ",".join(options), allow_blank=True)
                ws.add_data_validation(dv)
                dv.add("%s%d:%s%d" % (get_column_letter(col), debut, get_column_letter(col),
                                      debut + len(rows) + vides))
        return debut + len(rows) + vides + 2

    def titre_bloc(self, ws, r, texte):
        ws.cell(r, 1, texte).font = Font(bold=True, size=10, color=NAVY)
        return r + 1

    def enregistrer(self, dest):
        q = os.path.join(dest, "FORMULAIRES_DE_COLLECTE_%s_%s.xlsx"
                         % (self.p["raison_sociale"].replace(" ", "_").replace("'", ""),
                            datetime.date.today().isoformat()))
        self.wb.save(q)
        return q


# ─────────────────────────── les neuf feuilles ───────────────────────────
def f0_sommaire(K, D, lignes):
    ws = K.feuille("F0 Sommaire", "SOMMAIRE DES FORMULAIRES ET ÉTAT DES BESOINS",
                   "savoir ce qui manque avant d'écrire une ligne de livrable",
                   "le Superviseur, qui répartit les feuilles")
    rows = []
    for code in ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"):
        gr = [l for l in lignes if l[0] == code]
        vides = [l for l in gr if not l[5]]
        rows.append([NOMS[code], ", ".join(sorted({l[4] for l in gr})),
                     "%d" % len(gr), "%d" % len(vides),
                     "complet" if not vides else "à compléter",
                     "; ".join(sorted({l[2].split(",")[0] for l in gr}))])
    r = K.tableau(ws, 8, ["Formulaire", "Qui le remplit", "Besoins", "À fournir", "État",
                          "Les livrables qui en dépendent"],
                  [30, 26, 10, 11, 15, 46], rows, vides=0)
    ws.cell(r, 1, "Le détail des besoins, question par question :").font = Font(bold=True, size=10, color=NAVY)
    det = [[NOMS[c], q, l, qui, v or "— à fournir"] for c, q, l, ch, qui, v in lignes]
    K.tableau(ws, r + 1, ["Formulaire", "Ce qu'il faut fournir", "Le livrable qui en dépend",
                          "Qui répond", "Ce que le dossier porte déjà"],
              [28, 54, 34, 18, 30], det, vides=0)


def f1_identite(K, D):
    c, l01 = D.get("client", {}), D.get("l01") or {}
    ws = K.feuille(NOMS["F1"], "F1 — IDENTITÉ DE LA SOCIÉTÉ ET CADRAGE DE LA MISSION",
                   "l'en-tête de tous les livrables, le régime qui commande le chiffrage",
                   "le Secrétariat, puis le département Juridico-Fiscal pour le régime")
    champs = [
        ("Raison sociale", c.get("raison_sociale", "")), ("Ancienne dénomination, s'il y en a une", c.get("ancienne_denomination", "")),
        ("NCC", c.get("ncc", "")), ("RCCM", l01.get("rccm", "")),
        ("Forme juridique", ""), ("Capital social", ""),
        ("Siège social, adresse exacte", ""), ("Date de début d'activité", ""),
        ("Activité déclarée", l01.get("activite", "")), ("Activité réellement exercée", ""),
        ("Régime fiscal effectif", l01.get("regime", "")), ("L'avis ou la pièce qui établit ce régime", ""),
        ("Exercices couverts par la mission", c.get("exercices", "")),
        ("Nom et qualité du dirigeant", c.get("dirigeant", "")),
        ("Formule d'appel", c.get("formule", "")),
        ("Secteur, pour les références des documents", K.p["secteur"]),
        ("Comptable ou cabinet en charge", ""), ("Conseil juridique, avocat ou notaire", ""),
    ]
    rows = [[nom, val, "", ""] for nom, val in champs]
    K.tableau(ws, 8, ["Information demandée", "Ce que le dossier porte déjà", "À confirmer ou à corriger",
                      "La pièce qui l'établit"], [44, 40, 40, 38], rows, vides=4)


def f2_pieces(K, D):
    l02 = D.get("l02") or {}
    ws = K.feuille(NOMS["F2"], "F2 — INVENTAIRE DES PIÈCES DU CLIENT",
                   "l'audit documentaire, le score documentaire, et les limites déclarées du rapport",
                   "la Coordination, qui réclame, et le Juridico-Fiscal, qui dit ce que l'absence coûte")
    rows = [[d.get("domaine", ""), d.get("document", ""), d.get("situation", ""),
             d.get("pourquoi", ""), d.get("critique", ""), "", ""] for d in (l02.get("documents") or [])]
    rows = [r_[:2] + [""] + r_[2:] for r_ in rows]
    K.tableau(ws, 8, ["Domaine", "Pièce demandée", "Exercice", "Situation",
                      "Pourquoi elle manque, et ce que l'absence coûte", "Critique", "Reçue le", "Où elle est classée"],
              [18, 44, 11, 16, 48, 11, 13, 22], rows, vides=20,
              choix={4: ["Présente", "Incomplète", "Absente", "Sans objet", "À examiner"], 6: ["Oui", "Non"]})


def f3_obligations(K, D):
    l03 = D.get("l03") or {}
    ws = K.feuille(NOMS["F3"], "F3 — OBLIGATIONS DÉCLARÉES ET PAYÉES",
                   "le tableau d'exposition, la synthèse, et la matrice fiscale du rapport",
                   "le département Juridico-Fiscal, sur l'historique e-impôts et les avis")
    r = K.titre_bloc(ws, 8, "1. La grille déclarative — une case par nature et par mois")
    ws.cell(r, 1, "Codes : D+ déclaré et payé · D− déclaré non payé · D* déclaré à zéro ou minoré · "
                  "N non déclaré · TO+ taxé d'office payé · TO− taxé d'office non payé · — néant · ~ à vérifier")
    ws.cell(r, 1).font = Font(size=8, italic=True)
    natures = [n.get("nature", "") if isinstance(n, dict) else str(n) for n in (l03.get("mensuel") or [])]
    if not natures:
        natures = ["Impôt sur les traitements et salaires", "Contribution nationale et formation",
                   "Cotisations de prévoyance sociale", "Droit de timbre de quittance",
                   "Taxe de l'entreprenant ou impôt des microentreprises", "Taxe sur la valeur ajoutée",
                   "Retenues à la source", "Taxe spéciale d'équipement"]
    r += 1
    for an in exercices(K.p):
        r = K.titre_bloc(ws, r, "Exercice %d" % an)
        rows = [[n, an] + [""] * 12 for n in natures]
        r = K.tableau(ws, r, ["Nature de l'impôt ou de la cotisation", "Exercice"] + MOIS,
                      [46, 10] + [7] * 12, rows, vides=3,
                      choix={j: ["D+", "D-", "D*", "N", "TO+", "TO-", "—", "~"] for j in range(3, 15)})
    r = K.titre_bloc(ws, r, "2. Les avis émis par l'administration")
    r = K.tableau(ws, r, ["Nature", "Numéro de l'avis", "Date", "Base retenue", "Montant",
                          "Payé à ce jour", "Reste dû", "Pièce"],
                  [30, 26, 13, 18, 16, 16, 16, 28], (), vides=12)
    r = K.titre_bloc(ws, r, "3. Les procédures de l'administration : mise en demeure, avis à tiers détenteur, contrôle")
    K.tableau(ws, r, ["Nature de la procédure", "Date", "Impôt visé", "Montant", "Suite donnée", "Pièce"],
              [34, 13, 26, 16, 40, 28], (), vides=8)


def f4_flux(K, D):
    ws = K.feuille(NOMS["F4"], "F4 — FLUX BANCAIRES ET ESPÈCES",
                   "la note de chiffrage, le compte courant, le droit de timbre et le chiffre d'affaires reconstitué",
                   "le département Comptabilité, sur les relevés et les carnets")
    r = K.titre_bloc(ws, 8, "1. Les comptes, y compris ceux ouverts au nom du dirigeant qui ont reçu des recettes")
    r = K.tableau(ws, r, ["Banque", "Numéro de compte", "Titulaire", "Ouvert le", "Période couverte par le relevé",
                          "Relevé fourni", "Observations"],
                  [22, 26, 28, 13, 28, 14, 34], (), vides=8, choix={6: ["Oui", "Non", "Partiel"]})
    r = K.titre_bloc(ws, r, "2. Les flux à qualifier — un par ligne, avec sa pièce")
    r = K.tableau(ws, r, ["Date", "Libellé du relevé", "Entrée ou sortie", "Montant", "Catégorie retenue",
                          "Bénéficiaire ou payeur", "Pièce", "Adossé"],
                  [13, 42, 15, 16, 28, 28, 26, 12], (), vides=25,
                  choix={3: ["Entrée", "Sortie"], 8: ["Adossé", "À adosser", "Non adossé"]})
    r = K.titre_bloc(ws, r, "3. Les encaissements en espèces — carnets de reçus")
    K.tableau(ws, r, ["Carnet", "Numéros de reçus", "Période", "Nombre de reçus", "Total encaissé",
                      "Carnet fourni", "Observations"],
              [16, 24, 24, 16, 18, 14, 36], (), vides=10, choix={6: ["Oui", "Non"]})


def f5_paie(K, D):
    ws = K.feuille(NOMS["F5"], "F5 — PAIE ET OBLIGATIONS SOCIALES",
                   "l'exposition aux impôts sur salaires et aux cotisations, et la matrice sociale",
                   "le département Comptabilité, et le Juridico-Fiscal pour les contrats et registres")
    r = K.titre_bloc(ws, 8, "1. L'effectif réel, exercice par exercice — y compris le dirigeant")
    r = K.tableau(ws, r, ["Exercice", "Nom et prénoms", "Poste", "Entré le", "Sorti le", "Rémunération mensuelle",
                          "Mode de paiement", "Déclaré à la caisse", "Déclaré à l'impôt sur salaires",
                          "Contrat écrit", "Bulletins établis"],
                  [11, 26, 20, 13, 13, 20, 18, 17, 20, 14, 16], (), vides=18,
                  choix={1: [str(a) for a in exercices(K.p)], 8: ["Oui", "Non"], 9: ["Oui", "Non"],
                         10: ["Oui", "Non"], 11: ["Oui", "Non"]})
    r = K.titre_bloc(ws, r, "2. L'immatriculation et les registres de l'employeur")
    champs = [["Immatriculation à la caisse de prévoyance sociale", "", ""],
              ["Numéro d'employeur", "", ""], ["Registre d'employeur tenu", "", ""],
              ["Registre des délibérations tenu", "", ""], ["Déclaration annuelle des salaires déposée", "", ""],
              ["Médecine du travail", "", ""], ["Travailleurs étrangers : visas et contrats", "", ""]]
    K.tableau(ws, r, ["Obligation", "Oui, non, ou sans objet", "La pièce qui l'établit"],
              [52, 24, 44], champs, vides=4, choix={2: ["Oui", "Non", "Sans objet", "À vérifier"]})


def f6_decisions(K, D):
    ws = K.feuille(NOMS["F6"], "F6 — DÉCISIONS DU DIRIGEANT ET ARBITRAGES DE LA DIRECTION",
                   "« Le point et les bons usages », la note particulière, et les montants arrêtés du dossier",
                   "le Superviseur, qui recueille, et la Direction, qui arrête")
    ws.cell(7, 1, "L'Atelier ne porte rien de tout cela : sans cette feuille, « Le point et les bons usages » "
                  "reste un squelette et n'entre dans aucun inventaire.").font = Font(size=9, italic=True, color=OR)
    r = K.titre_bloc(ws, 9, "1. Les sujets que le dirigeant demande d'arrêter")
    r = K.tableau(ws, r, ["Sujet", "La question exacte qu'il pose", "Ce que nous avons répondu",
                          "Décision arrêtée", "Arrêtée le", "Par qui", "Le livrable qui la porte"],
                  [30, 44, 44, 40, 13, 18, 30], (), vides=10)
    r = K.titre_bloc(ws, r, "2. Les montants arrêtés par la Direction, et ce qui les fonde")
    r = K.tableau(ws, r, ["Montant arrêté", "Objet", "Assiette retenue", "Pourquoi celle-là et pas une autre",
                          "Arrêté le", "Incidence sur quel livrable"],
                  [20, 34, 24, 50, 13, 34], (), vides=8)
    r = K.titre_bloc(ws, r, "3. Les questions du dirigeant appelant une note particulière")
    K.tableau(ws, r, ["Question posée", "Le jour où elle a été posée", "Note à produire", "Qui la rédige"],
              [56, 20, 40, 22], (), vides=6)


def f7_actes(K, D):
    ws = K.feuille(NOMS["F7"], "F7 — ACTES, CONVENTIONS ET BIENS",
                   "les modèles d'actes, la séparation des patrimoines et le plan d'action",
                   "le département Juridico-Fiscal")
    r = K.titre_bloc(ws, 8, "1. Les actes et conventions : ce qui existe, ce qui manque")
    actes = [["Convention de compte courant d'associé"], ["Contrat de bail à usage professionnel"],
             ["Contrats de travail"], ["Procès-verbaux d'approbation des comptes"],
             ["Décision fixant la rémunération du dirigeant"], ["Acte de cession des biens au nom d'un tiers"],
             ["Contrats avec les partenaires et prestataires"], ["Statuts à jour"]]
    rows = [a + ["", "", "", "", "", ""] for a in actes]
    r = K.tableau(ws, r, ["Acte ou convention", "Existe", "Date de l'acte", "Enregistré",
                          "Où se trouve l'original", "Qui doit l'établir", "Urgence"],
                  [44, 12, 15, 14, 30, 24, 14], rows, vides=8,
                  choix={2: ["Oui", "Non"], 4: ["Oui", "Non", "Sans objet"],
                         6: ["Avocat", "Notaire", "La société", "L'Agence"], 7: ["Immédiate", "Prochaine", "Différée"]})
    r = K.titre_bloc(ws, r, "2. Les biens inscrits à l'actif, et au nom de qui ils sont")
    r = K.tableau(ws, r, ["Bien", "Identification", "Valeur aux livres", "Au nom de qui",
                          "Pièce de propriété", "Régularisation prévue"],
                  [30, 26, 18, 28, 28, 34], (), vides=12)
    r = K.titre_bloc(ws, r, "3. Les baux et leur enregistrement")
    K.tableau(ws, r, ["Local", "Bailleur", "Loyer annuel", "Bail écrit", "Enregistré", "Quittance d'enregistrement"],
              [28, 28, 18, 14, 14, 34], (), vides=6, choix={4: ["Oui", "Non"], 5: ["Oui", "Non"]})


def f8_restitution(K, D):
    l10 = D.get("l10") or {}
    ws = K.feuille(NOMS["F8"], "F8 — ENTRETIEN DE RESTITUTION",
                   "le script de restitution, document interne qui ne se remet jamais au client",
                   "la Coordination pour la logistique, le Superviseur pour le fond")
    champs = [["Date et heure", l10.get("date_heure", "")], ["Lieu", l10.get("lieu", "")],
              ["Durée prévue", l10.get("duree", "")],
              ["Présents pour l'entreprise", l10.get("presents_entreprise", "")],
              ["Présents pour l'Agence", l10.get("presents_agence", "")]]
    rows = [[n, v if isinstance(v, str) else "", ""] for n, v in champs]
    r = K.tableau(ws, 8, ["Élément", "Ce que le dossier porte déjà", "À compléter"], [30, 44, 44], rows, vides=2)
    r = K.titre_bloc(ws, r, "1. Ce qui va bien, et qu'il faut dire en ouverture")
    r = K.tableau(ws, r, ["Ce qui va bien", "Ce qui le prouve"], [60, 60], (), vides=6)
    r = K.titre_bloc(ws, r, "2. Ce qu'il ne faut pas dire, et pourquoi")
    r = K.tableau(ws, r, ["À ne pas dire", "Pourquoi", "Ce qu'il faut dire à la place"],
                  [40, 44, 44], (), vides=6)
    r = K.titre_bloc(ws, r, "3. Les questions qu'il va poser, et la réponse")
    r = K.tableau(ws, r, ["La question attendue", "La réponse"], [50, 70], (), vides=8)
    r = K.titre_bloc(ws, r, "4. Ce que l'Agence attend de lui à l'issue de l'entretien")
    K.tableau(ws, r, ["Ce que nous attendons", "De qui", "Ce que cela débloque"], [50, 22, 48], (), vides=6)


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    D, source = charger(a[0], a[a.index("--json") + 1] if "--json" in a else None)
    p = pivots(D); p["lignes_sans_piece"] = 0
    lignes = etat(D)
    manquants = [l for l in lignes if not l[5]]
    print("ÉTAT DES BESOINS — %s" % p["raison_sociale"])
    for code in ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"):
        gr = [l for l in lignes if l[0] == code]
        vides = [l for l in gr if not l[5]]
        print("  %-28s %d besoin(s), %d à fournir" % (NOMS[code], len(gr), len(vides)))
    print("  %d besoins, %d couverts, %d à fournir." % (len(lignes), len(lignes) - len(manquants), len(manquants)))
    if "--etat" in a:
        return 0
    dest = a[1]
    os.makedirs(dest, exist_ok=True)
    K = Classeur(p)
    f0_sommaire(K, D, lignes); f1_identite(K, D); f2_pieces(K, D); f3_obligations(K, D)
    f4_flux(K, D); f5_paie(K, D); f6_decisions(K, D); f7_actes(K, D); f8_restitution(K, D)
    print("\nÉcrit : %s" % K.enregistrer(dest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
