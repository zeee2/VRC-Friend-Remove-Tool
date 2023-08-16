<div align="center">

# VRC Friend Remove Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://en.wikipedia.org/wiki/MIT_License)</br>
Friend remove utility Using VRChat API

This utility is created for remove the friend in VRChat.</br>
Ultimately, I am aiming for a friend management tool

**Note:**</br>
*Currently this utility was developed in Python 3.10.9 version.*</br>
*Currently this utility was developed based on the VRChat API documentation as of August 17, 2023.*</br>
*If there are any changes to the VRChat API in the future, the utility may not function correctly.*
</div>

# Final Goal
- [ ] Implement more friend management features than just the ability to remove friends
- [ ] Rewrite using C# or another language (?) with a UI presence
- [ ] Create a simpler user experience
- [ ] Support Multi-language
- [ ] idk, What else could be added?

# Features
- Exclude friends from friend removal can be manually configured by the user
- Exclude friends from friend removal whose last login date is less than 100 days
- Save result as a JSON file

# Usage
- Clone this project.
```
git clone https://github.com/zeee2/VRC-Friend-Manager.git
```
- Install the required modules for operation.</br>*(Honestly, the modules used in this project are built-in to Python, so I don't know if they need to be installed.)*
```
Windows:
python -m pip install -r requirements.txt

Others:
python3 -m pip install -r requirements.txt
```
- Open the deny.txt file and enter the nicknames of users to be excluded from friend removal, each on a new line. Below is an example of deny.txt.
```
USER 1
USER2
user 3
```
- Run run.py.
```
python3 run.py
```
- Follow the steps as instructed.