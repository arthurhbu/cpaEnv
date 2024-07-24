def dfCursosPorCentro(collectionCursoseCentros,ano,centro_de_ensino):

    # Realizar a agregação de dados
    results = list(collectionCursoseCentros.aggregate([
    {
        "$lookup": {
            "from": "curso",
            "localField": "cd_curso",
            "foreignField": "cd_curso",
            "as": "curso"
        }
    },
    {
        "$unwind": "$curso"
    },
    {
        "$match": {
            "ano_referencia": ano,
            "centro_de_ensino": centro_de_ensino
        }
    },
    {
        "$group": {
            "_id": "$cd_curso",
            "nm_curso": {"$first": "$nm_curso"},
            "centro_de_ensino": {"$first": "$centro_de_ensino"},
            "matriculados": {"$first": "$matriculados"},
            "total_do_curso": {"$first": "$curso.total_do_curso"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "nm_curso": 1,
            "centro_de_ensino": 1,
            "respondentes": "$total_do_curso",
            "matriculados": 1,
            "porcentagem": {
                "$cond": {
                    "if": {"$eq": ["$matriculados", 0]},
                    "then": 0,
                    "else": {
                        "$round": [
                            {
                                "$multiply": [
                                    {"$divide": ["$total_do_curso", "$matriculados"]},
                                    100
                                ]
                            },
                            2
                        ]
                    }
                }
            }
        }
    },
    {
        "$sort": {"nm_curso": 1}
    }
    ]))


    return results

def dfCentroPorAno(collectionCurso,database, ano):
    centro_por_ano_temp = database['centro_por_ano_temp']

    collectionCurso.aggregate([
        {   
            "$lookup": {
            "from": "cursos_e_centros",
            "localField": "cd_curso",
            "foreignField": "cd_curso",
            "as": "cursos_e_centros"
            }
        },
        {
            "$unwind": "$cursos_e_centros"
        },
        {
            "$match": {
                "cursos_e_centros.ano_referencia": ano 
            }
        },
        {
            "$group": {
                "_id": "$nm_curso",
                "respondentes": {"$max": "$total_do_curso"},
                "centro_de_ensino": {'$first': '$cursos_e_centros.centro_de_ensino'},
                "matriculados": {'$first': "$cursos_e_centros.matriculados"},
            }
        },
        {
            '$addFields': {
                'centro_de_ensino': '$centro_de_ensino'
            }
        },
        {
            '$project': {
                '_id': 1,
                'centro_de_ensino': 1,
                'respondentes': 1,
                'matriculados': 1,
            }
        },
        {
            '$out':'centro_por_ano_temp'
        }
    ])
    
    centro_por_ano_temp.aggregate(
        [
            {
                '$lookup':{
                    "from": "centros_e_diretores",
                    "localField": "centro_de_ensino",
                    "foreignField": "centro_de_ensino",
                    "as": "centros_e_diretores"
                }
            },
            {
                "$unwind": "$centros_e_diretores"
            },
            {
                "$group": {
                    "_id": "$centro_de_ensino",
                    "centro_descricao": {"$first": "$centros_e_diretores.centro_descricao"},
                    "respondentes": {"$sum": "$respondentes"},
                    "matriculados": {"$sum": "$matriculados"},
                    "porcentagem": {
                        "$avg": {
                            "$multiply": [
                                {"$divide": [{"$sum": "$respondentes"}, {"$sum": "$matriculados"}]},
                                100
                            ]
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'centro_de_ensino':'$_id',
                    'centro_descricao':1,
                    'respondentes': 1,
                    'matriculados':1,
                    'porcentagem': {'$round': ['$porcentagem', 2]}
                }

            },
            {
                "$sort": {"_id": 1}
            },
            {
                '$out': f'centro_por_ano'
            }
            
        ]
    )
    # centro_por_ano_temp.drop()