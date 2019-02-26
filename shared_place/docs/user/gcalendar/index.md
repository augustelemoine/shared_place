<!-- add-breadcrumbs -->
# Intégration avec Google Calendrier

Google Calendrier n'ayant pas de liens avec les salles/ressources/espaces de coworking configurés dans ERPNext, on ne peut pas avoir de synchronisation complète avec le calendrier d'ERPNext.

Les réservations sont cependant visibles dans Google Calendar si la synchronisation est active.

Le flux est ainsi le suivant:
- Les réservations sont envoyées à Google Calendar toutes les 3 minutes.
- Si un événement est créé sur Google Calendrier, celui-ci sera synchronisé avec le document "Evénement".

Le titre de la réservation est synchronisé avec le champ "titre" de Google Calendrier.
Le nom de la ressource est ajouté dans le champ description de l'événement Google Calendrier.


La configuration de l'intégration n'est pas modifiée: voir la [documentation officielle].(https://support.erpnext.com/docs/user/en/guides/integration/google_calendar)


<!-- markdown -->