/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.c
 * Author: agsof
 *
 * Created on June 14, 2017, 6:52 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <errno.h>
#include <wiringPi.h>
#include <wiringSerial.h>
#include <time.h>
#include <unistd.h>

#define BUFFSIZE 1024

 
int main(int argc, char** argv) {
    

    
    int connfd = 0;

    
    while(TRUE){
        
        switch (currentByte = getChar()){
            case 'p':
                fprintf(dataLog, "Temperature: %l\nPressure: %l\n",getChar()<<24|getChar()<<16|getChar()<<8|getChar(),getChar()<<24|getChar()<<16|getChar()<<8|getChar());
                break;
               
            case 'g':
                fprintf(dataLog, "Latitude: %f\n",getChar()<<56|getChar()<<48|getChar()<<40|getChar()<<32|getChar()<<24|getChar()<<16|getChar()<<8|getChar());
                fprintf(dataLog,"Longitude: %f\n",getChar()<<56|getChar()<<48|getChar()<<40|getChar()<<32|getChar()<<24|getChar()<<16|getChar()<<8|getChar());
                fprintf(dataLog,"Altitude: %d\n",getChar()<<56|getChar()<<48|getChar()<<40|getChar()<<32|getChar()<<24|getChar()<<16|getChar()<<8|getChar());
                fprintf(dataLog,"Time: %l\n",getChar()<<24|getChar()<<16|getChar()<<8|getChar());
                fprintf(dataLog,"Speed KPH: %f\n",getChar()<<24|getChar()<<16|getChar()<<8|getChar());
                fprintf(dataLog,"Track Degree: %f\n",getChar()<<24|getChar()<<16|getChar()<<8|getChar());
                fprintf(dataLog,"Speed Time: %l\n",getChar()<<24|getChar()<<16|getChar()<<8|getChar());
                break;     
                
            case 'a':
                
                break;
                            
            default:
                break;
        }
        
    
        usleep(100);
        
    }
    
    
    return (EXIT_SUCCESS);
}



void setup();
uint64_t hash(unsigned char *str);
void error(const char*);

int fd;

int main()
{
        setup();
	struct sockaddr_in server_addr, client_addr;
	int listener_d = 0;
        FILE *dataLog = fopen("../dataLog.txt","w+");

	
	//creation of the socket
        listener_d = socket (AF_INET, SOCK_STREAM, 0);
	
	//preparation of the socket address
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = (in_port_t)htons(5000);
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	
	// Set socket for reuse
	int reuse = 1;	
	if (setsockopt(listener_d, SOL_SOCKET, SO_REUSEADDR, (char *)&reuse, sizeof(int)) == -1)
		error("Can't set the reuse option on the socket");
		
	// Bind the socket
	int c = bind (listener_d, (struct sockaddr *) &server_addr, sizeof(server_addr));
	if (c == -1)
		error("Can't bind to socket");
		
	// Listen
	if (listen(listener_d, 2) == -1)
		error("Can't listen");
	printf("Echo Server Listening....\n");	
	while (1) {
                int counter = 0;
		char buffer[BUFFSIZE];
		unsigned int address_size = sizeof(client_addr);  // size of structure holding client sddress
	
		memset(buffer, 0, BUFFSIZE);  // initialize buffer to 0
                
                for(int i=0;i<BUFFSIZE;i++){
                    if (serialDataAvail (fd))
                    {
                        buffer[i] = serialGetchar (fd);
                    }else{
                        --i;
                    }
                }
                
		// accept incomming connections
		int connect_d = accept(listener_d, (struct sockaddr *)&client_addr, &address_size);
		if (connect_d == -1)
			error("Can't open secondary socket");
			
		int len = 0;
		while ((len = recv(connect_d, buffer, BUFFSIZE, 0))) {
			
			printf("%s", "from client: ");
  		fputs(buffer, stdout);

			send(connect_d, buffer, len, 0);  //send data back to client
			
			memset(buffer, 0, BUFFSIZE);  // flush buffer to 0
		}
	
                if(counter == 2000){
                serialPutchar (fd, 0xF0) ;
                counter = 0;
                }
                
                counter++;
                
		close(connect_d);
	}
	fclose(dataLog);
	return 0;
}
uint64_t hash(unsigned char *str)
{
	uint64_t hash_v = 5381;
	int c;

	while (c = *str++)
	hash_v = ((hash_v << 5) + hash_v) + c; /* hash * 33 + c */

	return hash_v;
}

void error(const char *msg)
{
	printf("%s", msg);
	exit(1);
}

void setup(){
 
  if ((fd = serialOpen ("/dev/ttyAMA0", 38400)) < 0)
  {
    fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
    return 1 ;
  }

  if (wiringPiSetupGpio () == -1)
  {
    fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno)) ;
    return 1 ;
  }
    
}