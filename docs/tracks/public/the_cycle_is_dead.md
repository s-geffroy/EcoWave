# Le cycle est mort

!!! warning "Mise à jour V3 (juin 2026) — titre partiellement obsolète"

    Le **titre de cette page reste mais le verdict est nuancé**. Ce qui est mort, c'est la **lecture universaliste** : « un seul cycle canonique pour toutes les variables macro ». Le V3 du papier *Cycles Refuted* (juin 2026) montre que **trois cycles sont au contraire vivants** sur exactement les variables que leur théorie prédit (Juglar sur investissement-PIB et chômage ; Kuznets sur prix immobiliers, population et crédit ; Kitchin sur agrégats crédit marchés émergents). **Kondratieff est recasté** comme chronologie de dette de guerre Reinhart-Rogoff plutôt que comme long-wave endogène. Voir [résumé V3](../../papers/cycles_refuted_v3.md). La page est conservée pour préserver les permaliens et pour son contexte pédagogique sur ce qui *est* effectivement mort (la lecture universaliste).

!!! success "TL;DR — version V3"

    Depuis 1923, les manuels d'économie enseignent **4 cycles canoniques** : Kitchin (3-5 ans), Juglar (7-11 ans), Kuznets (15-25 ans), Kondratieff (40-60 ans). Pendant un siècle, ils ont été présentés comme **universels** — un même cycle pour toutes les variables. Notre protocole V3 (5 panels indépendants, 1 456 cellules, dual null AR(1)+ARFIMA) montre que cette lecture **universaliste est rejetée** par Benjamini-Hochberg FDR, mais que les trois premiers cycles **vivent bel et bien** sur les variables que leur théorie d'origine prédit (et seulement celles-là) — et Kondratieff devient une chronologie de **dette de guerre** plutôt qu'une long-wave endogène.

## Dans cette page

- **[L'enseignement officiel](#enseignement)** — les 4 cycles canoniques
- **[Le problème](#probleme)** — pas de test statistique original
- **[Notre protocole : 3 portes](#protocole)** — la démarche conservatrice
- **[Le résultat](#resultat)** — 0 / 9 436 cellules
- **[Pourquoi cette démolition est utile](#utilite)**

---

## L'enseignement officiel { #enseignement }

Si vous avez ouvert un manuel d'économie, vous y avez croisé les quatre
cycles canoniques. C'est l'un des rares contenus que tous les
programmes d'enseignement de l'économie répètent — du lycée au master,
en Europe comme aux États-Unis, dans les manuels néoclassiques comme
dans les manuels hétérodoxes.

- **Joseph Kitchin** (1923) — un cycle court de 3 à 5 ans, qu'il a
  observé dans les commandes de wagons aux États-Unis et au Royaume-
  Uni. Inventaires.
- **Clément Juglar** (1862) — un cycle moyen de 7 à 11 ans, lié au
  crédit, à l'investissement, et aux retournements bancaires.
- **Simon Kuznets** (1930) — un cycle long de 15 à 25 ans, observé dans
  les statistiques de construction immobilière et d'immigration.
- **Nikolaï Kondratieff** (1925, exécuté en 1938 par Staline pour cette
  recherche) — un super-cycle de 40 à 60 ans, qu'il rattachait aux
  grandes vagues technologiques.

L'image est belle, presque mécanique. La macroéconomie ressemblerait à
une grande horloge à quatre engrenages emboîtés, chacun tournant à
sa vitesse, et leurs combinaisons expliqueraient les retournements
historiques.

C'est ce qu'on enseigne. Sauf que **ce n'est pas vrai**.

## Le problème avec les cycles canoniques { #probleme }

Aucun de ces auteurs n'a jamais publié, à sa propre époque, un *test
statistique* de l'existence de son cycle. Tous ont raisonné en
*reconnaissance de forme* sur des courbes — une démarche utile pour
formuler une hypothèse, mais qui ne peut pas la valider.

Quand on regarde de près une série économique, on voit toujours des
fluctuations. La question n'est pas "y a-t-il des montées et des
descentes ?" — la réponse est trivialement oui. La question est : "ces
fluctuations sont-elles **organisées** autour de fréquences
particulières, ou bien sont-elles le sous-produit d'un processus
**stochastique** qui n'a pas d'horloge interne ?"

Pour répondre à cette question, il faut construire un *test*. Un test
qui propose deux hypothèses concurrentes :

- **H₀** : la série est compatible avec un bruit aléatoire structuré,
  sans cycle particulier.
- **H₁** : la série porte un cycle réel à une fréquence donnée.

Et qui permet de **rejeter H₀** seulement quand l'évidence est
suffisamment forte.

C'est exactement la démarche d'un essai clinique : on ne déclare pas
qu'un médicament fonctionne parce qu'on a vu trois patients aller mieux.
On compare à un placebo, on contrôle les biais, on calcule des
probabilités. La macroéconomie a longtemps fait sans cette discipline.

## Notre protocole : trois portes de falsifiabilité { #protocole }

Le projet CPV applique trois tests successifs sur chaque cycle candidat,
sur chaque série économique, sur chaque ensemble de pays. Ces trois
portes sont conçues pour être **conservatrices** : il faut les passer
toutes trois pour qu'un cycle soit déclaré "réel".

### Porte 1 — Le double null

On simule mille séries fictives qui ressemblent à la série observée
*par les propriétés que l'œil détecte*, mais sans cycle interne. Si la
série observée ne se distingue pas significativement de ces simulations,
le cycle proposé n'est qu'une coïncidence visuelle.

On utilise *deux* nulls indépendants :

- **AR(1) bootstrap** — Simule des séries qui ont la même variance et
  la même persistance (autocorrelation à un pas) que la série observée.
- **Phase-scramble** — Simule des séries qui ont le même spectre de
  puissance que la série observée mais des phases aléatoires.

Une cellule passe la Porte 1 seulement si **les deux** nulls la rejettent.

### Porte 2 — Le consensus de quatre méthodes

Quatre méthodes statistiques très différentes votent indépendamment sur
la phase actuelle de chaque cycle : PELT (segmentation par
changement de points), Markov-switching (Hamilton 1989), Christiano-
Fitzgerald + Hilbert (analyse spectrale + phase instantanée), Bry-
Boschan (turning points). Une cellule passe la Porte 2 seulement si
**au moins 3 sur 4** s'accordent.

L'idée est simple : un cycle vraiment présent doit être détectable par
des méthodes aux hypothèses paramétriques différentes. Un cycle qui
n'émerge qu'avec **une seule** méthode est sans doute un artefact de
cette méthode.

### Porte 3 — L'universalité

Un vrai cycle macroéconomique doit se manifester de la même façon dans
au moins quatre agrégats de pays sur cinq (mondial, pays à haut revenu,
pays à revenu intermédiaire supérieur, pays à revenu intermédiaire
inférieur, pays à faible revenu). Si le cycle n'apparaît que pour les
pays à haut revenu, ce n'est pas un cycle global — c'est un cycle local.

## Le résultat { #resultat }

Sur six panels macroéconomiques couvrant la période **1700 à 2024** :

- 65 ans de données de la Banque mondiale (1960–2024)
- 30 ans de données trimestrielles (1995–2024)
- 154 ans d'histoire longue (Maddison + Jordà-Schularick-Taylor,
  1870–2024)
- 316 ans de données monétaires britanniques (Bank of England
  Millennium, 1700–2016)
- 54 ans de données macroprudentielles BIS (1970–2024)
- 60 ans de données sectorielles (FRED + Our World in Data + BEIS)

Total : **9 436 cellules diagnostiques** testées rigoureusement.

**Aucun des quatre cycles canoniques ne survit aux trois portes.**

Plus précisément : la quasi-totalité des cellules échoue dès la Porte 1
(dual null). Les rares qui survivent à la Porte 1 échouent à la Porte 2.
Aucune ne passe les trois. Les datations pédagogiques (Korotayev-Tsirel
2010 pour Kondratieff par exemple) ne survivent pas non plus.

## Mais alors, qu'observe-t-on dans les séries ?

C'est ici que l'histoire devient intéressante. **Les séries
macroéconomiques ne sont pas du bruit blanc** — elles ont de la
structure, beaucoup de structure. Mais cette structure n'est pas
*cyclique*. Elle est de nature très différente.

Continuons sur la page suivante : [Ce qui remplace les
cycles](what_replaces_it.md).

## Pourquoi cette démolition est-elle utile ? { #utilite }

Démontrer que les quatre cycles canoniques sont morts ne suffit pas à
construire quelque chose de neuf. Mais c'est une **étape nécessaire** :
tant qu'on enseigne et qu'on modélise comme si Kitchin/Juglar/Kuznets/
Kondratieff étaient des lois physiques, on cherche au mauvais endroit
les explications des crises, des cycles de crédit, des grandes
transformations.

Notre travail montre qu'il **faut chercher ailleurs**. La page suivante
explique où.

---

!!! info "Pour les sceptiques"

    La procédure complète, le code Python, les données, les sidecars
    JSON : tout est public sur [GitHub](https://github.com/s-geffroy/EcoWave)
    et reproductible en une commande Docker. Si vous pensez que nous
    avons commis une erreur méthodologique, le code vous attend.
    Pour le détail technique, voir le [track académique](../acad/index.md)
    et la [méthode](../../methodology/protocole_cpv.md).
