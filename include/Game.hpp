#ifndef __GAME_HPP__
#define __GAME_HPP__

#include "Map.hpp"
#include "Tank.hpp"

#include <iostream>
#include <unordered_map>

enum Action
{
    LOGIN = 1,
    LOGOUT = 2,
    MAP = 3,
    GAME_STATE = 4,
    GAME_ACTIONS = 5,
    TURN = 6,
    CHAT = 100,
    MOVE = 101,
    SHOOT = 102
};

enum Result
{
    OKEY = 0,
    BAD_COMMAND = 1,
    ACCESS_DENIED = 2,
    INAPPROPRIATE_GAME_STATE = 3,
    TIMEOUT = 4,
    INTERNAL_SERVER_ERROR = 500
};





// for now, I can only think of 2 ways for playing:
// 1: call MAP on begining, GAME_STATE every turn and call game_actions to update tank information
// 2: call MAP on begining. call only GAME_STATE and based on its response update map/tank information
//      possible problem: GAME_STATE only shows vehicle info of player whose turn it is; TODO: ask this

class Game
{
    std::string username;
    
    short id;
    short turns_remaining;
    short players;
    short capture_points;
    short kill_points;
    
    Map *map;
    Tank tanks[5];

    // this will probably be needed on next stages
    // std::unordered_map<Hex*, Hex*> catapults;

public:
    Game(std::string &name): username(name) {}

    void start_game() {
        // login and save id

        // send MAP request and update tank spawn locations and map

        // while (1)
        //      send GAME_STATE request and update tank health/positions
        //      if game is finished call game_over and break
        //     
        //      if (GAME_STATE.current_player_idx == id)
        //          update out tank positions and hp with GAME_STATE repsonse
        //          play_move()
        // 
        //      send TURN message and await for OKAY response, if TIMEOUT is recieved then break           

    }

    // every function below start_game should maybe be private since its called only from inside this class

    // covers LOGOUT, CHAT, MOVE and SHOOT 
    void action_without_response(Action action, const std::string &data) {}

    // covers everything else; these two functions can be merged into one
    std::string& action_with_response(Action action, const std::string &data) {}

    void play_move()    {}

    // write output and logout
    void game_over()    {}

};

#endif