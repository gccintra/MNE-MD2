#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

// --- Variáveis Globais para Controle da Visão ---
double zoom = 1.0;
double centerX = -0.75;
double centerY = 0.0;
const int MAX_ITERATIONS = 200;
const int WINDOW_WIDTH = 800;
const int WINDOW_HEIGHT = 600;

// --- Protótipos das Funções ---
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset);
std::string readFile(const char* filePath);
GLuint createShaderProgram(const char* vertexSrc, const char* fragmentSrc);

int main() {
    // 1. Inicializar GLFW e criar a janela
    if (!glfwInit()) {
        std::cerr << "Falha ao inicializar GLFW" << std::endl;
        return -1;
    }
    GLFWwindow* window = glfwCreateWindow(WINDOW_WIDTH, WINDOW_HEIGHT, "Mandelbrot com Zoom", NULL, NULL);
    if (!window) {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    // 2. Inicializar GLEW
    if (glewInit() != GLEW_OK) {
        std::cerr << "Falha ao inicializar GLEW" << std::endl;
        return -1;
    }

    // 3. Carregar e compilar os shaders
    std::string vertexShaderSrc = readFile("shaders/mandelbrot.vert");
    std::string fragmentShaderSrc = readFile("shaders/mandelbrot.frag");
    GLuint shaderProgram = createShaderProgram(vertexShaderSrc.c_str(), fragmentShaderSrc.c_str());

    // 4. Criar um retângulo que preenche a tela (VBO/VAO)
    float vertices[] = { -1.0f, -1.0f,  1.0f, -1.0f,  1.0f,  1.0f, -1.0f, -1.0f,  1.0f,  1.0f, -1.0f,  1.0f };
    GLuint VAO, VBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    // 5. Configurar o callback do scroll do mouse para o zoom
    glfwSetScrollCallback(window, scroll_callback);

    // 6. Loop Principal de Renderização
    while (!glfwWindowShouldClose(window)) {
        // Movimentação com o teclado (Panning)
        double moveSpeed = 0.05 / zoom;
        if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) centerY += moveSpeed;
        if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) centerY -= moveSpeed;
        if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) centerX -= moveSpeed;
        if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) centerX += moveSpeed;
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) glfwSetWindowShouldClose(window, true);

        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(shaderProgram);

        // Enviar as variáveis (uniforms) para o shader
        glUniform2d(glGetUniformLocation(shaderProgram, "u_resolution"), (double)WINDOW_WIDTH, (double)WINDOW_HEIGHT);
        glUniform2d(glGetUniformLocation(shaderProgram, "u_center"), centerX, centerY);
        glUniform1d(glGetUniformLocation(shaderProgram, "u_zoom"), zoom);
        glUniform1i(glGetUniformLocation(shaderProgram, "u_max_iterations"), MAX_ITERATIONS);

        // Desenhar
        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 6);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // Limpeza
    glDeleteProgram(shaderProgram);
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glfwTerminate();
    return 0;
}

// Implementação da função de callback para o scroll
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset) {
    if (yoffset > 0) zoom *= 1.2;    // Zoom In
    else if (yoffset < 0) zoom /= 1.2; // Zoom Out
}

// Implementação da função para ler arquivos
std::string readFile(const char* filePath) {
    std::ifstream fileStream(filePath);
    if (!fileStream.is_open()) {
        std::cerr << "Erro ao ler o arquivo: " << filePath << std::endl;
        return "";
    }
    std::stringstream buffer;
    buffer << fileStream.rdbuf();
    return buffer.str();
}

// Implementação da função para criar o programa de shader
GLuint createShaderProgram(const char* vertexSrc, const char* fragmentSrc) {
    // Compilar shaders
    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexSrc, NULL);
    glCompileShader(vertexShader);

    GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentSrc, NULL);
    glCompileShader(fragmentShader);

    // Linkar shaders
    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    // Deletar shaders, pois já estão linkados
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    return shaderProgram;
}