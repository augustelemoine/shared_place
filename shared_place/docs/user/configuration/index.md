<!-- add-breadcrumbs -->
# Configuration

Afin de pouvoir proposer des créneaux de réservation en ligne, il est nécessaire de configurer correctement les différentes salles/ressources disponibles ainsi que les données de facturation qui leur sont associées.

## Application Tiers Lieux

L'application Tiers Lieux est composé d'un module principal, dénommé Tiers Lieux (Shared Place en version anglophone).  
Cette application est à son tour composé d'un module également dénommé Tiers Lieux.  
Celui-ci contient les DocTypes suivants, utilisés pour la configuration et la gestion des réservations:

### Paramètres (Shared Place Settings)

Les paramètres permettent de définir des valeurs par défaut applicables au calendrier visible par les utilisateurs et aux différents documents de l'application Tiers Lieux.  

**Paramètrage du calendrier**  
- Un texte d'aide affiché au dessus du calendrier 
- Une période limite de réservation  
  Exemple: si celle-ci est de 14 jours, les utilisateurs ne pourront pas faire de réservations au delà de 14 jours après aujourd'hui. 
-  
- La possibilité d'autoriser ou non les réservations le week-end  
- Une heure de début et une heure de fin du calendrier  
  Le calendrier ne permettra pas de voir les heures avant/après ces deux paramètres.  

**Paramètrage des unités de mesure**

Pour simplifier le paramétrage du calendrier, l'application permet de définir une unité de mesure par défaut (dans la plupart des cas l'"Heure") et d'ajouter les unités de mesure "Demi-journée" et "Journée" si besoin.  
Chaque unité de mesure dispose de son propre calendrier de réservation par défaut.  

__Calendrier de réservation par défaut__

C'est le calendrier standard de votre Tiers Lieux. Ajoutez-y les créneaux pendant lesquels les réservations sur votre plateforme peuvent être ouverts.  
<img src="/docs/assets/default_calendar.png" class="screenshot">

Choisissez ensuite l'unité de mesure par défaut pour vos réservations. Dans 99% des cas il s'agira de l'unité "Heure".  
Vous pouvez également créer une nouvelle unité de mesure si celle-ci n'existe pas.  

Puis définissez la durée de cette unité de mesure. Attention cette durée peut-être un nombre réel, mais doit être en heures.  

__Réservation à la demi-journée/journée__

Si vous souhaitez autoriser également les réservations à la demi-journée ou à la journée, cochez l'option correspondante et ajoutez un les créneaux correspondants aux demi-journées ou aux journée dans le calendrier.  
Sélectionnez également l'unité de mesure correspondant à chaque option.  
<img src="/docs/assets/half_day_calendar.png" class="screenshot">
  

### Salle (Shared Place Room)

Une salle est un espace privatisable, loué à un seul utilisateur (ou groupe d'utilisateurs).  

Chaque salle a un nom spécifique et est liée au minimum à un article et à une liste de prix.
La combinaison article/liste de prix/unité de mesure permet à ERPNext de calculer le prix à facturer.  

Il est donc primordial de bien penser à ajouter des prix pour chaque unité de mesure dans la liste de prix sélectionnée.
Vous pouvez également voir les prix correspondants à votre salle en cliquant sur le bouton "voir les prix liés".  

Vous avez également la possibilité de définir plusieurs options, chaque option étant liée à un article spécifique et donc à un prix spécifique.
Exemple: Vous voulez définir des prix différents en fonction du nombre de personnes réservant la salle, vous pouvez ajouter deux lignes correspondant à vos deux options de facturation.  
<img src="/docs/assets/room_options.png" class="screenshot">  


Une fois vos articles sélectionnés et vos prix ajoutés, vous pouvez ouvrir votre salle à la réservation.
Si celle-ci suit un calendrier différent du calendrier standard configuré dans les paramètres, créez un calendrier spécifique.
Ceci est valable pour l'unité de mesure par défaut uniquement.

Pour les demi-journées et les journées, le calendrier utilisé sera toujours celui configuré dans les paramètres.


### Ressource (Shared Place Resource)

Une ressource est un élément loué avec une salle ou indépendemment (Machine, imprimante, etc...)  

La configuration d'une ressource est similaire à celle d'une salle et suit les même règles.  

Vous pouvez par contre décider de lier une ressource à une salle ou non.  
Si la ressource est liée à une salle, les créneaux proposés sur le calendrier seront ceux de la salle.  
Si une salle est réservée, la ressource n'est plus disponible à la réservation.  

Si la ressource n'est pas liée à une salle, ne sélectionnez simplement pas salle dans la case correspondante et elle sera traitée indépendemment.  


### Espace de coworking (Shared Place Coworking Space)

Un espace de coworking est un espace partageable, loué à plusieurs utilisateurs en même temps.  

La configuration d'un espace de coworking est similaire à celle d'une salle.  

Vous pouvez par contre ajouter un nombre de places disponibles: l'application comptera le nombre d'inscrits à un créneau donné et bloquera les réservations pour ce créneau lorsque la limite sera atteinte.


### Réservation (Shared Place Booking)

Une réservation est un document enregistrant la réservation d'un créneau pour une salle/ressource/espace de coworking donné.  

Ce document est généré automatiquement lorsqu'un utilisateur réserve via la plateforme ou peut-être créé manuellement par un utilisateur système.  

Il permet de créer des événement visibles dans une vue 'Calendrier' d'ERPNext et permet de retrouver le devis et/ou la commande client correspondante.  

Chaque créneau réservé donne lieu à la création d'un document de réservation différent.  


<!-- markdown -->