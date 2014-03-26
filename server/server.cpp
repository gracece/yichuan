/* A simple server in the internet domain using TCP
   The port number is passed as an argument */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <time.h>


void error(const char *msg)
{
    perror(msg);
    exit(1);
}


int main(int argc, char *argv[])
{
    int sockfd, newsockfd, portno,on,ret;
    socklen_t clilen;
    char buffer[2048];
    struct sockaddr_in serv_addr, cli_addr;
    int n;
    if (argc < 2) {
        portno = 10086;
    }
    else
        portno = atoi(argv[1]);

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    on =1;
    ret = setsockopt(sockfd,SOL_SOCKET,SO_REUSEADDR,&on,sizeof(on));
    if (sockfd < 0) 
        error("ERROR opening socket");
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
                sizeof(serv_addr)) < 0) 
        error("ERROR on binding");
    listen(sockfd,5);
    clilen = sizeof(cli_addr);
    newsockfd = accept(sockfd, 
            (struct sockaddr *) &cli_addr, 
            &clilen);
    if (newsockfd < 0) 
        error("ERROR on accept");
    bzero(buffer,2048);
    while (1) {
        n = read(newsockfd,buffer,2047);
        if (n < 0) {
            error("ERROR reading from socket");
            break;
        }

        buffer[n] =0;

        char line[1024];
        int index=0;
        int i=0;
        FILE *fp;
        fp = fopen("../line.txt", "a+");
        for (i = 0;  i < strlen(buffer);  i++) {
            if (buffer[i]=='$') {
                line[index] = '\0';
                index = 0;
                fprintf(fp, "%u#",(unsigned)time(NULL));
                char data[4][10];
                int index_data = 0;
                int tmp =0;

                printf("line %s\n", line);
                memset(data,0,sizeof(data));
                for (int j = 0; j < strlen(line); j++) {
                    if (line[j]==',' or line[j] == '\0') {
                        data[tmp][index_data] = '\0';
                        tmp++;
                        index_data = 0;
                    }
                    else {
                        data[tmp][index_data] = line[j];
                        index_data++;
                    }
                }

                fprintf(fp, "{\"x1\":%s,\"y1\":%s,\"x2\":%s,\"y2\":%s}\n",data[0],data[1],data[2],data[3]);
                printf( "{\"x1\":%s,\"y1\":%s,\"x2\":%s,\"y2\":%s}\n",data[0],data[1],data[2],data[3]);
            }
            else {
                line[index] = buffer[i];
                index ++;
            }
        }
        fclose(fp);


            printf("%i\n", n);
        printf("Here is the  message: %s\n\n",buffer);
        n = write(newsockfd,"I got your message",18);
        if (n < 0) error("ERROR writing to socket");
    }
    close(newsockfd);
    close(sockfd);
    return 0; 
}
