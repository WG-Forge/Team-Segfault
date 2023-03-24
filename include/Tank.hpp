#ifndef __TANK_HPP__
#define __TANK_HPP__

#include <iostream>

// redundant?
// namespace tank_constants
// {
//     const std::string MEDIUM = "medium_tank";
//     const std::string LIGHT = "light_tank";
//     const std::string HEAVY = "heavy_tank";
//     const std::string ATSPG = "at_spg";
//     const std::string SPG = "spg";
// };


class Tank
{
    std::string type;
    short tank_id;
    short hp;
    short sp;
    Hex *position;
    const Hex *spawn_position;
public:
    Tank()  {}
    
    void update(const std::string &tank_info) {}


    // decrements tank hp. if tank is destroyed (hp is reduced to 0), resets vehicle hp (so the same object can be used as a respawn tank)
    // called if someone attacked us
    void reduce_health() 
    {
        hp--;
        if (hp <= 0)
            this->reset();
    }


    short get_id()          {return tank_id;}
    short get_hp()          {return hp;}
    std::string  get_type() {return type;}
    Hex& get_position()     {return *position;}

    // set hp to max (for now it can only be 2) and reset position
    // TODO: (on second stage) set hp based on vehicle type 
    void reset()                     {hp = 2; *position = *spawn_position;}
};

#endif