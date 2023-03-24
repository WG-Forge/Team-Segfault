/*
    enemy_tanks hash map:
        enemy tabk data could be implemented differently;
        we can delete previous data also in O(1) in case of enemy tank movement (iterate through all 10 values in enemy_tanks) 
        and enemy_tanks can be updated in O(1) since we have target_destination (map.insert())

*/

#ifndef __map_hpp__
#define __map_hpp__

#include "Tank.hpp"

#include <iostream>
#include <unordered_map>
#include <vector>

// redundant?
namespace hex_constants
{
    const std::string BASE = "base";
    const std::string OBST = "obstacle";
    const std::string LREP = "light_repair";
    const std::string HREP = "hard_repair";
    const std::string CTPL = "catapult";
};

class Hex 
{
private:
    short x;
    short y;
    short z;
public:
    Hex(short _x, short _y, short _z, const std::string &_type): x(_x), y(_y), z(_z) {};

};

class Map
{
    short size;
    // only saves hexes that are not empty
    // enemy_tanks should be changed to multiap since there can be multiple vehicles in base hex
    std::unordered_map<Hex*, std::string> special_hexes;
    std::unordered_map<Hex*, Tank*>        enemy_tanks;
public:
    
    Map()   {}

    // parse map data
    void update(const std::string &map) {}

    // TODO: add get/set methods (or make hash maps public??)

};


#endif