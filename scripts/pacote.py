# Gera o pacote zipado para entregar à hospedagem (site/ + servidores/ + LEIA-ME.txt).
# Roda o build, atualiza servidores/ e grava loja-brasilia-site-AAAA-MM-DD.zip em ~/Downloads.
# Uso: python3 scripts/pacote.py [pasta-de-destino]
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
destino = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / 'Downloads'


def saida(*cmd):
    return subprocess.run(cmd, cwd=raiz, check=True, capture_output=True, text=True).stdout.strip()


if saida('git', 'status', '--porcelain'):
    sys.exit('Há alterações sem commit. Faça o commit antes, para o LEIA-ME apontar o commit certo.')

subprocess.run(['python3', 'scripts/servidores.py'], cwd=raiz, check=True)
subprocess.run(['npm', 'run', 'build'], cwd=raiz, check=True)
if saida('git', 'status', '--porcelain'):
    sys.exit('O servidores.py alterou arquivos em servidores/. Faça o commit e rode de novo.')

hoje = date.today()
nome = f'loja-brasilia-site-{hoje.isoformat()}'
with tempfile.TemporaryDirectory() as tmp:
    pasta = Path(tmp) / 'loja-brasilia-site'
    shutil.copytree(raiz / 'dist', pasta / 'site')
    shutil.copytree(raiz / 'servidores', pasta / 'servidores')
    leia_me = (raiz / 'scripts/LEIA-ME.txt').read_text()
    (pasta / 'LEIA-ME.txt').write_text(
        leia_me.format(data=hoje.strftime('%d/%m/%Y'), commit=saida('git', 'rev-parse', '--short', 'HEAD'))
    )
    for lixo in pasta.rglob('.DS_Store'):
        lixo.unlink()
    destino.mkdir(parents=True, exist_ok=True)
    zip_final = shutil.make_archive(str(destino / nome), 'zip', tmp, 'loja-brasilia-site')

print(f'Pacote gerado: {zip_final}')
