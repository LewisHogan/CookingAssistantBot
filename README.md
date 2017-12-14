# CookingAssistantBot

A recipe assistant that runs on Pepper (Aldebaran's robot)

Written in Python 2.7

## Setup


### Dependencies

To use the bot you will need access to the following API's

- NAOqi API
- Yummly

The app_id and api_key for Yummly should be stored in a keys.json file in the following format

	{
			"app_id": "YOUR_YUMMLY_APP_ID",
			"api_key": "YOUR_YUMMLY_API_KEY"
	}

In addition to the above requirements, CookingAssistantBot also requires that the Requests library is installed on Pepper.