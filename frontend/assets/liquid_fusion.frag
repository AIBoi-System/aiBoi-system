//assets/liquid_fusion.frag

#include <flutter/runtime_effect.glsl>

uniform vec2 u_currentPos;   // Posição do indicador ativo
uniform vec2 u_nextPos;      // Posição do próximo indicador (durante o swipe)
uniform float u_radius;      // Raio da bolinha
uniform vec4 u_color;        // Cor do indicador

out vec4 fragColor;

float metaball_influence(vec2 p, vec2 center, float radius) {
    float d = distance(p, center);
    // Função de influência suave (blur)
    // 1 / (d/r)² é um ponto de partida, mas funções mais suaves são melhores
    float power = radius / d;
    return power * power; // Usamos power² para um "blur" mais agressivo que funde melhor
}

void main() {
    vec2 p = FlutterFragCoord().xy;

    // Calcula a influência das duas bolinhas
    float influence = metaball_influence(p, u_currentPos, u_radius);
    influence += metaball_influence(p, u_nextPos, u_radius);

    // Valor limite (Threshold). Ajuste para mais/menos viscosidade.
    // Maior valor = bolinhas menores, menor fusão.
    // Menor valor = bolinhas maiores, mais fusão ("viscosidade").
    float threshold = 0.5;

    if (influence > threshold) {
        fragColor = u_color;
    } else {
        fragColor = vec4(0.0); // Transparente
    }
}