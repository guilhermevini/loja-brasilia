// Datas das sessões, a partir dos calendários oficiais da Loja.
// `corpo` indica a quem pertence a sessão; tudo que não é 'loja' é corpo associado.
export type Corpo = 'loja' | 'capitulo' | 'marca' | 'nautas';

export interface Evento {
  data: string; // AAAA-MM-DD
  corpo: Corpo;
  tipo?: string; // destaque opcional: Eleição, Posse, Instalação
}

const loja = (datas: string[], especiais: Record<string, string> = {}): Evento[] =>
  datas.map((data) => ({ data, corpo: 'loja', tipo: especiais[data] }));

const de = (corpo: Corpo, datas: string[], tipo?: string): Evento[] => datas.map((data) => ({ data, corpo, tipo }));

export const nomesCorpos: Record<Corpo, string> = {
  loja: 'Loja Brasília',
  capitulo: 'Capítulo do Arco Real',
  marca: 'Loja de Marca',
  nautas: 'Nautas da Arca Real',
};

export const calendario: { ano: number; recesso: string; eventos: Evento[] }[] = [
  {
    ano: 2026,
    recesso: 'Recesso em julho.',
    eventos: [
      ...loja(
        [
          '2026-02-09', '2026-02-23', '2026-03-09', '2026-03-23', '2026-03-30', '2026-04-13', '2026-04-27',
          '2026-05-11', '2026-05-25', '2026-06-08', '2026-06-15', '2026-06-22', '2026-06-29', '2026-08-03',
          '2026-08-24', '2026-08-31', '2026-09-14', '2026-09-28', '2026-10-26', '2026-11-09', '2026-11-16',
          '2026-11-30', '2026-12-14',
        ],
        { '2026-05-11': 'Eleição', '2026-06-22': 'Posse' },
      ),
      ...de('capitulo', ['2026-03-16', '2026-05-18', '2026-08-17', '2026-10-19', '2026-11-23']),
      ...de('marca', ['2026-04-06', '2026-06-01', '2026-10-05']),
      ...de('marca', ['2026-02-02'], 'Instalação'),
      ...de('nautas', ['2026-05-04', '2026-08-10', '2026-12-07']),
      ...de('nautas', ['2026-03-02'], 'Instalação'),
    ],
  },
  {
    ano: 2027,
    recesso: 'Recesso em janeiro e julho.',
    eventos: [
      ...loja(
        [
          '2027-02-15', '2027-02-22', '2027-03-08', '2027-03-22', '2027-03-29', '2027-04-12', '2027-04-19',
          '2027-04-26', '2027-05-10', '2027-05-24', '2027-05-31', '2027-06-14', '2027-06-21', '2027-06-28',
          '2027-08-09', '2027-08-23', '2027-08-30', '2027-09-13', '2027-09-20', '2027-09-27', '2027-10-25',
          '2027-11-08', '2027-11-22', '2027-11-29', '2027-12-13',
        ],
        { '2027-05-10': 'Eleição', '2027-06-28': 'Posse' },
      ),
      ...de('capitulo', ['2027-03-15', '2027-05-17', '2027-08-16', '2027-10-18']),
      ...de('marca', ['2027-04-05', '2027-06-07', '2027-10-04']),
      ...de('marca', ['2027-02-01'], 'Instalação'),
      ...de('nautas', ['2027-05-03', '2027-08-02', '2027-12-06']),
      ...de('nautas', ['2027-03-01'], 'Instalação'),
    ],
  },
];
