#include <iostream>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
//#include <ctemplate/template.h>

int GetQueryString(char output[]) {
  // 1. 先从环境变量中获取到方法
  char* method = getenv("REQUEST_METHOD");
  if (method == NULL) {
    fprintf(stderr, "REQUEST_METHOD failed\n");
    return -1;
  }
  // 2. 如果是 GET 方法, 就是直接从环境变量中
  //    获取到 QUERY_STRING
  if (strcasecmp(method, "GET") == 0) {
    char* query_string = getenv("QUERY_STRING");
    if (query_string == NULL) {
      fprintf(stderr, "QUERY_STRING failed\n");
      return -1;
    }
    strcpy(output, query_string + 2); //去掉 1=
  } else {
    // 3. 如果是 POST 方法, 先通过环境变量获取到 CONTENT_LENGTH
    //    再从标准输入中读取 body
    char* content_length_str = getenv("CONTENT_LENGTH");
    if (content_length_str == NULL) {
      fprintf(stderr, "CONTENT_LENGTH failed\n");
      return -1;
    }
    int content_length = atoi(content_length_str);
    int i = 0;  // 表示当前已经往  output 中写了多少个字符了
    for (; i < content_length; ++i) {
      read(0, &output[i], 1);
    }
    output[content_length] = '\0';
  }
  return 0;
}

void ParseResponse(){
  //ctemplate::TemplateDictionary page("TestPage");
  //ctemplate::Template* tpl = ctemplate::Template::GetTemplate("./template/user_main.html", ctemplate::DO_NOT_STRIP);
  //std::string html;
  //tpl->Expand(&html, &page);
  char buf[1024] = {0};  
  GetQueryString(buf);
  std::cout << buf;
}

int main() {
  ParseResponse(); 
  return 0;
}
