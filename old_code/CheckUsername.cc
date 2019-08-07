#include <iostream>
#include <fstream>
#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <mysql/mysql.h>
using namespace std;

//1.连接MySQL数据库
//2.获取前端发送的 username TODO
//3.在数据库中查找username
//4.将查询成功与否信息按照一定格式发送给前端 TODO

void WriteSomething(char* buf, int size) {
	ofstream file("./test");		
	if(file.is_open()) {
		file.write(buf, size);
	}
	file.close();
}

void GetQueryString(char* buf, int* content_length) {
	char* p = getenv("CONTENT_LENGTH");
	if(NULL == p) {
		char error_msg[64] = "获取content-length失败";
		WriteSomething(error_msg, sizeof(error_msg));
		return;
	}	
	*content_length = atoi(p);
	for(int i = 0; i < *content_length; ++i) {
		read(0, &buf[i], 1);
	}
	buf[*content_length] = '\0';
}

int main(){
	MYSQL mysql;
	int result;
	int content_length = 0;
	char buf[64] = {0};
	char user_name[20] = {0};	
	char sql[128] = {0};
	//MySQL初始化
	mysql_init(&mysql);
	//TODO：从前端获取username
	GetQueryString(buf, &content_length);
	sscanf(buf, "username=%s", user_name);	
	WriteSomething(user_name, content_length);
	sprintf(sql, "select dev_name from dev where dev_name = '%s'", user_name);
	if(mysql_real_connect(&mysql, "localhost", "root", "nihao.", "itkim", 0, NULL, 0)) {
		result = mysql_query(&mysql, sql);
		if(result) {
			//用户名存在
		} else {
			//用户名不存在
		}
	}
	//TODO：将查询结构返回给前端
	//关闭MySQL句柄	
	mysql_close(&mysql);
	return 0;
}
