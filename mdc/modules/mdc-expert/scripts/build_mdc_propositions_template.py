#!/usr/bin/env python3
"""Generate MDC commercial documents for TIM 7 MULTISERVICE - format officiel MDC."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1A, 0x1A, 0x2E)
GOLD = RGBColor(0xE8, 0xC5, 0x47)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)


def set_cell_shading(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tc_pr.append(shd)


def add_horizontal_line(paragraph):
    p = paragraph._p
    p_pr = p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "1A1A2E")
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def setup_document(title_header):
    doc = Document()
    # A4 + marges 2,5 cm
    for section in doc.sections:
        section.page_height = Cm(29.7)
        section.page_width = Cm(21)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)
        section.header_distance = Cm(1.2)
        section.footer_distance = Cm(1.2)

        # Header
        header = section.header
        header_p = header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = header_p.add_run("LA MAISON DE LA CONFORMITÉ SARL  |  " + title_header)
        run.font.name = "Times New Roman"
        run.font.size = Pt(9)
        run.font.color.rgb = NAVY
        run.font.bold = True
        add_horizontal_line(header_p)

        # Footer
        footer = section.footer
        f1 = footer.paragraphs[0]
        f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = f1.add_run("LA MAISON DE LA CONFORMITÉ SARL")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(8)
        r1.font.bold = True
        r1.font.color.rgb = NAVY

        f2 = footer.add_paragraph()
        f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = f2.add_run("RCCM : CI-ABJ-03-2025-B13-10831  /  NCC : 2506426B  /  Capital : 1 000 000 FCFA")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(8)
        r2.font.color.rgb = DARK_GRAY

        f3 = footer.add_paragraph()
        f3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r3 = f3.add_run("Cel : 07 19 31 49 04  |  Email : lamaisondelaconformitesarl@outlook.com  |  www.lamaisondelaconformitesarl.net")
        r3.font.name = "Times New Roman"
        r3.font.size = Pt(8)
        r3.font.color.rgb = DARK_GRAY

    # Style par défaut
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(11)
    pf = style.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(6)
    return doc


def add_title(doc, text, size=14, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = color
    return p


def add_section_title(doc, text, size=12):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = NAVY
    return p


def add_body(doc, text, justify=True, bold=False, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = bold
    run.font.italic = italic
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.runs[0] if p.runs else p.add_run("")
    p.runs[0].text = ""
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    return p


def add_kv_table(doc, rows):
    table = doc.add_table(rows=len(rows), cols=2)
    table.autofit = False
    table.columns[0].width = Cm(4.5)
    table.columns[1].width = Cm(11.5)
    for i, (k, v) in enumerate(rows):
        c1 = table.cell(i, 0)
        c2 = table.cell(i, 1)
        c1.width = Cm(4.5)
        c2.width = Cm(11.5)
        for cell, txt, bold in ((c1, k, True), (c2, v, False)):
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(txt)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.bold = bold
            run.font.color.rgb = NAVY if bold else DARK_GRAY
    return table


def add_amount_table(doc, header, rows, total_label=None, total_value=None):
    n_cols = len(header)
    n_rows = 1 + len(rows) + (1 if total_label else 0)
    table = doc.add_table(rows=n_rows, cols=n_cols)
    table.style = "Light Grid Accent 1"
    # Header
    for j, h in enumerate(header):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(cell, "1A1A2E")
    # Body
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if j == n_cols - 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
        if i % 2 == 1:
            for j in range(n_cols):
                set_cell_shading(table.rows[i + 1].cells[j], "F4F4F4")
    # Total
    if total_label:
        row = table.rows[-1]
        c1 = row.cells[0]
        c1.text = ""
        p1 = c1.paragraphs[0]
        run1 = p1.add_run(total_label)
        run1.font.name = "Times New Roman"
        run1.font.size = Pt(11)
        run1.font.bold = True
        run1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(c1, "1A1A2E")
        # merge cells 0..n-2
        if n_cols > 2:
            merged = c1
            for k in range(1, n_cols - 1):
                merged = merged.merge(row.cells[k])
        cv = row.cells[-1]
        cv.text = ""
        pv = cv.paragraphs[0]
        pv.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        runv = pv.add_run(total_value)
        runv.font.name = "Times New Roman"
        runv.font.size = Pt(12)
        runv.font.bold = True
        runv.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(cv, "1A1A2E")
    return table


# ============================================================
# PROPOSITION FINANCIÈRE — TIM 7 MULTISERVICE
# ============================================================

def build_proposition_financiere():
    doc = setup_document("Proposition Financière — TIM 7 MULTISERVICE")

    add_title(doc, "PROPOSITION FINANCIÈRE", size=15, color=NAVY)
    add_title(doc, "MISSION DE MISE EN CONFORMITÉ DROIT DU TRAVAIL & PAIE", size=12, color=NAVY)
    add_title(doc, "TIM 7 MULTISERVICE", size=13, color=NAVY)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_horizontal_line(p)

    add_kv_table(doc, [
        ("Destinataire", "Direction Générale de TIM 7 MULTISERVICE"),
        ("À l'attention de", "Mme Fatoumata Zaharaye DIABY épouse KONÉ"),
        ("Référence", "MC-PROP-RESTO-2026-001"),
        ("Date", "Abidjan, le 1er mai 2026"),
        ("Objet", "Proposition financière — Mission d'accompagnement post-audit"),
        ("Validité", "30 jours"),
    ])

    doc.add_paragraph()

    # Section 1
    add_section_title(doc, "1. CONTEXTE ET RAPPEL DE LA MISSION")
    add_body(doc,
        "À la suite de l'audit juridique conduit par notre Cabinet sur les neuf (09) contrats de "
        "travail à durée indéterminée signés par TIM 7 MULTISERVICE entre juin et octobre 2025, plusieurs "
        "non-conformités majeures ont été relevées au regard de la Loi n° 2015-532 du 20 juillet 2015 "
        "portant Code du travail, de la Convention Collective Interprofessionnelle du 19 juillet 1977 et "
        "du Code de prévoyance sociale.")
    add_body(doc,
        "Le passif social latent estimé s'établit dans une fourchette de 15 à 25 millions de FCFA. "
        "Une intervention rapide est recommandée pour sécuriser la situation de la société avant tout "
        "contrôle de l'Inspection du Travail, de la CNPS ou de la DGI.")
    add_body(doc,
        "La présente proposition financière chiffre la mission d'accompagnement opérationnel proposée "
        "par MDC pour mettre en œuvre l'intégralité du plan d'action recommandé par le rapport d'audit.")

    # Section 2
    add_section_title(doc, "2. PÉRIMÈTRE DE LA MISSION — TROIS AXES")

    add_body(doc, "AXE 1 — RÉGULARISATION CONTRACTUELLE", bold=True)
    add_bullet(doc, "Personnalisation et finalisation des avenants pour chacun des 9 salariés (catégorie + échelon CCI 1977, ventilation salariale, clauses corrigées) ;")
    add_bullet(doc, "Adaptation et déploiement du modèle de contrat type CDI conforme pour les futurs recrutements ;")
    add_bullet(doc, "Élaboration et adoption d'un règlement intérieur conforme ;")
    add_bullet(doc, "Constitution d'un dossier individuel par salarié (contrat, CNI, certificat médical, fiche de poste, déclaration CNPS, lettres) ;")
    add_bullet(doc, "Organisation matérielle de la signature des avenants et accompagnement de la communication interne.")

    add_body(doc, "AXE 2 — MISE EN PLACE D'UNE PAIE CONFORME", bold=True)
    add_bullet(doc, "Paramétrage de la grille des salaires CCI 1977 (catégories, échelons, indices) ;")
    add_bullet(doc, "Calcul du salaire brut, des cotisations CNPS (salariée et patronale), de l'ITS, de la CN, du FDFP et de la taxe d'apprentissage ;")
    add_bullet(doc, "Mise en place d'un modèle de bulletin de paie conforme à l'article 31.8 du Code du travail ;")
    add_bullet(doc, "Production des bulletins de paie des trois (03) premiers mois et formation de la personne en charge à la maintenance ultérieure ;")
    add_bullet(doc, "Mise en place du calendrier des déclarations DISA mensuelles (CNPS) et des déclarations ITS / FDFP.")

    add_body(doc, "AXE 3 — SÉCURISATION SOCIALE ET FISCALE", bold=True)
    add_bullet(doc, "Vérification de l'immatriculation CNPS de TIM 7 MULTISERVICE et obtention/régularisation du numéro employeur ;")
    add_bullet(doc, "Affiliation des 9 salariés à la CNPS et obtention de leurs numéros d'immatriculation ;")
    add_bullet(doc, "Régularisation, le cas échéant, des déclarations DISA pour la période juin 2025 – avril 2026 ;")
    add_bullet(doc, "Déclaration nominative préalable des deux (02) salariés étrangers (Mlle Dossougouin et M. Atayi) auprès de l'AGEPE ;")
    add_bullet(doc, "Vérification de l'inscription à l'Inspection du Travail et dépôt du registre employeur ;")
    add_bullet(doc, "Préparation d'un dossier prêt à présenter en cas de contrôle (CNPS, DGI, Inspection du Travail).")

    # Section 3 — Tarifs
    add_section_title(doc, "3. PROPOSITION FINANCIÈRE")

    add_body(doc, "Les honoraires de la mission sont arrêtés sur une base forfaitaire, comme suit :")

    add_amount_table(
        doc,
        header=["Axe", "Prestation", "Honoraires (FCFA)"],
        rows=[
            ("Axe 1", "Régularisation contractuelle des 9 contrats + modèle type + règlement intérieur + dossiers individuels", "1 000 000"),
            ("Axe 2", "Mise en place d'une paie conforme (paramétrage + 3 mois de production + formation)", "1 200 000"),
            ("Axe 3", "Sécurisation sociale et fiscale (CNPS, AGEPE, Inspection du Travail, dossier de contrôle)", "800 000"),
        ],
        total_label="TOTAL FORFAITAIRE DE LA MISSION",
        total_value="3 000 000 FCFA",
    )

    doc.add_paragraph()

    add_body(doc,
        "Le Cabinet MDC n'est pas assujetti à la TVA. Les montants ci-dessus sont nets de toute taxe.",
        italic=True)

    # Tarif préférentiel global
    add_body(doc, "Tarif préférentiel global (mission complète sur les 3 axes) :", bold=True)
    add_body(doc,
        "Compte tenu de la mission d'audit déjà réalisée et de la souscription simultanée des trois axes, "
        "MDC consent à TIM 7 MULTISERVICE une remise commerciale de 500 000 FCFA, ramenant les honoraires "
        "forfaitaires globaux à 2 500 000 FCFA (deux millions cinq cent mille francs CFA).")

    # Conditions de paiement
    add_section_title(doc, "4. CONDITIONS DE PAIEMENT")
    add_body(doc, "Le règlement des honoraires est échelonné comme suit :")
    add_bullet(doc, "30 % à la signature du contrat de mission, soit 750 000 FCFA — déclencheur du démarrage des travaux ;")
    add_bullet(doc, "40 % à la signature des avenants par les 9 salariés (fin Axe 1), soit 1 000 000 FCFA ;")
    add_bullet(doc, "30 % à la livraison du dossier complet et du premier mois de paie conforme produit, soit 750 000 FCFA.")
    add_body(doc,
        "Tout paiement intervient dans un délai de 7 jours suivant la facture correspondante, par virement "
        "bancaire ou chèque. La mission ne saurait démarrer avant réception du premier acompte.")

    # Section 5 — Prestations supplémentaires
    add_section_title(doc, "5. PRESTATIONS COMPLÉMENTAIRES (sur devis)")
    add_bullet(doc, "Régularisation rétroactive des cotisations CNPS impayées : selon volume — devis spécifique après vérification des déclarations existantes ;")
    add_bullet(doc, "Représentation et accompagnement en cas de contrôle CNPS, DGI ou Inspection du Travail : 200 000 FCFA par séance ;")
    add_bullet(doc, "Rédaction d'un protocole transactionnel en cas de litige individuel : 250 000 FCFA par dossier ;")
    add_bullet(doc, "Audit social annuel de suivi : voir Proposition Commerciale séparée.")

    # Section 6 — Calendrier
    add_section_title(doc, "6. CALENDRIER PRÉVISIONNEL")
    add_amount_table(
        doc,
        header=["Phase", "Livrable", "Délai"],
        rows=[
            ("Démarrage", "Signature du contrat de mission + 1er acompte", "J0"),
            ("Phase 1", "Avenants personnalisés + règlement intérieur + dossiers individuels", "J0 + 21 jours"),
            ("Phase 2", "Signature effective des 9 avenants + facturation 2e tranche", "J0 + 30 jours"),
            ("Phase 3", "Paramétrage paie + production 1er bulletin de paie conforme", "J0 + 45 jours"),
            ("Phase 4", "Régularisation CNPS / AGEPE / Inspection du Travail", "J0 + 60 jours"),
            ("Clôture", "Livraison dossier final + facturation solde", "J0 + 90 jours"),
        ],
    )

    # Section 7 — Engagements
    add_section_title(doc, "7. ENGAGEMENTS DU CABINET")
    add_bullet(doc, "Confidentialité absolue sur l'ensemble des informations communiquées par TIM 7 MULTISERVICE ;")
    add_bullet(doc, "Mise à disposition d'une équipe pluridisciplinaire (juriste droit social, expert-comptable, fiscaliste) ;")
    add_bullet(doc, "Réactivité : réponse à toute sollicitation dans un délai maximum de 48 heures ;")
    add_bullet(doc, "Restitution finale en présentiel, accompagnée d'une note de synthèse pour la Direction Générale ;")
    add_bullet(doc, "Garantie de conformité : tout document produit par MDC est garanti conforme à la réglementation en vigueur à la date de sa rédaction.")

    # Section 8 — Prochaines étapes
    add_section_title(doc, "8. PROCHAINES ÉTAPES")
    add_bullet(doc, "Validation de la présente proposition par retour signé portant la mention « Bon pour accord » ;")
    add_bullet(doc, "Signature du contrat de mission ;")
    add_bullet(doc, "Versement du premier acompte ;")
    add_bullet(doc, "Démarrage des travaux dans la semaine suivante.")

    # Signature
    doc.add_paragraph()
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("Pour LA MAISON DE LA CONFORMITÉ SARL")
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.italic = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("M. BILE Fils Séverin")
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = NAVY

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("Gérant")
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.italic = True

    return doc


# ============================================================
# PROPOSITION COMMERCIALE — Suivi mensuel TIM 7
# ============================================================

def build_proposition_commerciale():
    doc = setup_document("Proposition Commerciale — TIM 7 MULTISERVICE")

    add_title(doc, "PROPOSITION COMMERCIALE", size=15, color=NAVY)
    add_title(doc, "CONSEIL FISCAL, SOCIAL ET STRATÉGIQUE", size=12, color=NAVY)
    add_title(doc, "TIM 7 MULTISERVICE", size=13, color=NAVY)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_horizontal_line(p)

    add_kv_table(doc, [
        ("Destinataire", "Direction Générale de TIM 7 MULTISERVICE"),
        ("À l'attention de", "Mme Fatoumata Zaharaye DIABY épouse KONÉ"),
        ("Référence", "MC-COM-RESTO-2026-001"),
        ("Date", "Abidjan, le 1er mai 2026"),
        ("Objet", "Proposition d'accompagnement mensuel — Suivi fiscal, social et conformité"),
        ("Validité", "30 jours"),
    ])

    doc.add_paragraph()

    # Intro
    add_section_title(doc, "CONTEXTE ET VALEUR PROPOSÉE")
    add_body(doc,
        "L'environnement réglementaire ivoirien s'est durci ces dernières années en matière de droit "
        "du travail, de cotisations sociales (CNPS) et de fiscalité salariale (ITS, FDFP, CN). Une PME "
        "du secteur de la restauration et du service traiteur, par la nature même de son activité "
        "(rotation de personnel, recours à des étrangers ressortissants CEDEAO, horaires atypiques, "
        "manipulation de denrées et hygiène) est particulièrement exposée à des contrôles de "
        "l'Inspection du Travail, de la CNPS ou de la DGI.")
    add_body(doc,
        "À l'issue de la mission de mise en conformité de vos contrats de travail, MDC vous propose "
        "un partenariat sur-mesure de suivi mensuel destiné à pérenniser le travail accompli, à "
        "anticiper les évolutions réglementaires et à sécuriser durablement TIM 7 MULTISERVICE.")

    # Section 1 — Mission de base
    add_section_title(doc, "1. MISSION DE BASE — SUIVI INTÉGRÉ FISCAL, SOCIAL & CONFORMITÉ")

    add_body(doc,
        "Objectif : garantir la conformité permanente de votre structure sur les plans fiscal, social "
        "et réglementaire, tout en identifiant systématiquement les opportunités d'optimisation.",
        italic=True)

    add_body(doc, "A. Domaine fiscal et comptable", bold=True)
    add_bullet(doc, "Veille réglementaire active sur les évolutions du Code Général des Impôts, du SYSCOHADA et des arrêtés sectoriels ;")
    add_bullet(doc, "Pilotage de la conformité déclarative mensuelle (TVA, ITS, FDFP, CN, taxes patronales) et annuelle (liasse fiscale, TEE, IBIC) ;")
    add_bullet(doc, "Audit préventif trimestriel et cartographie des risques fiscaux ;")
    add_bullet(doc, "Interface administrative avec la DGI (attestation de régularité fiscale, négociation d'échéanciers).")

    add_body(doc, "B. Domaine social et droit du travail", bold=True)
    add_bullet(doc, "Conformité sociale permanente : déclarations DISA mensuelles, suivi des cotisations CNPS (8 branches), DASC annuelle ;")
    add_bullet(doc, "Rédaction et adaptation des contrats de travail (CDI, CDD, stage) pour tout nouveau recrutement ;")
    add_bullet(doc, "Gestion des relations CNPS : immatriculations, contestations, attestations ;")
    add_bullet(doc, "Appui en cas de contrôle (Inspection du Travail, CNPS, AGEPE) — préparation, présence aux entretiens, rédaction des observations ;")
    add_bullet(doc, "Conseil sur la politique sociale (rémunération, primes, plan de formation FDFP, élections délégués du personnel).")

    add_body(doc, "C. Reporting stratégique", bold=True)
    add_bullet(doc, "Points d'étape trimestriels synthétisant la position fiscale, sociale, les risques identifiés et les pistes d'optimisation ;")
    add_bullet(doc, "Tableau de bord mensuel : effectifs, masse salariale, charges sociales, échéances fiscales à venir.")

    # Tarif principal
    doc.add_paragraph()
    add_amount_table(
        doc,
        header=["Mission de suivi mensuel", "Honoraires"],
        rows=[
            ("Suivi intégré fiscal, social et conformité — TIM 7 MULTISERVICE (effectif 9 à 15 salariés)", "150 000 FCFA / mois"),
        ],
    )

    doc.add_paragraph()
    add_body(doc,
        "Le Cabinet MDC n'est pas assujetti à la TVA. Le montant ci-dessus est net de toute taxe.",
        italic=True)
    add_body(doc,
        "Engagement contractuel : 12 mois renouvelable par tacite reconduction. "
        "Préavis de résiliation : 60 jours avant l'échéance.",
        italic=True)

    # Section 2 — Prestations supplémentaires
    add_section_title(doc, "2. PRESTATIONS SUPPLÉMENTAIRES (sur devis)")

    add_body(doc, "Domaine finance et stratégie", bold=True)
    add_bullet(doc, "Business plans, modélisations financières et études de rentabilité ;")
    add_bullet(doc, "Ingénierie de dossiers bancaires (financement BFR, équipements, expansion) ;")
    add_bullet(doc, "Diagnostics financiers spécialisés et rapports d'évaluation.")

    add_body(doc, "Domaine juridique, contractuel et social avancé", bold=True)
    add_bullet(doc, "Rédaction et négociation d'actes (baux commerciaux, conventions de prestation, contrats clients/fournisseurs) ;")
    add_bullet(doc, "Conseil en restructuration et gestion de licenciements collectifs ;")
    add_bullet(doc, "Gestion de contentieux social ou administratif (Tribunal du Travail, Inspection) ;")
    add_bullet(doc, "Audit social annuel complet (refacturé séparément à 800 000 FCFA).")

    # Section 3 — Conseil téléphonique
    add_section_title(doc, "3. CLAUSE DE CONSEIL TÉLÉPHONIQUE")
    add_bullet(doc, "Forfait mensuel inclus : 1 heure / mois (téléphone, WhatsApp, visioconférence) ;")
    add_bullet(doc, "Au-delà : 60 000 FCFA / heure, calculée au prorata réel ;")
    add_bullet(doc, "Traçabilité : récapitulatif mensuel des consultations communiqué avec la facture.")

    # Section 4 — Engagements
    add_section_title(doc, "4. NOS ENGAGEMENTS RÉCIPROQUES")

    add_body(doc, "Engagements de MDC", bold=True)
    add_bullet(doc, "Expertise pluridisciplinaire (droit social, fiscalité, comptabilité SYSCOHADA, conformité) ;")
    add_bullet(doc, "Secret professionnel absolu sur l'ensemble des informations transmises ;")
    add_bullet(doc, "Réactivité : réponse à toute sollicitation dans un délai maximum de 48 heures ouvrées ;")
    add_bullet(doc, "Transparence tarifaire : aucune prestation hors forfait sans accord écrit préalable ;")
    add_bullet(doc, "Garantie de conformité de tout document ou avis produit, dans les conditions et limites du droit applicable à la date de la prestation.")

    add_body(doc, "Engagement de TIM 7 MULTISERVICE", bold=True)
    add_body(doc,
        "La qualité et la sécurité de notre conseil reposent sur l'exhaustivité, l'exactitude et la "
        "fiabilité des informations que vous voudrez bien nous communiquer en temps utile. Nous vous "
        "demanderons en outre de désigner un interlocuteur unique pour fluidifier les échanges.")

    # Section 5 — Modalités de paiement
    add_section_title(doc, "5. MODALITÉS DE PAIEMENT")
    add_bullet(doc, "Facturation mensuelle, à terme à échoir (le 1er de chaque mois pour le mois en cours) ;")
    add_bullet(doc, "Délai de règlement : 7 jours suivant la facture ;")
    add_bullet(doc, "Mode de règlement : virement bancaire ou chèque libellé à l'ordre de LA MAISON DE LA CONFORMITÉ SARL.")

    # Section 6 — Souscription
    add_section_title(doc, "6. POUR ACCEPTER LA PRÉSENTE PROPOSITION")
    add_bullet(doc, "Signer le présent document avec la mention manuscrite « Bon pour accord » ;")
    add_bullet(doc, "Retourner un exemplaire signé par e-mail (lamaisondelaconformitesarl@outlook.com) ou par dépôt physique au cabinet ;")
    add_bullet(doc, "Versement de la première mensualité au démarrage du mois suivant.")

    # Signature
    doc.add_paragraph()
    doc.add_paragraph()
    sig_table = doc.add_table(rows=4, cols=2)
    sig_table.autofit = False
    sig_table.columns[0].width = Cm(7.5)
    sig_table.columns[1].width = Cm(7.5)

    cells = sig_table.rows[0].cells
    p = cells[0].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Pour LA MAISON DE LA CONFORMITÉ SARL")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p = cells[1].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Pour TIM 7 MULTISERVICE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = NAVY

    cells = sig_table.rows[1].cells
    for c in cells:
        for _ in range(3):
            c.add_paragraph()

    cells = sig_table.rows[2].cells
    p = cells[0].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("M. BILE Fils Séverin")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p = cells[1].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Mme Fatoumata Zaharaye DIABY épse KONÉ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    cells = sig_table.rows[3].cells
    p = cells[0].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Gérant")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    p = cells[1].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Directrice Générale")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    return doc


if __name__ == "__main__":
    base = "/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/TIM 7/AUDIT_CONTRATS_TRAVAIL"
    doc1 = build_proposition_financiere()
    p1 = f"{base}/05_PROPOSITION_FINANCIERE_TIM7.docx"
    doc1.save(p1)
    print(f"OK -> {p1}")

    doc2 = build_proposition_commerciale()
    p2 = f"{base}/06_PROPOSITION_COMMERCIALE_TIM7.docx"
    doc2.save(p2)
    print(f"OK -> {p2}")
