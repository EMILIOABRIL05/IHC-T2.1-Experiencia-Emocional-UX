"""Contrastes de muestras de color documentadas, sin certificar conformidad global."""
from pathlib import Path
import argparse
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
PAIRS=[
 ['Guardar original','#888772','#CECFAD',4.5],
 ['Zoom original','#8E8B78','#CFD0A8',3.0],
 ['Etiqueta original','#8A8B00','#F2FF00',4.5],
 ['Confirmar rediseño','#FFFFFF','#1F4FD8',4.5],
 ['Texto secundario rediseño','#4A5363','#FFFFFF',4.5],
 ['Estado coincide rediseño','#17693E','#E7F5EC',4.5],
 ['Borde zoom rediseño','#767F90','#FFFFFF',3.0],
]
def luminance(h):
    rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    lin=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(a*b for a,b in zip(lin,[.2126,.7152,.0722]))
def ratio(a,b):
    x,y=sorted([luminance(a),luminance(b)],reverse=True)
    return (x+.05)/(y+.05)
def generar(salida: Path) -> None:
    values=[ratio(r[1],r[2]) for r in PAIRS]
    out=Path(salida);out.mkdir(parents=True, exist_ok=True)
    with (out/'contrastes.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f, lineterminator='\n');w.writerow(['par','primer_plano','fondo','umbral_aplicado','ratio_calculado','alcance'])
        for r,v in zip(PAIRS,values):w.writerow(r+[round(v,6),'Muestra de colores; no certifica toda la interfaz'])
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10.5,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(10,4.8))
    ax.barh(range(7),values,color=['#b34b26']*3+['#1758a3']*4,height=.56,label='Contraste calculado')
    for y,(r,v) in enumerate(zip(PAIRS,values)):
        ax.plot(r[3],y,'|',color='#111827',ms=22,mew=2)
        ax.text(v+.1,y,f'{v:.2f}:1'.replace('.',','),va='center',fontsize=10)
    ax.set(yticks=range(7),yticklabels=[r[0] for r in PAIRS],xlim=(0,9),xlabel='Relación de contraste de los pares documentados')
    ax.invert_yaxis();ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    ax.set_title('Verificación parcial del contraste',loc='left',fontweight='bold',fontsize=14,pad=28)
    ax.text(0,1.045,'La marca negra indica el umbral aplicado a cada par: 4,5:1 para texto o 3:1 para control',transform=ax.transAxes,color='#6b7280',fontsize=9.2)
    fig.tight_layout();fig.savefig(out/'contraste_visual.png',dpi=240,bbox_inches='tight');plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, default=ROOT / 'curva_emocional')
    args = parser.parse_args()
    generar(args.salida)
    print('Contrastes generados en', args.salida)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
