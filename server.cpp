/****************************************************
 * Written By  Shaleen Garg
 * Roll no : 201401069
 * International Intstitute Of Information Technology
******************************************************/
#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

//*****************************************************************************************************//
//The following Struct is defined in netinet/in.h
//We use this to communicate with the other one
//in_addr structure, defined in the same header file, contains only one field, a unsigned long called s_addr.
/*
struct sockaddr_in
{
  short   sin_family; // must be AF_INET //
  u_short sin_port;
  struct  in_addr sin_addr;
  char    sin_zero[8]; // Not used, must be zero //
};
*/

//*****************************************************************************************************//

//The following Struct is given by netdb.h
//We use this to communicate with the server, It is for the client
/*
struct  hostent
{
  char    *h_name;        // official name of host //
  char    **h_aliases;    // alias list //
  int     h_addrtype;     // host address type 
  int     h_length;       // length of address
  char    **h_addr_list;  // list of addresses from name server 
  #define h_addr  h_addr_list[0]  // address, for backward compatiblity
}; 
*/
//*****************************************************************************************************//

void error(char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *arg[])
{
    
    return 0;
}
