import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from statemachine import StateMachine, State
import asyncio

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PlayerState(StateMachine):
    alive = State(initial=True)
    dead = State(final=True)

    died = alive.to(dead)


class SessionState(StateMachine):
    waiting_for_players = State(initial=True)
    game_active = State()

    start_game = waiting_for_players.to(game_active)
    end_game = game_active.to(waiting_for_players)


class GameState(StateMachine):
    pregame_briefing = State(initial=True)
    game_active = State()
    postgame_briefing = State(final=True)

    start_game = pregame_briefing.to(game_active)
    end_game = game_active.to(postgame_briefing)


def serialize_state(state_machine: StateMachine) -> str:
    return state_machine.current_state.id


def create_game_context():
    return [""]


def create_character_traits():
    return [""]


def assign_character_role():
    return ""


def gen_player_id():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    player_id = ""
    for i in range(0, 3):
        player_id += random.choice(chars)
    return player_id


class PlayerRequest(BaseModel):
    session_id: str
    name: str


class Player(BaseModel):
    id: str = Field(default_factory=gen_player_id)
    session_id: str
    name: str
    role: str = Field(default_factory=assign_character_role)
    traits: List[str] = Field(default_factory=create_character_traits)
    state: PlayerState = Field(default_factory=PlayerState)

    class Config:
        arbitrary_types_allowed = True

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data['state'] = serialize_state(self.state)

        return data


class Game(BaseModel):
    id: str
    session_id: str
    winner: Optional[Player] = None
    context: List[str] = Field(default_factory=create_game_context)
    state: GameState = Field(default_factory=GameState)

    class Config:
        arbitrary_types_allowed = True

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data['state'] = serialize_state(self.state)

        return data


class Session(BaseModel):
    id: str
    current_game_id: Optional[str] = None
    players: List[Player] = []
    games: List[Game] = []
    update_event: asyncio.Event = Field(default_factory=asyncio.Event, exclude=True)
    state: SessionState = Field(default_factory=SessionState)

    class Config:
        arbitrary_types_allowed = True

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data['state'] = serialize_state(self.state)
        data['players'] = [player.model_dump() for player in self.players]

        return data


sessions: Dict[str, Session] = {}


@app.get("/")
def main():
    return {"hello this is main"}


@app.get("/poll-server-for-updates/{session_id}")
async def poll_server_for_updates(session_id: str):
    current_session = sessions[session_id]

    await current_session.update_event.wait()
    current_session.update_event.clear()

    return current_session.model_dump()


@app.get("/update-client-test/{session_id}")
def update_client_test(session_id: str):
    current_session = sessions[session_id]
    current_session.update_event.set()

    return {'Client updated.'}


@app.get("/get-all-session-data")
def get_all_session_data():

    return [session.model_dump() for session in sessions.values()]


@app.get("/get-all-players-in-session/{session_id}")
def get_all_players_in_session(session_id: str):
    current_session = sessions[session_id]

    return [player.model_dump() for player in current_session.players]


@app.post("/create-new-session/{session_id}")
def create_new_session(session_id: str):
    session = Session(id=session_id)
    sessions.update({session_id: session})
    print(f"New session {session_id} created.")

    return {f"Session {session.id} created."}


@app.post("/end-session/{session_id}")
def end_session(session_id: str):
    sessions.pop(session_id)
    print(f"Session {session_id} ended.")

    return {f"Session {session_id} ended."}


@app.post("/create-new-game/{session_id}")
def create_new_game(session_id: str):
    current_session = sessions[session_id]
    game_id = str(len(current_session.games))
    game = Game(id=game_id, session_id=session_id)
    current_session.games.append(game)

    return {f"Game {game_id} has been created."}


@app.post("/end-game/{session_id}")
def end_game(session_id: str):
    current_session = sessions[session_id]
    current_session.games[-1].state.end_game()

    return {f"Game {current_session.games[-1].id} ended."}


@app.post("/add-player-to-session/")
async def add_player_to_session(player_req: PlayerRequest):
    player = Player(session_id=player_req.session_id, name=player_req.name)
    sessions[player_req.session_id].players.append(player)

    return {f"Added {player.name} to Session {player_req.session_id}"}


@app.post("/remove-player-from-session/{session_id}")
def remove_player_from_session(session_id: str):
    current_session = sessions[session_id]

    return {""}
