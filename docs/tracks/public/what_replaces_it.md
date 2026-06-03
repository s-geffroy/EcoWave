# Ce qui remplace les cycles

!!! info "Mise à jour V3 (juin 2026) — page recadrée comme *complément*, pas substitut"

    En V3, le verdict s'est affiné : la lecture **universaliste** des cycles est rejetée, mais **trois cycles substantifs sont vindiqués** sur leurs canaux propres. Le cluster des 5 propriétés ci-dessous est donc à lire comme **signature complémentaire** qui co-existe avec les trois cycles vindiqués (Juglar, Kuznets, Kitchin), pas comme leur substitut. Le projet a désormais deux papiers en parallèle : *Cycles Refuted V3* (publié, vindication variable-spécifique + Kondratieff recasté Reinhart-Rogoff) et un *companion paper en préparation* (cluster CBDIS + benchmark PASS 78 %). Voir [résumé V3](../../papers/cycles_refuted_v3.md).

!!! success "TL;DR"

    À côté des trois cycles substantifs vindiqués, **5 propriétés statistiques** apparaissent **dans la plupart** des séries macro : **C** longue mémoire (les chocs s'éteignent lentement, comme dans un fleuve, pas un étang) ; **B** multifractalité (la texture des fluctuations diffère selon l'échelle, comme une côte rocheuse vue d'avion vs à pied) ; **D** non-linéarité (cause et effet ne sont pas proportionnels) ; **I** information structurée (prédictibilité partielle exploitable) ; **S** dérive de régime cognitif (les croyances changent le système — Soros). Métaphore unificatrice : la **cascade en turbulence**.

## Dans cette page

- **[Cinq propriétés](#cinq-proprietes)** — C, B, D, I, S détaillées
- **[Une métaphore : la cascade](#cascade)** — turbulence K41
- **[Pourquoi le cycle ne fonctionnait pas](#pourquoi)** — 3 raisons
- **[La conséquence opérationnelle](#operationnel)** — modèles cascade

---

## Cinq propriétés qui apparaissent partout { #cinq-proprietes }

Quand les quatre cycles canoniques ont été éliminés par notre
protocole, il restait quelque chose dans les séries macroéconomiques.
Quelque chose de bien *plus* structuré qu'un simple bruit aléatoire.
Pour le caractériser, nous avons appliqué quatorze diagnostics
statistiques différents sur les mêmes 6 panels — diagnostics issus de
la physique statistique, de la théorie de l'information, et de
l'économétrie moderne.

Cinq propriétés ressortent comme stables, présentes systématiquement,
et conjointes (elles n'apparaissent jamais isolées). Nous les appelons
le **cluster C+B+D+I+S**.

### C — Longue mémoire

Imaginez que vous lancez une pierre dans un étang. Les vagues qu'elle
crée s'estompent en quelques secondes. C'est de la **mémoire courte** :
l'effet de la perturbation s'oublie vite.

Maintenant imaginez un fleuve. Une crue à la source aujourd'hui aura
encore des effets à l'embouchure dans plusieurs jours, voire des
semaines. Le système "se souvient" du choc pendant longtemps. C'est de
la **mémoire longue**.

Les séries macroéconomiques se comportent comme le fleuve. Un choc
d'inflation, de crédit, de chômage qui survient aujourd'hui aura encore
des effets mesurables dans dix, vingt, trente ans. Ce n'est pas une
métaphore : c'est quantifiable. Notre paramètre s'appelle `d` (pour
"degré d'intégration fractionnaire") et il mesure exactement à quelle
vitesse les chocs s'estompent. Pour la plupart des séries macro
testées, `d` est positif et significatif — donc longue mémoire.

### B — Multifractalité

Si vous zoomez sur une côte rocheuse vue d'avion, vous voyez les
mêmes formes de découpures qu'à pied. Cette propriété s'appelle
l'**auto-similarité**. Mais elle a deux variantes : la *monofractalité*
(toutes les échelles se ressemblent de la même manière), et la
**multifractalité** (chaque échelle a sa propre dimension).

Le marché boursier est connu pour être multifractal depuis Mandelbrot
des années 1960 : les "petites" fluctuations quotidiennes et les
"grandes" fluctuations mensuelles ne sont pas juste des versions
agrandies les unes des autres — elles ont des propriétés statistiques
**qualitativement différentes**.

Nous démontrons que la macroéconomie a la même propriété. Une crise
violente sur six mois n'est pas la même chose que dix crises légères
étalées sur cinq ans, même si le mouvement total est identique. La
**texture** des fluctuations diffère.

### D — Non-linéarité

Dans un système linéaire, la cause et l'effet sont proportionnels.
Doublez le choc, l'effet double. Ajoutez deux chocs, leurs effets
s'additionnent.

Dans un système non-linéaire, ce n'est plus vrai. Un choc deux fois plus
grand peut produire un effet dix fois plus grand. Deux chocs ensemble
peuvent s'annuler ou se renforcer mutuellement de façon imprévisible.

La macroéconomie est non-linéaire. Notre test statistique (BDS, du nom
de Brock-Dechert-Scheinkman 1996) le confirme sur la quasi-totalité des
cellules. Pratiquement : **on ne peut pas additionner des effets pour
faire une prévision**. Un modèle DSGE qui suppose la linéarité
intertemporelle rate cette propriété — et donc rate les retournements
brutaux.

### I — Information structurée

L'entropie mesure la quantité d'information aléatoire dans une série.
Une suite purement chaotique a une entropie maximale ; une suite très
prévisible (croissance constante par exemple) a une entropie minimale.

Les séries macroéconomiques sont **partiellement prévisibles** — mais
seulement dans des fenêtres temporelles particulières et avec des
contraintes structurelles précises. Notre diagnostic d'**entropie
permutationnelle** (et de **sample entropy**) montre que l'information
contenue dans la série n'est pas un pur bruit : elle a une structure
qui peut être exploitée.

C'est bonne nouvelle pour la prévision opérationnelle : il y a quelque
chose à prévoir. C'est mauvaise nouvelle pour les modèles qui supposent
que les fluctuations sont aléatoires : ils ratent cette structure.

### S — Dérive de régime cognitif

Cette propriété est la plus subtile. Quand les acteurs économiques
changent leurs croyances sur le fonctionnement du système — par
exemple : "la Banque centrale ne tolérera plus l'inflation" en 1979 avec
Volcker, ou "le QE va durer pour toujours" en 2009 — le système lui-
même change de régime.

C'est ce que George Soros appelle la **réflexivité** : les croyances sur
le système font partie du système. Le système n'est pas extérieur à
nous comme l'atmosphère est extérieure à un météorologue ; il *est*
partiellement constitué par nos anticipations.

Notre test détecte ces changements de régime via une statistique de
Kolmogorov-Smirnov appliquée à des fenêtres glissantes. Les
changements détectés correspondent souvent à des événements historiques
identifiables (Volcker, Black Monday 1987, GFC 2008, COVID 2020).

## Une métaphore : la cascade { #cascade }

Comment se représenter le tout ? L'image utile est celle d'une
**cascade en turbulence**.

Imaginez l'eau qui dégringole d'une chute. Au sommet, le flux est
relativement régulier. À mi-chute, il s'agite et forme des grandes
vagues. Vers le bas, ces vagues se brisent en mille tourbillons de plus
en plus petits. C'est la cascade de Kolmogorov, l'image canonique de la
turbulence en physique.

La macroéconomie ressemble à cela. Les *grandes* perturbations
historiques (révolutions industrielles, deux guerres mondiales,
construction de l'État-providence) jouent le rôle des grandes vagues
en haut. Elles se déclinent en cascades de perturbations plus petites
(cycles d'investissement, fluctuations sectorielles), elles-mêmes
déclinées en perturbations encore plus petites (variations
trimestrielles, ajustements de stocks). Et il y a un véritable
**transfert d'énergie** des grandes échelles vers les petites — ce
qu'exprime mathématiquement notre multifractalité.

Ce qui change la métaphore par rapport à la turbulence physique pure :
le système a aussi des **régimes cognitifs**. Comme si, de temps en
temps, la physique elle-même de la cascade changeait — parce que les
acteurs économiques changent leurs croyances sur le système.

## Pourquoi le cycle ne fonctionnait pas { #pourquoi }

L'image cyclique implique trois choses : une **fréquence privilégiée**,
une **forme reproductible**, et une **horloge** qui régule. Aucune de
ces trois choses n'est présente dans nos données.

- Pas de fréquence privilégiée : le spectre de puissance est
  *continu*, pas pointu.
- Pas de forme reproductible : la multifractalité (B) signifie
  précisément que chaque "cycle" est de nature différente.
- Pas d'horloge : la dérive de régime cognitif (S) brise toute
  régularité temporelle.

Le cycle est mort parce que la macroéconomie n'a pas d'horloge interne.
Elle a quelque chose de plus intéressant : une **cascade fractale avec
dérive cognitive**.

## La conséquence opérationnelle { #operationnel }

Si la macroéconomie est une cascade plutôt qu'une horloge, on peut
**la modéliser**, et donc la **prévoir**. Pas avec des modèles
cycliques, mais avec des modèles de cascade : MSM (Markov-Switching
Multifractal de Calvet-Fisher), ARFIMA + régime-switching (Bhardwaj-
Swanson), HAR (Heterogeneous Autoregressive de Corsi).

Nous avons testé ces modèles contre random walk (le modèle "bête" qui
dit que demain ressemble à aujourd'hui) sur 68 variables macro. Verdict :
**78 % de victoires** pour les modèles cascade.

C'est ce que la page suivante explique : [Pourquoi ça compte](why_it_matters.md).
