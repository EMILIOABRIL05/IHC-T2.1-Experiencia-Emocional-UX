"""Regenera curvas, resumen, contrastes y matriz a partir del CSV publicado."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from procesar_resultados import ROOT, DEFAULT_CSV, cargar_registros, analizar

GRAFICOS = ('curvas_original.png', 'curvas_rediseno.png', 'curva_emocional.png',
            'curvas_pareadas.png', 'mapa_valoraciones.png', 'diferencia_momentos.png',
            'resumen_resultados.csv', 'contraste_visual.png', 'contrastes.csv')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, default=DEFAULT_CSV)
    parser.add_argument('--salida', type=Path, default=ROOT, help='Raíz de salida; se crean curva_emocional/ y matriz/.')
    parser.add_argument('--sin-matriz', action='store_true', help='Regenerar solamente las figuras y los dos CSV.')
    parser.add_argument('--qa-dir', type=Path, help='Guardar vistas de la matriz y el resultado de su comprobación.')
    args = parser.parse_args()
    try:
        payload = analizar(cargar_registros(args.csv), args.csv)
        node = os.environ.get('CODEX_PRIMARY_RUNTIME_NODE') or shutil.which('node')
        builder = Path(__file__).with_name('generar_matriz.mjs')
        if not args.sin_matriz:
            if not node:
                raise ValueError('La matriz requiere Node.js y @oai/artifact-tool. Consulta scripts/README.md.')
            subprocess.run([node, str(builder), '--comprobar'], check=True)
        # Las dependencias y los registros se comprueban antes de escribir resultados.
        from generar_graficos import generar as generar_graficos
        from generar_contrastes import generar as generar_contrastes
        with tempfile.TemporaryDirectory(prefix='ihc-resultados-') as temp:
            stage = Path(temp)
            generar_graficos(payload, stage / 'curva_emocional')
            generar_contrastes(stage / 'curva_emocional')
            outputs = [Path('curva_emocional') / name for name in GRAFICOS]
            if not args.sin_matriz:
                inputs = stage / 'datos.json'
                # Los metadatos de inspección no sustituyen las puntuaciones del registro.
                from contenido import MOMENTOS
                payload['moments'] = MOMENTOS
                inputs.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
                matrix = Path('matriz/matriz_ux.xlsx')
                (stage / matrix).parent.mkdir()
                shutil.copy2(ROOT / matrix, stage / matrix)
                command = [node, str(builder), '--datos', str(inputs), '--matriz', str(stage / matrix)]
                if args.qa_dir:
                    command += ['--qa-dir', str(args.qa_dir.resolve())]
                subprocess.run(command, check=True)
                outputs.append(matrix)
            # Publicar solo cuando todos los generadores finalizaron correctamente.
            for relative in outputs:
                target = args.salida / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(stage / relative, target)
    except (OSError, ValueError, ImportError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f'No se pudo completar la actualización: {exc}\n')
    print('Resultados actualizados desde 30 registros. El informe entregado conserva su archivo original.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
