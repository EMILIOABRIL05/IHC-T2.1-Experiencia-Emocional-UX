"""Valida y resume los 30 registros publicados, sin completar ni sustituir datos."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / 'evidencias/pruebas_usuarios/resultados/registros_evaluacion.csv'
PARTICIPANTES = ('P1', 'P2', 'P3')
VERSIONES = ('A_original', 'B_rediseno')
MOMENTOS = ('M1', 'M2', 'M3', 'M4', 'M5')
CAMPOS = ('participante', 'version', 'momento', 'valor', 'emocion_evaluacion',
          'nota_evaluacion', 'captura_referencia', 'tipo_registro')
RESUMEN_CAMPOS = ('momento', 'media_A', 'media_B', 'diferencia_B_menos_A',
                  'mediana_A', 'mediana_B', 'min_A', 'max_A', 'min_B', 'max_B', 'tipo_registro')


def cargar_registros(path: Path = DEFAULT_CSV) -> list[dict]:
    """Exige una observación íntegra por código, versión y momento."""
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(CAMPOS):
            raise ValueError('Encabezado incompatible. Se requieren, en este orden: ' + ', '.join(CAMPOS))
        records = []
        seen = set()
        for line, row in enumerate(reader, start=2):
            if None in row or any(row.get(c) is None or not row[c].strip() for c in CAMPOS):
                raise ValueError(f'Fila {line}: hay campos vacíos o columnas adicionales.')
            key = (row['participante'], row['version'], row['momento'])
            if key[0] not in PARTICIPANTES or key[1] not in VERSIONES or key[2] not in MOMENTOS:
                raise ValueError(f'Fila {line}: código, versión o momento no admitido: {key}.')
            if key in seen:
                raise ValueError(f'Fila {line}: registro duplicado: {key}.')
            try:
                value = int(row['valor'])
            except ValueError as exc:
                raise ValueError(f'Fila {line}: valor debe ser un entero de −3 a +3.') from exc
            if not -3 <= value <= 3:
                raise ValueError(f'Fila {line}: valor fuera de la escala −3 a +3.')
            if row['tipo_registro'] != 'evaluacion_ux':
                raise ValueError(f'Fila {line}: tipo_registro debe ser evaluacion_ux.')
            seen.add(key)
            records.append({**row, 'valor': value})
    expected = {(p, v, m) for p in PARTICIPANTES for v in VERSIONES for m in MOMENTOS}
    if seen != expected:
        raise ValueError(f'Se requieren 30 registros completos. Faltan: {sorted(expected - seen)}.')
    return sorted(records, key=lambda r: (r['participante'], r['version'], r['momento']))


def analizar(records: list[dict], source: Path = DEFAULT_CSV) -> dict:
    lookup = {(r['participante'], r['version'], r['momento']): r['valor'] for r in records}
    summary = []
    for m in MOMENTOS:
        a, b = ([lookup[p, v, m] for p in PARTICIPANTES] for v in VERSIONES)
        summary.append(dict(zip(RESUMEN_CAMPOS, (
            m, float(mean(a)), float(mean(b)), float(mean(b) - mean(a)), median(a), median(b),
            min(a), max(a), min(b), max(b), 'evaluacion_ux'))))
    participants = []
    for p in PARTICIPANTES:
        a, b = (mean(lookup[p, v, m] for m in MOMENTOS) for v in VERSIONES)
        participants.append({'participante': p, 'media_A': a, 'media_B': b, 'diferencia_B_menos_A': b-a})
    a, b = (mean(r['valor'] for r in records if r['version'] == v) for v in VERSIONES)
    source = Path(source).resolve()
    try:
        source_name = source.relative_to(ROOT).as_posix()
    except ValueError:
        source_name = source.name
    return {
        'schema_version': 1,
        'source': {'path': source_name, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()},
        'records': records, 'summary': summary, 'participants': participants,
        'global': {'media_A': a, 'media_B': b, 'diferencia_B_menos_A': b-a},
    }


def escribir_resumen(payload: dict, target: Path) -> None:
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=RESUMEN_CAMPOS, lineterminator='\n')
    writer.writeheader()
    for row in payload['summary']:
        writer.writerow({k: round(v, 6) if isinstance(v, float) else v for k, v in row.items()})
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\ufeff' + buffer.getvalue(), encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, default=DEFAULT_CSV, help='CSV de entrada con el esquema publicado.')
    parser.add_argument('--salida', type=Path, help='Carpeta alternativa para resumen_resultados.csv.')
    parser.add_argument('--json', type=Path, help='Exportar registros y cálculos para el generador de la matriz.')
    parser.add_argument('--validar', action='store_true', help='Comprobar la entrada sin escribir archivos.')
    args = parser.parse_args()
    try:
        payload = analizar(cargar_registros(args.csv), args.csv)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Error: {exc}\n')
    if not args.validar:
        escribir_resumen(payload, (args.salida or ROOT / 'curva_emocional') / 'resumen_resultados.csv')
        if args.json:
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    g = payload['global']
    print(f"30 registros válidos. Media A: {g['media_A']:.6f}; media B: {g['media_B']:.6f}; diferencia: {g['diferencia_B_menos_A']:.6f}.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
