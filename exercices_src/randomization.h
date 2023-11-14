#include <iostream>
#include <cstdlib>
#include <vector>
#include <functional>

/** Infrastructure minimale de test **/
#define ASSERT(test) if (!(test)) std::cout << "Test failed in file " << __FILE__ \
				            << " line " << __LINE__ << ": " #test << std::endl
#define CHECK(C) if ( !(C) ) { throw std::runtime_error("\\x1b[48;5;224mTest failed: "#C); }
// TODO: how to initialize the seed?

// TODO: randomize ???
#define PLUSOUMOINS +

#define CONST const auto

// TODO: randomize ???
#define X x
#define Y y
#define Z z

int RANDOM_INT(int min, int max) {
    return min + (rand() % (max - min + 1));
}

template<typename T, typename ... Args>
T RANDOM_CHOICE(const T arg0, const Args... args) {
    const std::vector<T> v({arg0, args...});
    return v[rand() % v.size()];
}

template<typename ... Args>
auto RANDOM_CHOICE(const char * arg0, const Args... args) {
    const std::vector<std::string> v({arg0, args...});
    return v[rand() % v.size()];
}

class RANDOM_VECTOR_CLASS {
    public:
    template <typename F, typename ... Args>
        auto operator ()(int N, F f, Args ... args) {

        using invoke_result_t = typename std::invoke_result<F, Args ...>::type;
        std::vector<invoke_result_t> v(N);
        for (auto &value: v)
            value = f(args...);
        return v;
    }
    /*template<typename ... Args>
        auto operator ()(int N, RANDOM_VECTOR_CLASS f, Args... args) {
        std::vector<std::vector<int>> v(N);
        for (auto &value: v)
            value = f(args...);
        return v;
        }*/
};

RANDOM_VECTOR_CLASS RANDOM_VECTOR;

template<typename T>
std::ostream & operator << (std::ostream& o, const std::vector<T> &v) {
    o << "{";
    if ( v.size() >= 0 ) {
        o << v[0];
        for ( unsigned int i=1; i<v.size(); i++ )
            o << ", " << v[i];
    }
    o << "}";
    return o;
}
