TARGET = mandelbrot
CXX = g++
CXXFLAGS = -std=c++17 -g -Wall
LIBS = -lGLEW -lglfw -lGL

all: $(TARGET)

$(TARGET): mandelbrot.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) mandelbrot.cpp $(LIBS)

clean:
	rm -f $(TARGET)
