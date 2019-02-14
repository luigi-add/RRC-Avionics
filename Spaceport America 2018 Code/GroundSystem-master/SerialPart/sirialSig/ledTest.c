/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   ledTest.c
 * Author: agsof
 *
 * Created on April 1, 2017, 2:42 AM
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#include <wiringPi.h>
#include <wiringSerial.h>


#define LEDSLOW 4
#define LEDFAST 2

/*
 * 
 */
int main1(int argc, char** argv) {
    if (wiringPiSetupGpio() == -1) {
        fprintf(stdout, "Unable to start wiringPi: %s\n", strerror(errno));
        return 1;
    }

    pinMode(LEDFAST, OUTPUT);
    pinMode(LEDSLOW, OUTPUT);

    for (;;) {
        digitalWrite(LEDSLOW, LOW);
        digitalWrite(LEDFAST, HIGH);
        printf("Slow LOW\nFast HIGH\n\n");
        delay(5000);

        digitalWrite(LEDSLOW, HIGH);
        digitalWrite(LEDFAST, LOW);
        printf("Slow HIGH\nFast LOW\n\n");
        delay(5000);

        digitalWrite(LEDFAST, HIGH);
        printf("Slow HIGH\nFast HIGH\n\n");
        delay(5000);
    }


    return (EXIT_SUCCESS);
}

