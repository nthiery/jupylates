#ifndef RANDOMIZATION_H
#define RANDOMIZATION_H

#include <iostream>
#include <cstdlib>
#include <vector>
#include <functional>
#include <sstream>

/** Infrastructure minimale de test **/
#ifndef ASSERT
#define ASSERT(test) if (!(test)) { throw std::runtime_error("\\x1b[48;5;224mTest failed: "#test); }
#endif
#ifndef CHECK
#define CHECK(test) if ( !(test) ) { throw std::runtime_error("\\x1b[48;5;224mTest failed: "#test); }
#endif

// TODO: how to initialize the seed?

// TODO: randomize ???
#define PLUSOUMOINS +

// TODO: randomize ???
#define VALOUREF &

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

template<class T>
T INPUT(T t) {
    return t;
}

template<class T>
void INPUT_EXPR(std::string description, T& answer, T& solution, T answer_value, T solution_value) {
    answer = answer_value;
    solution = solution_value;
}

template<class T>
void INPUT_EXPR(std::string description, T& answer, T& solution, T solution_value) {
    answer = solution_value;
    solution = solution_value;
}

#define INPUT_TEXT INPUT_EXPR<std::string>
#define INPUT_INT INPUT_EXPR<int>
#define INPUT_FLOAT INPUT_EXPR<float>
#define INPUT_BOOL INPUT_EXPR<bool>

template<class T>
std::string to_literal(T i) {
    std::ostringstream s;
    s << i;
    return s.str();
}
// Will need to be overriden for vectors, ...


void SUBSTITUTE(std::string name, std::string value) {
    std::cout << "{\"" << name << "\": \"" << value << "\"}" << std::endl;
}

template<class T>
void SUBSTITUTE_LITERAL(std::string name, T value) {
    SUBSTITUTE(name, to_literal(value));
}

#endif
