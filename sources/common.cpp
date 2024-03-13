#include "common.h"

#include <filesystem>
#include <format>

#define NO_G3D_ALLOCATOR 1
#include "SIMDString.h"

void
log_info(const char* msg)
{
  printf("[    INFO] /_\\ %s\n", msg);
}

void
log_success(const char* msg)
{
  printf(std::format("\033[0;32m[ SUCCESS] /_\\ {} \033[0m\n", msg).c_str());
}

String
get_output_string(const char* filename, int line)
{
  return String(
    std::format("{} | {}",
                std::filesystem::path(filename).filename().string().c_str(),
                line));
}

void
log_warning(const char* msg, const char* file, int line)
{
  printf(std::format("\033[0;33m[ WARNING] /_\\ {} /_\\ {} \033[0m\n",
                     msg,
                     get_output_string(file, line).c_str())
           .c_str());
}

void
log_error(const char* msg, const char* file, int line)
{
  printf(std::format("\033[0;31m[  FAILED] /_\\ {} /_\\ {} \033[0m\n",
                     msg,
                     get_output_string(file, line).c_str())
           .c_str());
  exit(EXIT_FAILURE);
}