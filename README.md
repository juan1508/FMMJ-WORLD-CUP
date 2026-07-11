# 🏆 FMMJ WORLD CUP UNITED 26

App de Streamlit para el mundial privado entre **Mati**, **Jnka** y **Dibu**.
Anfitriones: México 🇲🇽 (verde), Estados Unidos 🇺🇸 (azul), Canadá 🇨🇦 (rojo).

## ⚠️ Estructura IMPORTANTE (por qué se corrigió el error anterior)
El `FileNotFoundError` que salió en Streamlit Cloud pasó porque la app buscaba
un archivo dentro de una carpeta `data/` que no quedó bien subida a GitHub.

**Esta versión ya NO usa ninguna subcarpeta ni archivo de datos externo obligatorio.**
Los 5 archivos van todos sueltos, en la raíz del repo:

```
app.py
teams_data.py
matches_data.py
requirements.txt
.gitignore
```

- `teams_data.py` y `matches_data.py` tienen los equipos, convocatorias y el
  calendario **escritos directamente en Python** (no se leen de ningún JSON).
- El único archivo que se genera es `tournament_state.json` (donde se guardan
  los resultados y los premios), y **la app lo crea sola automáticamente**
  la primera vez que corre, si no existe. No hace falta subirlo a GitHub.

## Cómo subirlo a GitHub (todo en la raíz, sin carpetas)

```bash
mkdir fmmj-world-cup-united-26
cd fmmj-world-cup-united-26
# copia aquí los 5 archivos: app.py, teams_data.py, matches_data.py, requirements.txt, .gitignore
git init
git add .
git commit -m "FMMJ WORLD CUP UNITED 26 - v2 sin dependencias externas"
git branch -M main
git remote add origin https://github.com/juan1508/fmmj-world-cup-united-26.git
git push -u origin main
```

Si usas la interfaz web de GitHub ("Add file" → "Upload files"), simplemente
arrastra los 5 archivos sueltos — NO crees ninguna carpeta `data/`.

## Desplegar en Streamlit Cloud
1. [share.streamlit.io](https://share.streamlit.io) → New app
2. Repo: `juan1508/fmmj-world-cup-united-26`, branch `main`
3. Main file path: `app.py`
4. Deploy 🚀

## Qué hay en la app
- 8 grupos (32 selecciones) con banderas y presidente dueño de cada selección
- Tabla de posiciones automática
- Calendario de fase de grupos para registrar marcador + goleadores
- **Eliminatorias** con dos vistas:
  - 🎯 **Bracket visual** estilo Champions League (Octavos → Cuartos → Semis → Final, con líneas conectoras y colores por ronda)
  - 📝 Carga de resultados de eliminatorias (con definición por penales si hay empate)
- Convocatoria de 26 jugadores por selección (`L. Apellido`)
- Premios:
  - Bota de Oro automática (según goles cargados)
  - Campeón / Subcampeón / Tercer lugar automáticos
  - **Balón de Oro, Guante de Oro y Mejor Jugador Joven ahora quedan guardados**
    en `tournament_state.json` (antes no se guardaban)

## Nota sobre persistencia
`tournament_state.json` vive en el disco de la instancia de Streamlit Cloud y
persiste mientras la app no se reinicie/redepliegue. Recomendación: cada
cierto tiempo (por ejemplo al terminar una jornada), bajen ese archivo desde
"Manage app" y guárdenlo como respaldo (o súbanlo al repo si quieren que quede
como punto de partida fijo).

## Resetear el torneo
Basta con borrar `tournament_state.json` (o simplemente no subirlo): la app
genera un calendario nuevo desde cero automáticamente en el siguiente run.
