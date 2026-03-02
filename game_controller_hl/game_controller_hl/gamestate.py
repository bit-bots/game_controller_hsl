#!/usr/bin/env python
# -*- coding:utf-8 -*-

from construct import Byte, Struct, Enum, Bytes, Const, Array, Int16ul, PaddedString, Flag, Int16sl

Short = Int16ul

RobotInfoStruct = "robot_info" / Struct(
    # define NONE                        0
    # define PENALTY_HL_KID_BALL_MANIPULATION    1
    # define PENALTY_HL_KID_PHYSICAL_CONTACT     2
    # define PENALTY_HL_KID_ILLEGAL_ATTACK       3
    # define PENALTY_HL_KID_ILLEGAL_DEFENSE      4
    # define PENALTY_HL_KID_REQUEST_FOR_PICKUP   5
    # define PENALTY_HL_KID_REQUEST_FOR_SERVICE  6
    # define PENALTY_HL_KID_REQUEST_FOR_PICKUP_2_SERVICE 7
    # define MANUAL                      15
    "penalty" / Byte,
    "secs_till_unpenalized" / Byte,
    #"number_of_warnings" / Byte,
    #"number_of_yellow_cards" / Byte,
    #"number_of_red_cards" / Byte,
    #"goalkeeper" / Flag
)

TeamInfoStruct = "team" / Struct(
    "team_number" / Byte,
    "field_player_color" / Enum(Byte,
                        BLUE=0,
                        RED=1,
                        YELLOW=2,
                        BLACK=3,
                        WHITE=4,
                        GREEN=5,
                        ORANGE=6,
                        PURPLE=7,
                        BROWN=8,
                        GRAY=9
                        ),
    "goalkeeper_color" / Enum(Byte,
                        BLUE=0,
                        RED=1,
                        YELLOW=2,
                        BLACK=3,
                        WHITE=4,
                        GREEN=5,
                        ORANGE=6,
                        PURPLE=7,
                        BROWN=8,
                        GRAY=9
                        ),
    "score" / Byte,
    "penalty_shot" / Byte,  # penalty shot counter
    "single_shots" / Short,  # bits represent penalty shot success
    "message_budget" / Short, #is short here intentional?
    "players" / Array(11, RobotInfoStruct) #always eleven fine?
)

GameStateStruct = "gamedata" / Struct(
    "header" / Const(b'RGme'),
    "to_motion" / Flag,
    "packet_number" / Byte,
    "players_per_team" / Byte,
    "competition_phase" / Enum(Byte,
                        COMPETITION_PHASE_ROUNDROBIN=0,
                        COMPETITION_PHASE_PLAYOFF = 1
                        ),
    "competition_type" / Enum(Byte,
                        COMPETITION_TYPE_NORMAL=0,
                        COMPETITION_TYPE_MOST_PASSES=1
                        ),
    "game_phase" / Enum(Byte,
                        GAME_PHASE_NORMAL=0,
                        GAME_PHASE_PENALTYSHOOT=1,
                        GAME_PHASE_OVERTIME =2,
                        GAME_PHASE_TIMEOUT=3,
                        ),
    "state" / Enum(Byte,
                        STATE_INITIAL=0,
                        # auf startposition gehen
                        STATE_READY=1,
                        # bereithalten
                        STATE_SET=2,
                        # spielen
                        STATE_PLAYING=3,
                        # spiel zu ende
                        STATE_FINISHED=4,
                        # standby
                        STATE_STANDBY=5
                        ),
    "set_play" / Enum(Byte,
                             SET_PLAY_NONE=0,
                             SET_PLAY_GOAL_KICK=1,
                             SET_PLAY_PUSHING_FREE_KICK=2,
                             SET_PLAY_CORNER_KICK=3,
                             SET_PLAY_KICK_IN=4,
                             SET_PLAY_PENALTY_KICK=5,
                             ),
    "first_half" / Flag,
    "kicking_team" / Byte,
    "secs_remaining" / Int16sl,
    "secondary_time" / Int16sl,
    "teams" / Array(2, "team" / TeamInfoStruct)
)

GAME_CONTROLLER_RESPONSE_VERSION = 2

ResponseStruct = Struct(
    "header" / Const(b"RGrt"),
    "version" / Const(GAME_CONTROLLER_RESPONSE_VERSION, Byte),
    "player_number" / Byte,
    "team_number" / Byte,
    "fallen" / Flag,
    "pose" / float[3],
    "ball_age" / float,
    "ball" / float[2]
)
