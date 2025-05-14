## Installation Steps for Advanced Users (only needs to run once)
- Python 3.10+ required (or use pyenv for a specific new version)
- Download latest version of `keep-it-markdown` from releases and unzip it to your working directory
- Create a fresh virtual environment within the working directory 
- Activate a virtual environment 
- Install KIM dependencies in the venv - `pip install -r requirements.txt`
- Follow **Second Way** instructions here to get a copy of the oauth_token cookie value - https://github.com/rukins/gpsoauth-java?tab=readme-ov-file
- Run the script in the KIM directory - `python get_token.py`
- Enter your Google email account name, oauth_token, and Android ID when prompted (Android ID can be anything, OAuth token expires in about 5 min)
- Copy the Keep Token value output from `get_token.py` 
- Linux users - you may need to install a Keyring - `pip install keyrings.alt`
- Run KIM to save the Token in your local Keyring - `python kim.py -t <your long token value here>`

Congratulations! You're done! Your Token is valid for all KIM versions now (unless Google changes it). You can now run KIM locally from this point on (see `kim.py --help` for switch options) 
