#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>


int main( int argc, char *argv[] )
{
  struct sockaddr_in saddr;
  int soc;
  char ip_addr[100];
  int port;
  char buf[1024];
  int len;

  if ( argc != 3 ) {
    fprintf( stderr, "Usage: %s IP_address Port\n", argv[0] );
    exit( 1 );
  }

  strcpy( ip_addr, argv[1] );
  port = atoi( argv[2] );

  if ( ( soc = socket( AF_INET, SOCK_STREAM, 0 ) ) < 0 ) {
    perror( "socket" );
    exit( 1 );
  }

  memset( &saddr, 0, sizeof( saddr ) );
  saddr.sin_family = AF_INET;
  saddr.sin_addr.s_addr = inet_addr( ip_addr );
  saddr.sin_port = htons(port);

  if ( connect( soc, ( struct sockaddr * )&saddr, ( socklen_t )sizeof( saddr ) ) < 0 ) {
    perror( "connect" );
    exit( 1 );
  }
  fprintf( stderr, "Connection established: socket %d used.\n", soc );

  while( fgets( buf, 1024, stdin ) ) {
    write( soc, buf, strlen( buf )+1 );
    fsync( soc );
    len = read( soc, buf, 1024 );
    buf[len] = '\0';
    fprintf( stdout, "%s\n",  buf );
  }

  close( soc );

  return 0;
}


