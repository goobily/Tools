#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdarg.h>
#include <string.h>
#include <assert.h>
#include "..\redis\hiredis\hiredis.h"

#pragma comment(lib, "hiredis.lib")

using namespace std;

void doTest()
{
    //redis默认监听端口为6379 可以再配置文件中修改
    redisContext* c = redisConnect("127.0.0.1", 6379);
    if (c->err)
    {
        printf("Connect to redisServer faile:%s\n", c->errstr);
        redisFree(c);
        return;
    }
    printf("Connect to redisServer Success\n");

    const char* command1 = "set John Shuai";
    redisReply* r = (redisReply*)redisCommand(c, command1);

    if (NULL == r)
    {
        printf("Execut command1 failure\n");
        redisFree(c);
        return;
    }
    if (!(r->type == REDIS_REPLY_STATUS && (strcmp(r->str, "OK") == 0 || strcmp(r->str, "ok") == 0)))
    {
        printf("Failed to execute command[%s]\n", command1);
        freeReplyObject(r);
        redisFree(c);
        return;
    }
    freeReplyObject(r);
   // printf("Succeed to execute command[%s]\n", command1);

    const char* command2 = "strlen John";
    r = (redisReply*)redisCommand(c, command2);
    if (r->type != REDIS_REPLY_INTEGER)
    {
        printf("Failed to execute command[%s]\n", command2);
        freeReplyObject(r);
        redisFree(c);
        return;
    }
    int length = r->integer;
    freeReplyObject(r);
    printf("The length of 'John' is %d.\n", length);
   // printf("Succeed to execute command[%s]\n", command2);


    const char* command3 = "get John";
    r = (redisReply*)redisCommand(c, command3);
    if (r->type != REDIS_REPLY_STRING)
    {
        printf("Failed to execute command[%s]\n", command3);
        freeReplyObject(r);
        redisFree(c);
        return;
    }
    printf("The value of 'John' is %s\n", r->str);
    freeReplyObject(r);
   // printf("Succeed to execute command[%s]\n", command3);

    const char* command_select = "select 1";
    r = (redisReply*)redisCommand(c, command_select);
    if (NULL == r) {
        cout << "Failed to execute command[" << command_select << "]" << endl;
        redisFree(c);
        return;
    }
    if (!(r->type == REDIS_REPLY_STATUS && (strcmp(r->str, "OK") == 0 || strcmp(r->str, "ok"))))
    {
        cout << "Failed to execute command[" << command_select << "]" << endl;
        freeReplyObject(r);
        redisFree(c);
        return;
    }
    cout << "Success to execute command[" << command_select << "]" << endl;
    freeReplyObject(r);

    const char* command4 = "set goobily good";
    r = (redisReply*)redisCommand(c, command4);
    if (NULL == r)
    {
        printf("Execut command1 failure\n");
        redisFree(c);
        return;
    }
    if (!(r->type == REDIS_REPLY_STATUS && (strcmp(r->str, "OK") == 0 || strcmp(r->str, "ok") == 0)))
    {
        printf("Failed to execute command[%s]\n", command4);
        freeReplyObject(r);
        redisFree(c);
        return;
    }
    freeReplyObject(r);
   // printf("Succeed to execute command[%s]\n", command4);

    const char* command_keys = "keys * ";
    r = (redisReply*)redisCommand(c, command_keys);
    if (r->type != REDIS_REPLY_ARRAY)
    {
        cout << "Failed to execute command[" << command_keys << "]" << endl;
        freeReplyObject(r);
        redisFree(c);
        return;
    }

    cout << "keys of DB 1 are:" << endl;

    int ele_num = r->elements;
    for (int i = 0; i < ele_num; ++i)
    {
        cout << r->element[i]->str << endl;
    }

    freeReplyObject(r);

    redisFree(c);

}

int main()
{
    //WSADATA wsaData;
    //int nRet;
    //if ((nRet = WSAStartup(MAKEWORD(2, 2), &wsaData)) != 0) {
    //    printf("WSAStartup failed\n");
    //    exit(0);
    //}
    doTest();
    return 0;
}
