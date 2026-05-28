# Trois portes de falsifiabilité

> **Résumé.** Une phase n'est publiée pour une cellule (agrégat, cycle,
> mois) que si **les trois portes** réussissent : existence du cycle dans
> les données (Porte 1), consensus inter-méthode (Porte 2), universalité
> cross-groupes (Porte 3). Les échecs sont publiés explicitement
> (`rejected` / `disputed` / `regional`) plutôt que dissimulés — c'est ce
> qui distingue le protocole CPV de la littérature classique sur les
> vagues longues.

## Notation

| Symbole | Sens |
|---|---|
| $H_0$ | Hypothèse nulle : la bande ne porte pas de puissance distincte d'un bruit AR(1) + phase scramble |
| $H_1$ | Hypothèse alternative : un cycle de la bande est présent |
| $\alpha$ | Seuil de rejet du null ($\alpha = 0.05$) |
| $p_{\text{dual}}$ | $p$-value combinée du null dual (max des deux $p$-values individuelles) |
| $m$ | Nombre de méthodes votantes ($m = 4$) |
| $k$ | Nombre minimum d'accord pour la Porte 2 ($k = 3$) |
| $n$ | Nombre de groupes de revenu pour la Porte 3 ($n = 5$) |
| $q$ | Nombre minimum d'accord cross-groupes ($q = 4$) |

## Porte 1 — existence du cycle

**Énoncé du test.** $H_0$ : la puissance dans la bande $[\text{lo}, \text{hi}]$
est compatible avec un null conservatif combinant (a) un AR(1) ajusté sur la
série (moyenne, variance, persistance) et (b) un scramble de phase préservant
le spectre ([Theiler *et al.*, 1992](../bibliographie.md#theiler-et-al-1992)).

**Critère de décision.** $p_{\text{dual}} < \alpha = 0.05$ → la cellule
passe la Porte 1 et procède à la Porte 2. Sinon : `phase = rejected`,
`separable = 0`, `ar1_p_value = p_dual`.

**Implémentation.** `ecowave/cycles/surrogate.py:dual_null` avec $B = 1\,000$
surrogates par défaut.

**Source.** [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998) ;
[Grinsted *et al.* (2004)](../bibliographie.md#grinsted-moore-jevrejeva-2004) ;
[Theiler *et al.* (1992)](../bibliographie.md#theiler-et-al-1992).

## Porte 2 — consensus inter-méthode

**Énoncé du test.** Au moins $k = 3$ méthodes parmi $\{D, E, F, G\}$ doivent
voter la **même** étiquette de phase :

- **F** — CF band-pass + phase de Hilbert ([Christiano & Fitzgerald, 2003](../bibliographie.md#christiano-fitzgerald-2003))
- **G** — Datation Bry-Boschan ([Harding & Pagan, 2002](../bibliographie.md#harding-pagan-2002))
- **E** — Markov-switching AR(1) ([Hamilton, 1989](../bibliographie.md#hamilton-1989))
- **D** — Ruptures PELT ([Killick *et al.*, 2012](../bibliographie.md#killick-fearnhead-eckley-2012))

**Critère de décision.** Si l'étiquette modale rassemble $\geq 3$ votes :
phase publiée. Si la modale ne rassemble que 2 votes : `phase = disputed`.
Le **désaccord est publié explicitement** dans `cycle_consensus`, jamais
résolu en choisissant une méthode « amicale ».

**Implémentation.** `ecowave/cycles/consensus.py:compute_phase_consensus`.

**Justification.** Les quatre méthodes incarnent des hypothèses génératives
très hétérogènes (filtre fréquentiel vs deux régimes Markov vs ruptures de
moyenne vs détection de retournements). Un accord à 3/4 implique qu'aucun
artéfact méthodologique unique ne pilote le résultat.

## Porte 3 — universalité cross-groupes

**Énoncé du test.** Pour chaque cycle et chaque mois `as_of`, le cycle est
qualifié `universal` seulement si $\geq q = 4$ agrégats de revenu sur
$n = 5$ (WLD + HIC + UMC + LMC + LIC) partagent la même phase modale.

**Critère de décision.** Si $\geq 4 / 5$ accordent : flag `universal = 1`.
Sinon : `universal = 0` ; le cycle est qualifié `regional / idiosyncratic`
et la liste des groupes concordants est publiée dans `cycle_universality.notes`.

**Implémentation.** `ecowave/cycles/universality.py:compute_cross_group_concordance`.

**Justification.** Transpose le critère C6 de transférabilité (EcoWave
historique) de la dimension temporelle à la dimension de stratification de
revenu. Un cycle global doit s'imposer indépendamment du niveau de
développement ; un cycle qui n'existe que pour HIC est `regional`.

## Autres contraintes (toujours pré-enregistrées)

- **Endpoint caveat.** Toute cellule dont le dernier point de données est à
  moins de $\lfloor \text{hi\_years}/2 \rfloor$ du bord du panel est marquée
  `endpoint_caveat = 1`. La phase est tout de même publiée mais le lecteur
  est explicitement averti que le filtre CF est instable à la frontière.
- **Adéquation de fréquence.** Les données WB sont annuelles ; Kitchin
  (3–5 ans) est borderline ; la borne basse (3 ans) est sous le seuil de
  Nyquist annuel. Le protocole pré-enregistre Kitchin uniquement sur la
  bande haute 4–5 ans ; l'upsample trimestriel (spline) est une variante
  de sensibilité, jamais le défaut.
- **Small-N Kondratieff.** Les séries WB commencent en 1960 (~65 ans, soit
  $\approx 1.0$–$1.5$ K-wave). La Porte 1 rejette fréquemment Kondratieff
  pour les agrégats à historique court ; c'est publié `separable = 0`, non
  réinterprété comme un signal caché.
- **Pas de cherry-picking de bande.** Les bornes des bandes sont figées
  dans `ecowave/cycles/bands.py:CYCLE_BANDS` et ne sont jamais ajustées
  agrégat par agrégat.

## Échelle de verdict

| Verdict | Porte 1 | Porte 2 | Porte 3 | Phase publiée |
|---|---|---|---|---|
| **A** | ✓ | ✓ (4/4 d'accord) | ✓ (universal) | étiquette modale |
| **B** | ✓ | ✓ (3/4 d'accord) | ✓ | étiquette modale + dissident noté |
| **C** | ✓ | ✗ (`disputed`) ou ✓ + Porte 3 ✗ | — | cellule rapportée, verdict qualifié |
| **D** | ✗ | — | — | `rejected` (échec honnête) |

## Caveats

La discipline de pré-enregistrement implique que les bornes, méthodes et
seuils ci-dessus sont gelés ; toute modification ouvre la suspicion
d'ajustement *post hoc* aux données. Les modifications passées sont tracées
dans [Feuille de route](feuille_de_route.md) et dans l'historique git.

## Références

- [Christiano & Fitzgerald (2003)](../bibliographie.md#christiano-fitzgerald-2003)
- [Grinsted, Moore & Jevrejeva (2004)](../bibliographie.md#grinsted-moore-jevrejeva-2004)
- [Hamilton (1989)](../bibliographie.md#hamilton-1989)
- [Harding & Pagan (2002)](../bibliographie.md#harding-pagan-2002)
- [Killick, Fearnhead & Eckley (2012)](../bibliographie.md#killick-fearnhead-eckley-2012)
- [Theiler *et al.* (1992)](../bibliographie.md#theiler-et-al-1992)
- [Torrence & Compo (1998)](../bibliographie.md#torrence-compo-1998)
