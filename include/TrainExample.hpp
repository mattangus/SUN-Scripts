#pragma once
#include <opencv2/opencv.hpp>
#include <vector>
#include <string>

#include "Point.hpp"
#include "MetaParser.hpp"

class TrainExample
{
private:
    std::string imgFile;
    std::string annotFile;
public:
    cv::Mat image;
    cv::Mat annot;
    std::string name;
    std::vector<Point<int>> pts;
    std::string username;

    TrainExample(std::string imgFile, std::string annotFile) :
        imgFile(imgFile), annotFile(annotFile) { }

    ~TrainExample() { }

    static TrainExample makeExample(std::string imgFile, std::string annotFile)
    {
        TrainExample ex(imgFile, annotFile);

        ex.load();
    }

    void load()
    {
        
    }
};