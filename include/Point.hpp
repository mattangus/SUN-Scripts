

template <typename T>
class Point
{
private:
public:
    T x;
    T y;
    Point(T x, T y) : x(x), y(y) { }
    Point() : x(0), y(0) { }
    ~Point() { }
};