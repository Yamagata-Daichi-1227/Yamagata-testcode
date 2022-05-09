#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main( int argc, char *argv[] )
{
  int fd1, fd2;
  struct sockaddr_in saddr;
  struct sockaddr_in caddr;

  int len;
  int ret;
  int port;
  char buf[1024];

  if ( argc != 2 ) {
    fprintf( stderr, "Usage: %s Port_number\n", argv[0] );
    exit( 1 );
  }
  port = atoi( argv[1] );

  if ( ( fd1 = socket( AF_INET, SOCK_STREAM, 0 ) ) < 0 ) {
    perror( "socket" );
    exit( 1 );
  }

  memset( &saddr, 0, sizeof( saddr ) );
  saddr.sin_family = AF_INET;
  saddr.sin_addr.s_addr = INADDR_ANY;
  saddr.sin_port = htons(port);

  if ( bind( fd1, ( struct sockaddr * )&saddr, ( socklen_t )sizeof( saddr ) ) < 0 ) {
    perror( "bind" );
    exit( 1 );
  }

  if ( listen( fd1, 5 ) < 0 ) {
    perror( "listen" );
    exit( 1 );
  }

  while( 1 ) {
    len = sizeof( caddr );
    if ( ( fd2 = accept( fd1, ( struct sockaddr * )&caddr, ( socklen_t * )&len ) ) < 0 ) {
      perror( "accept" );
      exit( 1 );
    }
    fprintf( stderr, "Connection established: socket %d used.\n", fd2 );
    fprintf( stderr, "Client: IP=%s, PORT=%d.\n",
	     inet_ntoa( caddr.sin_addr ), ntohs(caddr.sin_port) );

    while( fgets( buf, 1024, stdin ) ) {
      write( fd2, buf, strlen( buf )+1 );
      fsync( fd2 );
      len = read( fd2, buf, 1024 );
      buf[len] = '\0';
      fprintf( stdout, "%s", buf );
    }

    close( fd2 );
  }

  close( fd1 );

  return 0;
}
