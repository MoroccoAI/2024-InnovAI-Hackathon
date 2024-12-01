# dashboard/management/commands/load_drug_data.py
import csv
from django.core.management.base import BaseCommand
from dashboard.models import Drug 

class Command(BaseCommand):
    help = 'Load drug data from CSV file and save into Drug model'

        
    def handle_statut_commercialisation(self, statut):
        if statut == 'Non Commercialisé':
            return 'NC'  # Use 'NC' instead of 'CC' to match the model
        elif statut == 'Retiré du Marché':
            return 'RM'
        elif statut == 'Commercialisé / AO':
            return 'C/AO'
        else:
            return 'C'  # Default for 'Commercialisé' should be 'C'

    def handle_statut_amm_mapping(self , statut):
        if(statut=='AMM ENREGISTREE'):
            return 'AMME'
        else :
            return 'AMMR'
        
    def handle(self, *args, **kwargs):
        file_path = './assets/data/data.csv'  # Path to your CSV file relative to project root
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['SPECIALITE']
                dosage = row['DOSAGE']
                form = row['FORME']
                substances = row['SUBSTANCE ACTIVE']
                statut_amm = self.handle_statut_amm_mapping(row['STATUT AMM'])
                statut_commercialisation = self.handle_statut_commercialisation(row['STATUT COMMERCIALISATION'])
                presentation = row['PRESENTATION']
                pp_gn = row['PP GN']
                class_therapeutique = row['CLASSE THERAPEUTIQUE']
                EPI = row['EPI']
                PPV = float(row['PPV'].replace(',', '.')) if row['PPV'] else 0
                PH = float(row['PH'].replace(',', '.')) if row['PH'] else 0
                PFHT = float(row['PFHT'].replace(',', '.')) if row['PFHT'] else 0
                code_ATC = row['CODE'] if row['CODE'] else ''
                TVA = float(row['TVA'].replace(',', '.')) if row['TVA'] else None
                
                drug, created = Drug.objects.update_or_create(
                    name=name,
                    dosage=dosage,
                    form=form,
                    substances=substances,
                    statutAMM=statut_amm,
                    statutCommercialisation=statut_commercialisation,
                    presentation=presentation,
                    pp_gn=pp_gn,
                    class_therapeutique=class_therapeutique,
                    EPI=EPI,
                    PPV=PPV,
                    PH=PH,
                    PFHT=PFHT,
                    code_ATC=code_ATC,
                    TVA=TVA
                )
                
        self.stdout.write(self.style.SUCCESS('Successfully loaded drug data'))
