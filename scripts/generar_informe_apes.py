"""Punto de entrada conservado para identificar el antiguo generador del informe.

El informe entregado no se regenera. El procesamiento vigente está en
procesar_resultados.py y generar_curva_y_matriz.py.
"""
import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', help='Argumento del generador anterior; ya no se utiliza.')
    parser.parse_args()
    parser.exit(2, 'El generador del informe fue retirado: informe/informe_final.pdf se conserva sin cambios.\n'
                   'Para actualizar curvas y matriz, ejecuta: python3 scripts/generar_curva_y_matriz.py\n')


if __name__ == '__main__':
    raise SystemExit(main())
