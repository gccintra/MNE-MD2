#version 330 core
#extension GL_ARB_gpu_shader_fp64 : require // Necessário para tipos double em GLSL < 4.00

out vec4 FragColor;

uniform dvec2 u_resolution; // Alterado para dvec2 (double)
uniform dvec2 u_center;     // Alterado para dvec2 (double)
uniform double u_zoom;      // Alterado para double
uniform int u_max_iterations;

// Função para gerar cores bonitas
vec3 getColor(int i) {
    if (i == u_max_iterations) {
        return vec3(0.0, 0.0, 0.0); // Preto para o interior do conjunto
    }
    // Cálculos de cor usando double para consistência, resultado convertido para vec3 (float)
    double t = double(i) / double(u_max_iterations);
    double r = 9.0 * (1.0 - t) * t * t * t;
    double g = 15.0 * (1.0 - t) * (1.0 - t) * t * t;
    double b = 8.5 * (1.0 - t) * (1.0 - t) * (1.0 - t) * t;
    return vec3(r, g, b);
}

void main() {
    // Mapeia a coordenada do pixel para o plano complexo
    dvec2 uv = (dvec2(gl_FragCoord.xy) - 0.5 * u_resolution) / u_resolution.y; // Usa dvec2

    // Aplica o zoom e o deslocamento (pan)
    dvec2 c = u_center + uv / u_zoom; // Usa dvec2

    // Algoritmo de Mandelbrot
    dvec2 z = dvec2(0.0); // Usa dvec2
    int i;
    for (i = 0; i < u_max_iterations; i++) {
        double x = (z.x * z.x - z.y * z.y) + c.x; // Usa double
        double y = (2.0 * z.x * z.y) + c.y;       // Usa double
        if (x * x + y * y > 4.0) { // 4.0 será promovido para double na comparação
            break;
        }
        z.x = x;
        z.y = y;
    }

    // Colore o pixel
    FragColor = vec4(getColor(i), 1.0);
}