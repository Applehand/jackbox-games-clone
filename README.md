# Project Colony Party

## Introduction

A couch co-op game that involves deception and role play in a sci-fi setting.

## Features

- Adversarial gameplay for 2-4 players.
- Round-based structure with short game sessions.
- Players use a web page to issue actions and must complete objectives while maintaining anonymity.

## Installation

To run the project locally, you'll need to clone this repository and set up three things - the frontend, the backend, and the game engine.

### 1. Clone the Repository

Make sure [git](https://git-scm.com/) is installed, and run this to clone these remote files into your local file system:
  ```
  git clone https://github.com/Applehand/colony-party.git
  cd colony-party
  ```
### 2. Set Up the Backend

Make sure Python is installed, and run this to create and activate the virtual environment:
```
python -m venv venv
source venv/bin/activate
```
On Windows, use:
```
python -m venv venv
venv\Scripts\activate
```
You should see (venv) in your terminal upon activation.

Install the required server libraries with:
```
pip install -r requirements.txt
```
Start the server:
```
fastapi dev main.py
```
### 3. Set Up the Frontend

Make sure [Node](https://nodejs.org/) is installed and run this to serve the frontend to your browser:
```
cd frontend
npx serve
```
### 4. Set Up the Game Engine (Godot)

Make sure you have [Godot](https://godotengine.org/) installed. To edit and run the Game, do:
- Open Godot Launcher
- Click on "Import"
- Select the project.godot file.
- Edit Project

## Usage

To begin, run the Godot project and create a session. Open the web frontend to enter the session ID and a name, then click the "Join Session" button. Follow the prompts to participate in the game.

## Doc Links
- [AlpineJS](https://alpinejs.dev/)
- [AlpineJS Requests](https://github.com/0wain/alpinejs-requests)
- [PicnicCSS](https://picnicss.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

