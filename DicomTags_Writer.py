# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 08:59:30 2025

@author: 129391
"""

import pydicom
from pydicom.tag import Tag
from tkinter import Tk, filedialog, simpledialog, messagebox


def convert_str_to_tag(tag_str):
    try:
        # Nettoyer la chaîne (retirer parenthèses et espaces)
        tag_str = tag_str.strip().replace("(", "").replace(")", "")
        group_str, elem_str = tag_str.split(",")
        group = int(group_str, 16)
        elem = int(elem_str, 16)
        return Tag(group, elem)
    except Exception:
        return None

def modifier_champ_dicom():
    root = Tk()
    root.withdraw()

    fichier = filedialog.askopenfilename(
        title="Sélectionnez un fichier DICOM à modifier",
        filetypes=[("Fichier DICOM", "*.dcm"), ("Tous les fichiers", "*.*")]
    )
    
    ds = pydicom.dcmread(fichier)   
        
    if not fichier:
        print("Aucun fichier sélectionné.")
        return
    
    Tag_to_Edit= simpledialog.askstring("Saisir un tag hexadécimal", "Quel tag DICOM souhaitez-vous modifier ?\nVeuillez saissir le code hexadécimal\n")

    if not Tag_to_Edit:
        messagebox.showinfo("Annulé", "Aucun tag saisi.")
        return

    Tag_to_Edit = convert_str_to_tag(Tag_to_Edit)

    if Tag_to_Edit not in ds:
        cree = messagebox.askyesno("Tag non présent", f"Le tag '{Tag_to_Edit}' n'existe pas dans ce fichier.\nVoulez-vous le créer ?")
        if not cree:
            return
    
    try:
        # Demander la nouvelle valeur
        nouvelle_valeur = simpledialog.askstring("Nouvelle valeur", f"Saisissez la nouvelle valeur pour {Tag_to_Edit} :")
        if nouvelle_valeur is None:
            messagebox.showinfo("Annulé", "Aucune modification effectuée.")
            return

        # Appliquer la modification
        ds[Tag_to_Edit].value = nouvelle_valeur

        # Sauvegarde dans un nouveau fichier
        nouveau_fichier = fichier.replace(".dcm", "_modifie.dcm")
        ds.save_as(nouveau_fichier)

        messagebox.showinfo("Succès", f"Tag '{Tag_to_Edit}' mis à jour avec succès !\nFichier sauvegardé :\n{nouveau_fichier}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

# Lancer la fonction
modifier_champ_dicom()
