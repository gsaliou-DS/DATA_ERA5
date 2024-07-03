import os
import netCDF4
from datetime import datetime

def verifier_fichiers_nc(dossier):
    fichiers_incorrects = []
    for fichier in os.listdir(dossier):
        if fichier.endswith('.nc'):
            chemin_fichier = os.path.join(dossier, fichier)
            resultat = verifier_fichier_nc(chemin_fichier)
            if resultat is not None:
                fichiers_incorrects.append(resultat)
    
    if fichiers_incorrects:
        print("\nFichiers avec des dates incorrectes :")
        for fichier, debut, fin in fichiers_incorrects:
            print(f"  {fichier} : Début trouvé = {debut}, Fin trouvée = {fin}")

def verifier_fichier_nc(chemin_fichier):
    nc_fichier = netCDF4.Dataset(chemin_fichier, 'r')
    
    try:
        nom_fichier = os.path.basename(chemin_fichier)
        annee = int(nom_fichier.split('_')[0])
        
        for nom_var, var in nc_fichier.variables.items():
            if nom_var == 'time':
                time_units = var.units
                dates = netCDF4.num2date(var[:], time_units)
                premiere_date = dates[0]
                derniere_date = dates[-1]
                
                # Vérification de la première date
                date_debut_attendue = datetime(annee, 1, 1, 0, 0)
                debut_correct = premiere_date == date_debut_attendue
                
                # Vérification de la dernière date
                date_fin_attendue = datetime(annee, 12, 31, 23, 0)
                fin_correcte = derniere_date == date_fin_attendue
                
                if not (debut_correct and fin_correcte):
                    return (nom_fichier, premiere_date, derniere_date)
    except Exception as e:
        print(f"Erreur lors de la vérification du fichier {chemin_fichier} : {e}")
    finally:
        nc_fichier.close()
    return None

dossier = '/Volumes/IMT-SC-015/DATA_ERA5'
verifier_fichiers_nc(dossier)
