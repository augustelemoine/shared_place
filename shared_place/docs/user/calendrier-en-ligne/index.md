<!-- add-breadcrumbs -->
## Le calendrier en ligne

L'application Tiers Lieux propose un outil de réservation de salles/ressources basé sur un calendrier en ligne accessible depuis le site e-commerce d'ERPNext.

Cet outil fonctionne en lien avec la fonctionnalité de site e-commerce d'ERPNext.

### Configuration du site e-commerce

Chaque article sont liés à un groupe d'article et celui-ci doit être autorisé sur le site web pour que les articles liés soient visibles également:

1. Allez dans les groupes d'articles qui doivent être affichés sur le site web et cochez "Show in Website"
<img src="/shared_place/assets/item_group_config.png" class="screenshot">

2. Allez dans les articles liés aux salles/espaces de coworking/ressources et cochez "Show in Website"
<img src="/shared_place/assets/item_config.png" class="screenshot">

__Attention__: ERPNext génère automatiquement une URL sur le site web dans le champ "route".
Cette URL ne doit contenir aucun accent. Vous pouvez la modifier pour supprimer les accents si nécessaires.

3. Dans les paramètres du panier, activez l'achat d'articles via le site web
  Vous pouvez activer la caisse si vous souhaitez que les utilisateurs paient depuis le site e-commerce.

4. Vous pouvez ajouter une nouvelle section dans la barre supérieure de votre site pour faciliter la navigation.
<img src="/shared_place/assets/website_config.png" class="screenshot">

5. Vous pouvez également ajouter des articles sur la page d'accueil de votre site dans le document "Page d'accueil"
<img src="/shared_place/assets/homepage_config.png" class="screenshot">


### Utilisation du calendrier

Sur le site e-commerce, chaque utilisateur peut sélectionner un article.
Si cet article est lié à une ou plusieurs salles/ressources/espaces de coworking, il est alors directement redirigé vers le calendrier:
<img src="/shared_place/assets/homepage_selection.gif" class="screenshot">

**Etape 1**
Il doit alors choisir entre l'une des unités de mesure proposées (voir la section configuration).

Les salles/ressources/espaces de coworking correspondants à cet article sont alors mis en évidence en bleu.

**Etape 2**
Il peut ensuite sélectionner le créneau qui lui convient dans le calendrier.

Une fenêtre s'ouvre alors avec plusieurs options:
<img src="/shared_place/assets/slot_selection.png" class="screenshot">

**Etape 3**
Cette fenêtre permet de voir le prix associé au créneau sélectionné.
En ajoutant un créneau, l'horaire de fin de réservation peut être modifié. Il est ainsi possible de réserver plusieurs créneaux consécutifs.

Enfin, si certaines salles ou espaces de coworking proposent des options, celles-ci sont sélectionnables et permettent de recalculer également le prix.

Lorsque l'utilisateur a sélectionné toutes ses options, il peut cliquer sur "Ajouter au panier".

**Etape 4**
Le créneau est ajouté au panier. Il est toujours possible de le supprimer en cas d'erreur.
__Attention__: Seule la suppression de tous les créneaux liés à un article est possible.

Le panier sera automatiquement réinitialisé au bout de la durée définie dans les paramètres de l'application "Tiers Lieux".

**Etape 5**
L'utilisateur peut valider son panier en cliquant sur "Passer la commande".
A ce stade, l'annulation n'est plus possible et l'utilisateur peut voir le bon de commande correspondant à sa réservation.

Il peut également voir les réservations qu'il a faite dans son compte, sous la rubrique "Réservations".


**Alternative**
Si l'utilisateur souhaite acheter des unités sans sélectionner de créneau spécifique, il peut cliquer sur le bouton "Acheter des unités sans sélectionner un créneau" sous le calendrier pour être redirigé vers l'interface d'achat classique d'ERPNext.
<img src="/shared_place/assets/buy_units.png" class="screenshot">

L'unité de vente est celle définie dans les paramètres de vente de l'article.

<!-- markdown -->