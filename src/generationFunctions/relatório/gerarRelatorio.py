import pystache
import re
import sys
from src.supportFunctions.ponto_2_virgula import ponto_2_virgula
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def gerarRelatorioPorCurso(curso_escolhido, collectionCurso, collectionCursosPorCentro):
    """
    Gerar um relatório de apenas um curso.

    :param curso_escolhido: Nome do curso que você quer gerar o relatório md
    :type curso_escolhido: String
    :param collectionCurso: Nome da collection que tem as informações do csv principal
    :type collectionCurso: Collection
    :param collectionCursosPorCentro: Nome da collection que tem as informações para gerar a 
    introdução do relatório.
    :type collectionCursosPorCentro: Collection
    """


    #Talvez separar parte inicial para virar uma função compor capa
    
    directory = Path('relatorio')
    directory.mkdir(parents=True, exist_ok=True)
    file = f'{directory}/{curso_escolhido}.md'

    with open(file, 'w', buffering=-1,encoding='utf-8') as arquivo:

        arquivo.write("---\n")
        arquivo.write("title: \"Relatório do Curso de {}\"\n".format(curso_escolhido))
        arquivo.write("titlepage: true\n")
        arquivo.write("titlepage-background: \"capa\"\n")
        arquivo.write("titlepage-rule-color: \"B3B3B3\"\n")
        arquivo.write("page-background: \"interna02\"\n")
        arquivo.write("page-background-opacity: '1.0'\n")
        arquivo.write("author: [CPA-Comissão Própria de Avaliação]\n")
        arquivo.write("lang: \"pt-BR\"\n")
        arquivo.write("---\n\n")

        #Precisa criar a função que compõe a introdução
        with open("info_introducao.md",'r', encoding='utf-8') as f:
            template_introducao = f.read()
        renderer = pystache.Renderer()
        participacao_curso = 0.0
        for document in collectionCursosPorCentro.find({'nome_do_curso': curso_escolhido}):
            participacao_curso = document['porcentagem']
        intro = renderer.render(template_introducao, {'curso': curso_escolhido, 'participacao_curso': participacao_curso})
        arquivo.write(f'{intro} \n')


        #-------------------------------- VIRA UMA FUNÇÃO ----------------------------
        for document in collectionCurso.find({'nome_do_curso': curso_escolhido}):
            # if document['codigo_disciplina'] == '-':
            legenda_gpt = re.sub(r'\"','',document["legendaGraficoGPT"]).rstrip()
            # arquivo.write(f"![{legenda_gpt}]({f'{document["path"]}.png'} '{legenda_gpt}')")
            arquivo.write(f"![{legenda_gpt}]({document['path']}.png '{legenda_gpt}')")
            print('\n', file=arquivo)
            print(f"Tabela index_- {document['legendaGraficoGPT']} \n", file=arquivo)
            arquivo.write(document['tabela'])
            arquivo.write('\n')
            print(' ', file=arquivo)
            print(document['relatorioGraficoGPT'], file=arquivo)
            arquivo.write('\n')
            arquivo.write('\n')
            print(f"Edição da pergunta {document['nu_pergunta']} do subgrupo {document['cd_subgrupo']} do curso {document['nome_do_curso']} concluida com sucesso!")
        
        # for document in collectionCurso.find({'nome_do_curso': curso_escolhido}):
            # if document['codigo_disciplina'] != '-':
            ...
        #------------------------------------VIRA UMA FUNÇÃO ----------------------------

        with open("info_conclusao.md",'r',encoding='utf-8') as f:
            template_conclusao = f.read()
        rendererConclusao = pystache.Renderer()
        conclusao = rendererConclusao.render(template_conclusao, {'curso': curso_escolhido, 'participacao_curso': ponto_2_virgula(participacao_curso)})
        arquivo.write(f'{conclusao} \n')
    arquivo.close()

    