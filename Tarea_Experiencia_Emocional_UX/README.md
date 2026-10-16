# Experiencia emocional del usuario · Pantalla «Mapa» (B-4)

**Universidad Técnica de Ambato · Facultad de Ingeniería en Sistemas, Electrónica e Industrial**
Carrera de Software · 5to «A» · Interacción Humano-Computador
Tarea grupal T2.1 · Emoción y experiencia de usuario · Entrega: viernes 16 de octubre de 2026

- Caso de estudio: [`B-4-mapa.png.jpeg`](https://github.com/juANO2202/HCI-2026-G1/blob/main/prototipos/original/B-4-mapa.png.jpeg) (repositorio del Grupo 1)
- Prototipo en Figma: <https://www.figma.com/design/qHv7b4pqeDrXumpQNNd2FN>
- Informe: [`informe/informe_final.pdf`](informe/informe_final.pdf)

## Integrantes, roles y contribuciones

| Integrante | Rol | Tareas realizadas | Archivos a su cargo |
|---|---|---|---|
| Emilio Abril | Coordinación e informe | Integración del informe en formato APES y README | `README.md`, `informe/` |
| Manuel Cusme | Inspección (Actividad 1) | Tarea, 5 momentos, capturas numeradas C1–C6, contraste WCAG | `evidencias/original/` |
| William Martínez | Curva emocional (Actividad 2) | Curva emocional esperada y momentos críticos | `curva_emocional/` |
| Pablo Lozada | Matriz UX (Actividad 3) | Matriz momento/emoción/evidencia/mejora y fundamentos IHC | `matriz/`, `scripts/` |
| Jonathan Gamboa | Rediseño y verificación (Actividades 4–5) | Rediseño en Figma, antes/después y verificación por inspección | `rediseño/` |

La participación de cada integrante se verifica en el historial de commits.

## Tarea evaluada

> Tu pedido debe llegar a **Calle Inventada 123, Barrio Ejemplo**. Verifica en el mapa que la ubicación de entrega sea la correcta, corrígela si hace falta y guarda la dirección para continuar al pago.

Momentos: **M1** Ingreso (antes) · **M2** Explorar el mapa · **M3** Ajustar/corregir · **M4** Guardar/confirmar (durante) · **M5** Finalizar (después).

## Hallazgos principales

- **C3 · El mapa contradice la dirección:** el pin está en una manzana distinta a la del «123 · Calle Inventada».
- **C4 · Sin medios para corregir:** no hay buscador ni pista de arrastre; zoom de 32×30 px con contraste de 2,2:1.
- **C5–C6 · Jerarquía invertida:** «Guardar dirección» parece deshabilitado (2,3:1) y «OMITIR» es 5,4 veces más grande; no hay confirmación.
- **C1–C2 · Desconfianza:** cuenta regresiva y «¡OFERTA ÚNICA!» en un paso de verificación; errores ortográficos.

## Alcance

No se realizaron pruebas con usuarios ajenos al equipo. Por eso la curva emocional es una **curva esperada (hipótesis del equipo a partir de la inspección)** y no una medición, y la verificación del rediseño se hizo **por inspección** con criterios medibles: contraste, tamaño de objetivos, elementos visibles y heurísticas. En `evidencias/pruebas_usuarios/` queda un instrumento de prueba preparado para validar la curva con participantes reales.

## Rediseño (M1–M8) y verificación

| Criterio | Original | Rediseño |
|---|---|---|
| Contraste del botón principal | 2,3:1 | 6,6:1 |
| Tamaño de los botones de zoom | 32 × 30 px | 44 × 44 px |
| El pin coincide con la dirección | No | Sí, con indicador |
| Medios visibles para corregir | 0 | 3 |
| Retroalimentación al guardar | Ninguna | Mensaje, ✓ y «Deshacer» |
| Elementos de urgencia | 3 | 0 |

## Estructura

```
Tarea_Experiencia_Emocional_UX/
├── README.md
├── evidencias/
│   ├── original/            capturas originales, anotadas y numeradas (C1–C6)
│   └── pruebas_usuarios/    instrumento y protocolo preparados (no aplicados)
├── curva_emocional/curva_emocional.png
├── matriz/matriz_ux.xlsx
├── rediseño/                antes_despues.png, enlace_figma.md y estados del rediseño
├── informe/informe_final.pdf (y .docx, formato APES)
└── scripts/                 generación de la curva, la matriz y el informe
```

## Regenerar

```bash
pip install matplotlib openpyxl python-docx
python3 scripts/generar_curva_y_matriz.py
python3 scripts/generar_informe_apes.py --repo https://github.com/<usuario>/<repositorio>
soffice --headless --convert-to pdf --outdir informe informe/informe_final.docx
```
