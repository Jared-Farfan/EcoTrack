# Vibe Report – EcoTrack

## 1. Cómo configuré las reglas de mi agente
Creé un archivo `.cursorrules` en la raíz del proyecto para que la IA supiera
desde el primer prompt quién es y cómo debe trabajar. Lo organicé en cinco
bloques: rol (copiloto y ejecutor, yo pongo la visión), stack (Python y
Streamlit, sin base de datos), estilo de código (modular, lógica separada de la
interfaz, sin números mágicos), flujo de trabajo (planear en pocas líneas,
corregir errores solo, cambios pequeños) y "vibe" del producto (tono amable,
paleta verde, resultados con desglose). Después conecté el proyecto a Replit
para probar y desplegar en la nube. [COMPLETAR: modelo que usaste en Cursor y
cómo conectaste el repo con Replit.]

## 2. Dificultades al delegar el código a la IA
- **Prompts vagos, resultados vagos:** cuando dije "calcula el CO2" sin más,
  la IA inventó factores sin indicar unidades. Tuve que pedir factores
  nombrados y con unidad.
- **Ambigüedad del lenguaje natural:** frases como "viajé 20km" no dicen el
  medio de transporte. Tuve que decidir un valor por defecto.
- **Confianza ciega:** el código corría, pero los números eran aproximados.
  Aprendí a verificar los resultados y a dejar claro en la interfaz que son
  estimaciones.
- **Entorno distinto:** lo que funcionaba en local necesitó ajustes de puerto
  y dependencias en Replit. [COMPLETAR: el error real que te tocó resolver y
  cómo se lo describiste a la IA.]

## 3. De escribir código a orquestar una visión
[COMPLETAR con tu experiencia real.] Pasé de pensar "¿cómo escribo esta
función?" a pensar "¿qué quiero que haga el producto y cómo lo comprobaré?".
Se siente más cercano a dirigir que a ejecutar: mi trabajo fue definir
intención, límites y criterios de calidad, y revisar con ojo crítico. Lo más
liberador fue iterar rápido; lo más exigente, comunicar con precisión. Mi
conclusión es que delegar código no elimina la responsabilidad: la mueve hacia
el diseño, la verificación y las decisiones de producto.
