import os
import xarray as xr

def verifier_fichiers_nc(dossier):
    fichiers_incorrects = []
    for fichier in os.listdir(dossier):
        if fichier.endswith('.nc'):
            chemin_fichier = os.path.join(dossier, fichier)
            resultat = verifier_fichier(chemin_fichier)
            if resultat is not None:
                fichiers_incorrects.append(resultat)
    
    if fichiers_incorrects:
        print("\nFichiers avec des dates incorrectes :")
        for fichier, debut, fin in fichiers_incorrects:
            print(f"  {fichier} : Début trouvé = {debut}, Fin trouvée = {fin}")
        tronquer_fichiers(dossier, fichiers_incorrects)
        # verifier que les fichiers crée soit 

def verifier_fichier(chemin_fichier):
    try:
        nom_fichier = os.path.basename(chemin_fichier)
        annee = int(nom_fichier.split('_')[0])
        
        ds = xr.open_dataset(chemin_fichier)
        dates = ds.time.values
        premiere_date = str(dates[0])
        derniere_date = str(dates[-1])
        
        # Vérification de la première date
        date_debut_attendue = f'{annee}-01-01T00:00:00.000000000'
        debut_correct = premiere_date == date_debut_attendue
        
        # Vérification de la dernière date
        date_fin_attendue = f'{annee}-12-31T23:00:00.000000000'
        fin_correcte = derniere_date == date_fin_attendue
        
        # Vérification de l'année
        annee_correcte = annee == int(premiere_date[:4]) and annee == int(derniere_date[:4])
        
        if not (debut_correct and fin_correcte and annee_correcte):
            return (nom_fichier, premiere_date, derniere_date)
    except Exception as e:
        print(f"Erreur lors de la vérification du fichier {chemin_fichier} : {e}")
    return None

def tronquer_fichiers(dossier, fichiers_incorrects):
    for fichier, debut, fin in fichiers_incorrects:
        chemin_fichier = os.path.join(dossier, fichier)
        tronquer_fichier(chemin_fichier, debut[:4])

def tronquer_fichier(chemin_fichier, annee):
    try:
        nom_fichier = os.path.basename(chemin_fichier)
        annee = int(nom_fichier.split('_')[0])
        print('nom')
        ds = xr.open_dataset(chemin_fichier)
        debut_annee = f'{annee}-01-01T00:00:00.000000000'
        fin_annee = f'{annee}-12-31T23:00:00.000000000'
        
        ds_tronquee = ds.sel(time=slice(debut_annee, fin_annee))
        
        nom_fichier = os.path.basename(chemin_fichier)
        nouveau_nom = f"corrige_{nom_fichier}"
        chemin_nouveau_fichier = os.path.join(os.path.dirname(chemin_fichier), nouveau_nom)
        
        ds_tronquee.to_netcdf(chemin_nouveau_fichier)
        
        print(f"Fichier corrigé créé : {chemin_nouveau_fichier}")
        
    except Exception as e:
        print(f"Erreur lors de la création du fichier corrigé pour {chemin_fichier} : {e}")

dossier = 'DATA_ERA5'
verifier_fichiers_nc(dossier)