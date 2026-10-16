"""Contenido compartido por los scripts del informe (inspección, hipótesis y verificación).

IMPORTANTE: los valores de la curva son una HIPÓTESIS del equipo construida a partir de la
inspección experta. No son mediciones con usuarios. Las métricas de verificación sí son
medidas sobre los diseños (colores, tamaños y elementos visibles).
"""

FIGMA = "https://www.figma.com/design/qHv7b4pqeDrXumpQNNd2FN"
ORIGINAL_URL = "https://github.com/juANO2202/HCI-2026-G1/blob/main/prototipos/original/B-4-mapa.png.jpeg"

TAREA = ("Tu pedido debe llegar a Calle Inventada 123, Barrio Ejemplo. Verifica en el mapa que la ubicación "
         "de entrega sea la correcta, corrígela si hace falta y guarda la dirección para continuar al pago.")

INTEGRANTES = [
    ("Abril Lara Emilio Alexander", "Emilio Abril", "Coordinación, informe y README", "README.md, informe/"),
    ("Cusme Manuel", "Manuel Cusme", "Inspección del prototipo y evidencias numeradas (Actividad 1)", "evidencias/original/"),
    ("Martínez William", "William Martínez", "Curva emocional esperada (Actividad 2)", "curva_emocional/"),
    ("Lozada Pablo", "Pablo Lozada", "Matriz UX y fundamentos IHC (Actividad 3)", "matriz/, scripts/"),
    ("Gamboa Jonathan", "Jonathan Gamboa", "Rediseño en Figma y verificación (Actividades 4 y 5)", "rediseño/"),
]

# esperado_antes / esperado_despues: escala −3 (muy negativa) a +3 (muy positiva) — HIPÓTESIS
MOMENTOS = [
    dict(id="M1", nombre="Ingreso", fase="Antes", captura="C1, C2",
         que_hace="Llega al paso 4 «Mapa» y recibe la primera impresión.",
         emocion="Presión / desconfianza", esperado_antes=-1, esperado_despues=1,
         evidencia="Banner rojo «¡OFERTA ÚNICA!», cuenta regresiva 09:59 activa y «¡¡No pierdas la Ofertta!!» en un paso de verificación; "
                   "errores ortográficos y tres tipografías mezcladas; el título no dice qué hacer.",
         mejora="M1: encabezado sobrio y aviso de precio reservado, sin cuenta regresiva. M3: título orientado a la tarea con una instrucción breve.",
         principio="Nielsen H8 (diseño estético y minimalista) y H2; diseño emocional, nivel visceral [1]; evitar patrones engañosos de urgencia [7].",
         emocion_despues="Tranquilidad"),
    dict(id="M2", nombre="Explorar el mapa", fase="Durante", captura="C3",
         que_hace="Busca su dirección en el mapa y la compara con el pin.",
         emocion="Confusión / duda", esperado_antes=-2, esperado_despues=2,
         evidencia="El pin rojo está en la manzana superior derecha y el marcador «123 · Calle Inventada» en la inferior izquierda: "
                   "el mapa contradice la dirección escrita. El pin es solo un contorno, sin etiqueta.",
         mejora="M4: pin sólido sobre el lote de la dirección, lote resaltado, etiqueta «Tu entrega» e indicador «El pin coincide / está lejos de la dirección».",
         principio="Nielsen H1 (visibilidad del estado) y H2 (coincidencia con el mundo real); Gestalt de proximidad; brecha de evaluación [2].",
         emocion_despues="Confianza"),
    dict(id="M3", nombre="Ajustar / corregir", fase="Durante", captura="C4",
         que_hace="Intenta mover, buscar o corregir la ubicación.",
         emocion="Frustración", esperado_antes=-3, esperado_despues=1,
         evidencia="No hay buscador ni señal de que el pin se pueda arrastrar; los controles de zoom miden 32×30 px, no tienen etiqueta y su contraste es 2,2:1.",
         mejora="M4: buscador de dirección y «Usar mi ubicación». M5: pista «Arrastra el pin para ajustarlo» y zoom de 44×44 px con borde.",
         principio="Nielsen H3 (control y libertad), H6 (reconocer antes que recordar) y H7; significantes [2]; Ley de Fitts [6]; WCAG 2.2 · 1.4.11 y 2.5.5 [4].",
         emocion_despues="Control"),
    dict(id="M4", nombre="Guardar / confirmar", fase="Durante", captura="C5, C6",
         que_hace="Guarda o confirma la dirección de entrega.",
         emocion="Incertidumbre", esperado_antes=-2, esperado_despues=2,
         evidencia="«Guardar dirección» es gris sobre beige (2,3:1) y parece deshabilitado; al pulsarlo no ocurre nada visible. "
                   "«OMITIR »» es 5,4 veces más grande y es la única forma de avanzar.",
         mejora="M7: un único botón primario «Confirmar ubicación y continuar» (460×60 px, 6,6:1); se elimina «OMITIR» y «Volver» queda como acción secundaria.",
         principio="Nielsen H5 (prevención de errores); jerarquía visual y figura-fondo (Gestalt); WCAG 2.2 · 1.4.3 [4]; Ley de Fitts [6].",
         emocion_despues="Seguridad"),
    dict(id="M5", nombre="Finalizar", fase="Después", captura="C6, B-5",
         que_hace="Pasa al pago y valora si su dirección quedó guardada.",
         emocion="Inseguridad", esperado_antes=-1, esperado_despues=2,
         evidencia="Tras guardar u omitir no hay mensaje de confirmación y el indicador de pasos no marca pasos completados; "
                   "solo en el paso 5 se vuelve a ver la dirección en el resumen.",
         mejora="M8: mensaje «Ubicación guardada correctamente» con la dirección y «Deshacer»; el paso 4 se marca con ✓. M2: indicador de pasos con estado.",
         principio="Nielsen H1 (retroalimentación) y H3 (deshacer); diseño emocional, nivel reflexivo [1]; satisfacción según ISO 9241-11 [5].",
         emocion_despues="Satisfacción"),
]

PROBLEMAS = [
    ("C1", "Urgencia artificial", "Banner rojo, «¡OFERTA ÚNICA!», cuenta regresiva 09:59 y «¡¡No pierdas la Ofertta!!» en un paso que pide revisar con calma."),
    ("C2", "Baja credibilidad", "Errores ortográficos («Ofertta» dos veces, «dia» sin tilde), «ayuda??» y tres familias tipográficas mezcladas."),
    ("C3", "El mapa contradice la dirección", "El pin está en una manzana distinta a la del marcador «123 · Calle Inventada»."),
    ("C4", "Sin medios para corregir", "No hay buscador ni pista de arrastre; zoom de 32×30 px, sin etiqueta y con contraste de 2,2:1."),
    ("C5", "Guardar parece deshabilitado", "Texto gris sobre beige (2,3:1) y sin respuesta visible al pulsarlo."),
    ("C6", "Jerarquía invertida", "«OMITIR »» domina la pantalla, es la única forma de avanzar y no hay confirmación final."),
]

MEJORAS = [
    ("M1", "Encabezado sobrio y aviso de precio reservado, sin cuenta regresiva", "C1, C2"),
    ("M2", "Indicador de pasos con estado (✓ en los completados, «Paso 4 de 5»)", "C6"),
    ("M3", "Título orientado a la tarea e instrucción breve", "C1"),
    ("M4", "Buscador, «Usar mi ubicación», pin alineado y arrastrable, indicador de coincidencia", "C3, C4"),
    ("M5", "Zoom de 44×44 px con borde y pista «Arrastra el pin para ajustarlo»", "C4"),
    ("M6", "Panel con dirección, referencia para el repartidor y costos completos", "C2, C3"),
    ("M7", "Un solo botón primario «Confirmar ubicación y continuar»; se elimina «OMITIR»", "C5, C6"),
    ("M8", "Mensaje de confirmación con «Deshacer» y paso 4 marcado como completado", "C6"),
]

# Verificación por inspección: (criterio, original, rediseño, referencia)
VERIFICACION = [
    ("Contraste del botón para guardar/confirmar", "2,3:1", "6,6:1", "WCAG 1.4.3 (≥ 4,5:1)"),
    ("Contraste de los controles de zoom", "2,2:1", "4,0:1 (borde) · 16,5:1 (ícono)", "WCAG 1.4.11 (≥ 3:1)"),
    ("Contraste de la etiqueta «Dirección»", "3,3:1", "7,8:1", "WCAG 1.4.3 (≥ 4,5:1)"),
    ("Tamaño de los botones de zoom", "32 × 30 px", "44 × 44 px", "WCAG 2.5.5 (44 × 44 px)"),
    ("Tamaño del botón para guardar/confirmar", "142 × 30 px", "460 × 60 px", "Ley de Fitts"),
    ("Tamaño de «OMITIR» frente al botón de guardar", "5,4 veces mayor", "«OMITIR» eliminado", "Nielsen H5"),
    ("El pin coincide con la dirección escrita", "No", "Sí, con indicador de estado", "Nielsen H1, H2"),
    ("Medios visibles para corregir la ubicación", "0", "3 (buscar, mi ubicación, arrastrar)", "Nielsen H3, H6"),
    ("Retroalimentación al guardar", "Ninguna", "Mensaje, ✓ en el paso y «Deshacer»", "Nielsen H1, H3"),
    ("Elementos de urgencia o presión", "3", "0", "Patrones engañosos [7]"),
    ("Errores ortográficos visibles", "3", "0", "Credibilidad"),
    ("Familias tipográficas", "3", "1", "Nielsen H4"),
    ("Heurísticas de Nielsen con hallazgos", "8 de 10", "Atendidas en el diseño", "Ver tabla 6"),
]

HEURISTICAS = [
    ("H1 · Visibilidad del estado", "No confirma el guardado; los pasos no muestran cuáles están completos.", "Mensaje de confirmación, ✓ en los pasos e indicador de coincidencia del pin."),
    ("H2 · Coincidencia con el mundo real", "El mapa contradice la dirección; para avanzar se pulsa «OMITIR».", "Pin sobre la dirección; botón «Confirmar ubicación y continuar»."),
    ("H3 · Control y libertad", "No hay forma visible de corregir ni de deshacer.", "Buscador, arrastre del pin, «Deshacer» y «Volver»."),
    ("H4 · Consistencia y estándares", "Tres tipografías; enlaces subrayados junto a una pestaña verde.", "Una tipografía y estilos de botón consistentes."),
    ("H5 · Prevención de errores", "«OMITIR» dominante permite saltarse la verificación.", "Se elimina «OMITIR»; aviso cuando el pin está lejos de la dirección."),
    ("H6 · Reconocer antes que recordar", "Nada indica que el pin se puede arrastrar.", "Pista visible «Arrastra el pin para ajustarlo»."),
    ("H8 · Diseño estético y minimalista", "Banners de urgencia y mensajes que compiten con la tarea.", "Se retiran; queda solo la información de la tarea."),
    ("H10 · Ayuda y documentación", "Enlace «ayuda??» poco serio y sin instrucciones en pantalla.", "«Ayuda» y una instrucción breve bajo el título."),
]

CONTRASTES = [
    ("«Guardar dirección»", "Original", "#888772", "#CECFAD", "≥ 4,5:1 (1.4.3)"),
    ("Botones de zoom (+/−)", "Original", "#8E8B78", "#CFD0A8", "≥ 3:1 (1.4.11)"),
    ("Etiqueta «Dirección»", "Original", "#8A8B00", "#F2FF00", "≥ 4,5:1 (1.4.3)"),
    ("Botón «Confirmar ubicación»", "Rediseño", "#FFFFFF", "#1F4FD8", "≥ 4,5:1 (1.4.3)"),
    ("Texto secundario", "Rediseño", "#4A5363", "#FFFFFF", "≥ 4,5:1 (1.4.3)"),
    ("Estado «El pin coincide»", "Rediseño", "#17693E", "#E7F5EC", "≥ 4,5:1 (1.4.3)"),
    ("Borde de zoom y campos", "Rediseño", "#767F90", "#FFFFFF", "≥ 3:1 (1.4.11)"),
]

REFERENCIAS = [
    "D. A. Norman, Emotional Design: Why We Love (or Hate) Everyday Things. New York, NY, USA: Basic Books, 2004.",
    "D. A. Norman, The Design of Everyday Things, ed. revisada y ampliada. New York, NY, USA: Basic Books, 2013.",
    "J. Nielsen, “10 usability heuristics for user interface design,” Nielsen Norman Group, 1994. [En línea]. Disponible: https://www.nngroup.com/articles/ten-usability-heuristics/",
    "World Wide Web Consortium (W3C), “Web Content Accessibility Guidelines (WCAG) 2.2,” W3C Recommendation, oct. 2023. [En línea]. Disponible: https://www.w3.org/TR/WCAG22/",
    "Ergonomics of human-system interaction — Part 11: Usability: Definitions and concepts, ISO 9241-11:2018, 2018.",
    "P. M. Fitts, “The information capacity of the human motor system in controlling the amplitude of movement,” J. Exp. Psychol., vol. 47, no. 6, pp. 381–391, 1954.",
    "H. Brignull, Deceptive Patterns: Exposing the Tricks Tech Companies Use to Control You. London, UK: Testimonium, 2023.",
    "Grupo 1 HCI-2026, “Prototipo original B-4-mapa,” repositorio HCI-2026-G1, GitHub, 2026. [En línea]. Disponible: " + ORIGINAL_URL,
]


def _lum(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contraste(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return round((la + 0.05) / (lb + 0.05), 1)
