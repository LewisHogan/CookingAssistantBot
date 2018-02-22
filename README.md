# CookingAssistantBot

A recipe assistant that runs on Pepper (Aldebaran's robot)

Written in Python 2.7

## Setup
Install the requests library for Python2.7
Clone this repository and run main.py

### Dependencies

To use the bot you will need access to the following API's

- NAOqi API
- Yummly

The app_id and api_key for Yummly should be stored in a keys.json file in the following format

	{
			"yummly_app_id": "YOUR_YUMMLY_APP_ID",
			"yummly_api_key": "YOUR_YUMMLY_API_KEY",
			"tesco_api_key": "YOUR_TESCO_API_KEY_HERE"
	}

In addition to the above requirements, CookingAssistantBot also requires that the Requests library is installed.

## Still Need Testing

- Tesco API Integration for Pricing information

## Coming Soon

- Temperature Conversion
