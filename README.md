# Zenika-bot
# Zenika SkillZ and Platon chatbot

## Project's description:
This project's goal is to act as a link between clients and employees looking to sharpen their skills on different domains and in one of Zenika's french agencies. Users can ask for information to the bot and it will answer them by giving the email adress of available trainers.

The framework used to program this bot is RASA. All AI matters as well as the bot's training are handled by RASA when executing the command `rasa train` after deciding and or/changing how you want your bot to react. You can choose between various methods to train the bot as well as how it reads and processes the key words in your dialogue.


## How to install and run the project:
It is first recomended that you create a virtual environment to run the bot. To create one, you need Anaconda,  and then to run 

```
conda create -n your_env_name python=x.x anaconda 
```

To run this project, you will need to download the python module RASA. Run the following command to do so: `pip install rasa` or `pip3 install rasa` for Python3.

Once installed, two terminal windows will be needed: The first one will run `rasa run actions` to allow custom actions to be done by the bot, and a second one will run `rasa shell` used to start a dialogue with the bot.

Additionally, after each change in a file that is not actions.py, you will need to run `rasa train` for the bot to take into account your latest changes.

## How to use the project:
Just converse with the bot and admire.

## How to contribute to the project:
The words and sentences linked to intents are in the _nul.yml_ file. Skill names and agency names are in their respective files of the same name.

You can change which stories (series of intents and answers) the bot will be trained with in the _stories.yml_ file.

The _domain.yml_ file contains every intent the user can have, the entities the bot can recognize, as well as the name of his actions and the responses corresponding to these actions.

More importantly, the _config.yml_ file is were the training algorithms and their parameters are, as well as the *pipelines*, which are tokenizers or featurizers that help the bot recognize specific words and behaviors.

Lastly, the _actions.py_ file is were all custom actions are programed. It reads the _.csv_ files of the database and prepares answers accordingly to what it understood and has as informations.