#include <iostream>
#include <string>
#include <cstdio>

int main() {
  std::string user_name("test_name"); 
  char sql[64] = {0};
  sprintf(sql, "select dev_name from dev where dev_name = '%s'", user_name.data());
  std::cout << "sql = " << sql << std::endl;
  return 0;
}
