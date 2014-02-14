#ifndef CONSTANTS_H
#define CONSTANTS_H
/*
In C++ const objects have internal linkage unless explicitly declared extern 
so the is no problem with putting a definition in a header.
*/
// Digital Pins START
/* 
Built-in digital pin:
Default Pin Mapping 
Arduino Pin VNH5019   Basic Function
Digital 2   M1INA     Motor 1 *direction input A
Digital 4   M1INB     Motor 1 *direction input B
Digital 6   M1EN/DIAG Motor 1 enable input/fault output
Digital 7   M2INA     Motor 2 *direction input A
Digital 8   M2INB     Motor 2 *direction input B
Digital 9   M1PWM     Motor 1 *speed input // cannot configure
Digital 10  M2PWM     Motor 2 *speed input // cannot configure 
Digital 12  M2EN/DIAG Motor 2 enable input/fault output

Analog  A0  M1CS      Motor 1 current sense output
Analog  A1  M2CS      Motor 2 current sense output

*/
// Encoder: two channels for both speed and direction 
// remaining least-significant-bit pins

const unsigned char INA1 = 2; // remapped to 5
const unsigned char INB1 = 5;
const unsigned char EN1DIAG1 = 6;
const unsigned char CS1 = A0;  // not used 
const unsigned char INA2 = 7;
const unsigned char INB2 = 8;
const unsigned char EN2DIAG2 = 12;
const unsigned char CS2 = A1; // not used 

const unsigned char M1_ENCODER_A = 3; // external interrupt pin 2, 3
const unsigned char M1_ENCODER_B = 5; 
const unsigned char M2_ENCODER_A = 11; 
const unsigned char M2_ENCODER_B = 13; 


// Digital Pins END

// Analog Pins START

// Analog Pins END
#endif