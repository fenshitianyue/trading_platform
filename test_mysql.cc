#include <iostream>
#include <string>
#include <cstdio>
#include <mysql/mysql.h>


int main() {
  MYSQL mysql; 
  int result;
  std::string user_name("test_name");
  char sql[64] = {0};
  sprintf(sql, "select dev_name from dev where dev_name = '%s'", user_name.data()); 
  //MySQL初始化
  mysql_init(&mysql);
  //连接数据库itkim
  if(mysql_real_connect(&mysql, "localhost", "root", "nihao.", "itkim", 0, NULL, 0)) {
    
    result = mysql_query(&mysql, sql); 
    if(result) {
      //成功
      std::cout << "用户名存在！" << std::endl;
    } else {
      //失败
      std::cout << "用户名不存在！" << std::endl;
    }
  } else {
    std::cout << "MySQL连接失败！" << std::endl;
  }
  //关闭MySQL句柄
  mysql_close(&mysql);
  return 0;
}
