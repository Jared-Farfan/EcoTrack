# Vibe Report – EcoTrack

## 1. Cómo configuré las reglas de mi agente

Lo primero que hice fue crear un archivo `.cursorrules` en la raíz del proyecto
para que la IA entendiera cómo quería trabajar antes de escribir una sola línea.
Lo dividí en cinco bloques: **rol** (la IA es copiloto y ejecutor; yo pongo la
visión), **stack** (Python y Streamlit, sin base de datos), **estilo de código**
(modular, lógica separada de la interfaz y factores de emisión en diccionarios
con nombre y unidad), **flujo de trabajo** (explicar el plan en pocas líneas,
hacer cambios pequeños y corregir los errores sin pedirme tocar el código) y
**vibe del producto** (tono amable, paleta verde, resultados con desglose).
Después conecté el proyecto con Replit para probar y desplegar en la nube, y
usé Claude Sonnet dentro de Cursor como motor principal. 

## 2. Dificultades al delegar el código a la IA

- **Prompts vagos, resultados vagos.** Mi primera instrucción fue muy general y
  la IA inventó factores de emisión sin unidades. Tuve que volver a pedirlos con
  nombre y unidad.
- **Ambigüedad del lenguaje natural.** Una frase como "viajé 20 km" no dice en
  qué medio. Tuve que decidir un valor por defecto y dejarlo documentado.
- **Confianza en resultados que "se ven bien".** La app corría sin errores, pero
  los números eran aproximados. Aprendí a no darlos por válidos solo porque el
  código funcionaba, y por eso la interfaz avisa que son estimaciones.
- **Diferencias entre local y nube.** Al llevar la app a Replit tuve que ajustar
  el puerto y las dependencias. Le pasé el error a la IA, describí el problema
  y ella propuso la corrección. 

## 3. De escribir código a orquestar una visión

Pasé de preguntarme "¿cómo escribo esta función?" a preguntarme "¿qué quiero que
haga el producto y cómo voy a comprobar que lo hace bien?". Se siente más
parecido a dirigir que a ejecutar: mi trabajo fue definir la intención, poner
límites claros y revisar con ojo crítico lo que la IA entregaba.

Lo más liberador fue la velocidad: pude validar la idea de EcoTrack en horas y
dedicar mi atención al diseño y a la experiencia de usuario. Lo más exigente fue
comunicar con precisión, porque la calidad del resultado dependía directamente de
la calidad de mis instrucciones.

Mi conclusión es que delegar el código no elimina la responsabilidad, sino que la
mueve hacia el diseño, la verificación y las decisiones de producto. La IA
escribe rápido, pero la visión y el criterio siguen siendo míos.
