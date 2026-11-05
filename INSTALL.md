## Installation Steps for Advanced Users (only needs to run once)
- Download latest version of `keep-it-markdown` from releases and unzip it to your working directory
### Pipx Install
- Be sure `brew` (macOS), `winget` (Windows), are available on your OS (Linux users should have `apt` or `dnf` - check with AI on installing with other Linux distributions such as Alpine or Arch)
- Install `pipx` - see README or use AI for instructions for your OS 
- Install KIM dependencies - `pipx install -e .` (go to **Continue here** section)
### Pip Install
- Create a fresh virtual environment within the working directory 
- Activate a virtual environment 
- Install KIM dependencies in the venv - `pip install -e .` 
### Continue here
- Follow **Second Way** instructions here to get a copy of the oauth_token cookie value - https://github.com/rukins/gpsoauth-java?tab=readme-ov-file
- Run the script in the KIM directory - `get-token`
- Enter your Google email account name, oauth_token, and Android ID when prompted (Android ID can be anything, OAuth token expires in about 5 min)
- Copy the Keep Token value output from `get-token` 
- Run KIM to save the Token in your local Keyring - `kim -t <your long token value here>` 

Congratulations! You're done! Your Token is valid for all KIM versions now (unless Google changes it). You can now run KIM locally from this point on directly as `kim`  (see `kim --help` for switch options)
