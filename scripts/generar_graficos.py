"""Genera las seis figuras emocionales y el resumen a partir de registros validados."""
from pathlib import Path
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from procesar_resultados import (ROOT, DEFAULT_CSV, PARTICIPANTES, VERSIONES, MOMENTOS,
                                 cargar_registros, analizar, escribir_resumen)


def generar(payload: dict, salida: Path) -> None:
    rows = payload['records']
    codes, moments, versions = PARTICIPANTES, MOMENTOS, VERSIONES
    OUT = Path(salida)
    OUT.mkdir(parents=True, exist_ok=True)
    data = {}
    for version in versions:
        data[version] = np.array([[int(next(r['valor'] for r in rows if (r['participante'],r['version'],r['momento'])==(code,version,m))) for m in moments] for code in codes])
        assert np.logical_and(data[version]>=-3,data[version]<=3).all()
    A,B = [data[v] for v in versions]
    labels = ['M1\nIngreso','M2\nExplorar','M3\nAjustar','M4\nConfirmar','M5\nFinalizar']
    colors = ['#0072B2','#D55E00','#009E73']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10.5,'axes.titlesize':14,'axes.labelsize':10.5,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
    def setup(ax):
        ax.axhspan(-3.45,0,color='#fff4ed',zorder=0)
        ax.axhspan(0,3.45,color='#edf5fa',zorder=0)
        ax.axhline(0,color='#6b7280',lw=.9)
        ax.set(xticks=range(5),xticklabels=labels,yticks=range(-3,4),ylim=(-3.4,3.4),xlim=(-.18,4.18))
        ax.grid(axis='y',alpha=.17)
    def save(fig,name):
        fig.savefig(OUT/name,dpi=240,bbox_inches='tight')
        plt.close(fig)
    def signed(v): return ('+' if v>0 else '')+f'{v:.1f}'.replace('.',',')

    # Trayectorias por versión y promedio de los tres casos.
    for values,name,title in [(A,'curvas_original.png','Versión A del original'),(B,'curvas_rediseno.png','Versión B del rediseño')]:
        fig,ax=plt.subplots(figsize=(9.6,4.8));setup(ax)
        for i,code in enumerate(codes):ax.plot(range(5),values[i],marker=['o','s','^'][i],color=colors[i],lw=1.7,alpha=.9,label=code)
        ax.plot(range(5),values.mean(axis=0),'D--',color='#111827',lw=2.5,markersize=6,label='Promedio de 3 participantes')
        ax.set_ylabel('Valoración emocional de −3 a +3')
        ax.set_title(title,loc='left',fontweight='bold',pad=28)
        ax.text(0,1.045,'Evaluación comparativa con tres participantes',transform=ax.transAxes,color='#6b7280',fontsize=10)
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),ncol=4,frameon=False)
        fig.tight_layout();save(fig,name)

    fig,ax=plt.subplots(figsize=(9.6,4.8));setup(ax)
    for values,color,marker,title,offset in [(A,'#b34b26','o','A original',-23),(B,'#1758a3','s','B rediseño',12)]:
        avg=values.mean(axis=0)
        ax.fill_between(range(5),values.min(axis=0),values.max(axis=0),color=color,alpha=.10)
        ax.plot(range(5),avg,marker=marker,color=color,lw=2.6,label=title)
        for i,y in enumerate(avg):ax.annotate(signed(y),(i,y),textcoords='offset points',xytext=(0,offset),ha='center',fontsize=10,fontweight='bold',color=color)
    ax.set_ylabel('Promedio de la valoración emocional')
    ax.set_title('Comparación emocional antes y después',loc='left',fontweight='bold',pad=28)
    ax.text(0,1.045,'Evaluación · Bandas de mínimo a máximo de los perfiles',transform=ax.transAxes,color='#6b7280',fontsize=9.4)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),ncol=2,frameon=False)
    fig.tight_layout();save(fig,'curva_emocional.png')

    fig,axes=plt.subplots(1,3,figsize=(12,4),sharey=True)
    for i,ax in enumerate(axes):
        setup(ax);ax.set_xticklabels(moments)
        ax.plot(range(5),A[i],'o--',color='#b34b26',lw=1.8,label='A original')
        ax.plot(range(5),B[i],'s-',color='#1758a3',lw=1.8,label='B rediseño')
        ax.set_title(codes[i]+f'   Δ medio {signed(float((B[i]-A[i]).mean()))}',fontsize=12)
        ax.set_xlabel('Momentos M1 a M5')
    axes[0].set_ylabel('Valoración emocional')
    handles,legend=axes[0].get_legend_handles_labels()
    fig.legend(handles,legend,loc='lower center',ncol=2,frameon=False)
    fig.suptitle('Trayectorias emparejadas de los tres participantes',x=.05,ha='left',fontweight='bold',fontsize=14)
    fig.tight_layout(rect=(0,.10,1,.88));save(fig,'curvas_pareadas.png')

    fig,ax=plt.subplots(figsize=(9.3,4.3))
    heat=np.vstack([A,B]);im=ax.imshow(heat,cmap='RdBu',norm=TwoSlopeNorm(vmin=-3,vcenter=0,vmax=3),aspect='auto')
    ax.set(xticks=range(5),xticklabels=labels,yticks=range(6),yticklabels=[f'A original · {c}' for c in codes]+[f'B rediseño · {c}' for c in codes])
    for y in range(6):
        for x in range(5):ax.text(x,y,('+' if heat[y,x]>0 else '')+str(heat[y,x]),ha='center',va='center',color='white' if abs(heat[y,x])>=2 else '#111827',fontsize=12,fontweight='bold')
    ax.axhline(2.5,color='white',lw=3);ax.tick_params(length=0)
    fig.colorbar(im,ax=ax,ticks=range(-3,4),shrink=.85,label='Valoración emocional')
    ax.set_title('Las 30 valoraciones de la evaluación',loc='left',fontweight='bold',pad=16)
    fig.tight_layout();save(fig,'mapa_valoraciones.png')

    fig,ax=plt.subplots(figsize=(9.2,3.5));delta=(B-A).mean(axis=0)
    ax.barh(range(5),delta,color='#1758a3',height=.56)
    ax.set(yticks=range(5),yticklabels=['M1 Ingreso','M2 Explorar','M3 Ajustar','M4 Confirmar','M5 Finalizar'],xlim=(min(0, float(delta.min())-.5), max(3.9, float(delta.max())+.5)),xticks=np.arange(min(0, np.floor(delta.min())), max(4, np.ceil(delta.max()))+1),xlabel='Diferencia B menos A en puntos de la escala')
    ax.invert_yaxis();ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    for y,x in enumerate(delta):ax.text(x+(.07 if x>=0 else -.07),y,signed(x),va='center',ha='left' if x>=0 else 'right',fontsize=11,fontweight='bold')
    ax.set_title('Cambio por momento en la evaluación',loc='left',fontweight='bold',pad=16)
    fig.tight_layout();save(fig,'diferencia_momentos.png')

    escribir_resumen(payload, OUT / 'resumen_resultados.csv')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, default=DEFAULT_CSV)
    parser.add_argument('--salida', type=Path, default=ROOT / 'curva_emocional')
    args = parser.parse_args()
    try:
        payload = analizar(cargar_registros(args.csv), args.csv)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Error: {exc}\n')
    generar(payload, args.salida)
    print('Gráficos y resumen generados en', args.salida)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
