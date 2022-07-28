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
        #print (skill)
        
        df = pd.read_csv('bdd/Export Skillz 2022-06-27 - Feuille 1.csv', sep=',', encoding='utf-8')
        df.columns = df.columns.str.strip() #Enleve les espaces en "bord" de chaque colonne du dataframe
        
        mask2= df['skill_level']>3 #Masque pour que seules les compétences de niveau 4 ou 5 des utilisateurs soient retenues
        
        #Reste à voir comment récupérer les caractères spéciaux comme (+,#,>,<) Tokenizer personalisé mais il faut arriver à le connecter au code
        
        if (skill):
            print (skill)
            df_skill_name = df['skill_name']
            mask1 = (df_skill_name).str.casefold() == skill.casefold()
            df_trainers_skill=df[(mask1 & mask2)]
        
        
        if (not skill):
            dispatcher.utter_message(" Nous n'avons pas compris votre demande. Veuillez la préciser en ajoutant la compétence recherchée ainsi que l'agence")

        elif (skill):
            if (len(df_trainers_skill)==0 ):
                dispatcher.utter_message(" Nous sommes désolés, nous n'avons pas de formateur {}".format(skill))
            else:
                df_trainers_emails = df_trainers_skill['collaborator_email'].drop_duplicates(keep='first').values.tolist()
                df_trainers_agency_name = df_trainers_skill['collaborator_agency_name'].values.tolist()
                
                #Nouvelle liste contenant skill + agence du collaborateur
                df_trainers_skill_and_agency = [(df_trainers_emails[i], df_trainers_agency_name[i]) \
                    for i in range(len(df_trainers_emails))]
                
                #emails_agence_skill = True
                dispatcher.utter_message(" Vous pouvez contacter l'une de ces adresses pour apprendre {}".format(skill))
                
                #Envoie du message avec le mail et l'agence
                for trainer in df_trainers_skill_and_agency:
                    dispatcher.utter_message ( "{}".format(trainer[0]) +" à : l'agence de {}".format(trainer[1]))


        return [AllSlotsReset()]