from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import pandas as pd
import numpy as np
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset

class ActionTrainerSearch(Action):

    def name(self) -> Text:
        return "action_trainer_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Any:
        skill = tracker.get_slot("skill") #Récupère l'entité "skill" repérée par le bot
        agence = tracker.get_slot("agence") #Récupère l'entité "agence" repérée par le bot
        print (skill)
        print (agence)
        df = pd.read_csv('bdd/Export Skillz 2022-06-27 - Feuille 1.csv', sep=',', encoding='utf-8')
        df.columns = df.columns.str.strip() #Enleve les espaces en "bord" de chaque colonne du dataframe
        
        df_collaborator_agency_name=df['collaborator_agency_name']
        mask2= df['skill_level']>3 #Masque pour que seules les compétences de niveau 4 ou 5 des utilisateurs soient retenues
        
                
        if (skill):
            print (skill)
            df_skill_name = df['skill_name']
            mask1 = (df_skill_name).str.casefold() == skill.casefold()
            df_trainers_skill=df[(mask1 & mask2)]
            
        if (agence):
            print (agence)
            mask3 = df_collaborator_agency_name.str.casefold() == agence.casefold()
            df_trainers_agence=df[(mask2 & mask3)]
        
        emails = False
        emails_agence_skill= False
        if (not skill and not agence):
            dispatcher.utter_message(" Nous n'avons pas compris votre demande. Veuillez la préciser en ajoutant la compétence recherchée ainsi que l'agence")

        elif (skill):
            if (len(df_trainers_skill)==0 ):
                dispatcher.utter_message(" Nous sommes désolés, nous n'avons pas de formateur {}".format(skill))
            else:
                if (agence):
                    df_trainers_emails= df_trainers_skill['collaborator_email'].drop_duplicates(keep='first').values.tolist()
                    emails= True
                    emails_agence_skill = True
                    dispatcher.utter_message(" Vous pouvez contacter l'une de ces adresses pour apprendre {}".format(skill))
                else:
                    df_trainers_emails= df_trainers_skill['collaborator_email'].drop_duplicates(keep='first').values.tolist()
                    emails= True
                    dispatcher.utter_message(" Vous pouvez contacter l'une de ces adresses pour apprendre {}".format(skill))

        if(emails):
            for trainer_email in df_trainers_emails:
                dispatcher.utter_message ( "{}".format(trainer_email))
        if(emails_agence_skill):
            for trainer_email in df_trainers_emails:
                dispatcher.utter_message ( "{}".format(trainer_email[0]) +" : formateur {}".format(trainer_email[1]))
       

        return [AllSlotsReset()]