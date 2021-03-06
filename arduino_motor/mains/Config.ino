#include "Config.h"
int const Config::MAX_SPEED_ANALOG = 255;
int const Config::DESIGNED_MAX_SPEED = 400;
int const Config::WHEEL_DIAMETER = 6;

int const Config::COUNTS_PER_REVOLUTION = 2249/2; // only one output connected to arduino for each encoder
double const Config::DISTANCE_PER_TICK_CM = (PI*WHEEL_DIAMETER)/COUNTS_PER_REVOLUTION; //0.016762077012005334

int const Config::SAMPLE_TIME = 1; // tuned
double const Config::WHEELS_INTERVAL = 17.10; // turning right 17.24 SWE Lab (low V); ( SPL high V 17.15) (SWE high V 17.12)
double const Config::WHEELS_INTERVAL_LEFT = 17.10; // (SPL high V 17.15) (SWE high V 17.10)                     

double Config::MAX_SPEED = 300;
double Config::TARGET_SPEED = 200;
double Config::MIN_SPEED = 150;
double Config::PID_UPPER_LIMIT = COUNTS_PER_REVOLUTION*6*(double(MAX_SPEED)/DESIGNED_MAX_SPEED);
double Config::PID_LOWER_LIMIT = PID_UPPER_LIMIT*(double(MIN_SPEED)/DESIGNED_MAX_SPEED);
double Config::PID_SETPOINT = PID_UPPER_LIMIT*(double(TARGET_SPEED)/DESIGNED_MAX_SPEED);

bool Config::verbose = true;

//double const Config::TICKS_PER_DEGREE = (WHEELS_INTERVAL/2)*(PI/180)*(1/DISTANCE_PER_TICK_CM); //8.95463688680154
//double const Config::TICKS_PER_DEGREE_LEFT = (WHEELS_INTERVAL_LEFT/2)*(PI/180)*(1/DISTANCE_PER_TICK_CM); 

// range from 796 - 810; 803 baseline, -7 to +7; log 14 = 4
double const Config::TICKS_PER_DEGREE_LEFT = (803+(-4))/90.0; // {6.08: [+2], 6.20: [-6, -4]}
double const Config::TICKS_PER_DEGREE = (803+(-4))/90.0; // {6.08: [+2], 6.20: [-5, -4]}
int const Config::VIRTUAL_OFFSET = 5;
