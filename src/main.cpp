#include <iostream>
#include "argparse/argparse.hpp"
#include <string>

#include "spdlog/spdlog.h"

int main(int argc, char const *argv[])
{
    ArgumentParser parser;

    // add some arguments to search for
    parser.addArgument("-b", "--base_path", 1, false);

    // parse the command-line arguments - throws if invalid format
    parser.parse(argc, argv);

    // if we get here, the configuration is valid
    std::string basePath = parser.retrieve<std::string>("base_path");
    
    return 0;
}
