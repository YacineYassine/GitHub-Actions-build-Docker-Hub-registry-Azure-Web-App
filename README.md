# GitHub-Actions-build-Docker-Hub-registry-Azure-Web-App

L'objectif initial (avec une app simple qui affiche message de bienvue dans le browser) est d'avoir un déploiement continu (CD) entièrement automatisé sans intervention manuelle.

# Workflow

GitHub (code) → GitHub Actions (build) → Docker Hub (registry) → Azure Web App (production)

workflow fera :
Déclenchement : Sur push sur la branche main

Build Docker : Construire l'image avec le tag du commit

Push vers Docker Hub : Authentification et publication

Déploiement Azure : Mettre à jour la Web App avec la nouvelle image

Forcer le redémarrage : S'assurer qu'Azure utilise la dernière version

🔧 Ce dont vous aurez besoin :
Secrets GitHub à configurer :

DOCKERHUB_USERNAME : Votre nom d'utilisateur Docker Hub

DOCKERHUB_TOKEN : Votre token d'accès Docker Hub

AZURE_CREDENTIALS : Vos credentials Azure (Service Principal)
