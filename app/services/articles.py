# Catálogo estático de artigos publicados no site.
#
# Cada chave do dicionário é o "slug" do artigo — a parte da URL que o identifica
# de forma legível (ex: /publicacoes/critica-mortos-de-amor).
#
# Estrutura de cada artigo:
#   title      : título completo do artigo
#   category   : categoria exibida como badge (ex: "Guia", "Crítica", "Notícia")
#   cover      : nome do arquivo de imagem de capa (em app/static/images/)
#   cover_alt  : texto alternativo da imagem (acessibilidade / SEO)
#   blocks     : lista de blocos de conteúdo. Cada bloco tem um campo "type":
#                  "paragraph" : parágrafo de texto com campo "text"
#                                e "class" opcional (ex: "lead", "byline")
#                  "heading"   : subtítulo de seção com campo "text"
#                  "image"     : imagem com campos "src", "alt" e "caption" opcional
#
# FEATURED_ARTICLE_SLUGS define a ordem em que os artigos aparecem na home page.
ARTICLES = {
    "ordem-cronologica-cavaleiros-do-zodiaco": {
        "title": "Ordem cronológica dos animes de Cavaleiros do Zodíaco",
        "category": "Guia",
        "cover": "Cavaleiros-do-Zodiaco.webp",
        "cover_alt": "Arte da matéria sobre Cavaleiros do Zodíaco",
        "blocks": [
            {
                "type": "paragraph",
                "text": (
                    "Aproveitando que no último 1º de setembro se comemorou "
                    "29 anos da estreia do anime dos Cavaleiros do Zodíaco, "
                    "vamos aqui falar a ordem cronológica da história."
                ),
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-1.webp",
                "alt": "Imagem da série Os Cavaleiros do Zodíaco",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Os Cavaleiros do Zodíaco, também conhecido como Saint "
                    "Seiya, é um popular anime dos anos 90 e sua exibição "
                    "inicial aconteceu pela extinta Rede Manchete. Depois da "
                    "estreia, o anime passou a ganhar diversas outras "
                    "temporadas e spin-offs que acrescentam em muito a "
                    "mitologia da obra."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Entretanto, a mais conhecida das sagas, A Saga das Doze "
                    "Casas, é parte de uma linha cronológica que conta uma "
                    "história muito maior do que pensávamos. Confira e "
                    "descubra mais sobre a cronologia do anime."
                ),
            },
            {
                "type": "paragraph",
                "text": "Não iremos falar dos filmes, apenas das séries em anime.",
            },
            {
                "type": "heading",
                "text": (
                    "Cavaleiros do Zodíaco: The Lost Canvas – A Saga de Hades "
                    "(Saint Seiya: The Lost Canvas – Meiō Shinwa)"
                ),
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-2.webp",
                "alt": "Imagem de The Lost Canvas",
                "caption": "Imagem: TMS Entertainment",
            },
            {
                "type": "paragraph",
                "text": (
                    "Vamos começar por um que é polêmico: Saint Seiya: The "
                    "Lost Canvas. Originalmente, a obra, tanto mangá quanto "
                    "anime, seria canônica, mas atualmente não é o caso. The "
                    "Lost Canvas acontece 243 anos antes da obra clássica "
                    "criada por Masami Kurumada e conta a Guerra Santa entre "
                    "Atena e Hades durante o século 18."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Neste anime acompanhamos Tenma, o Cavaleiro de Pégaso, "
                    "um órfão com forte ligação com Alone e Sasha, que se "
                    "tornariam os hospedeiros de Hades e Atena. Também "
                    "aparecem Dohko de Libra, mestre de Shiryu, e Shion de "
                    "Áries, antigo Mestre do Santuário e mestre de Mu."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "A história de Saint Seiya: The Lost Canvas – Meiō Shinwa "
                    "foi feita por Shiori Teshirogi em parceria com Masami "
                    "Kurumada. O anime possui 26 episódios e não tem final. "
                    "Os episódios foram exibidos entre 2009 e 2011. O mangá "
                    "fez sucesso e ganhou a continuação The Lost Canvas "
                    "Gaiden; ambas as obras foram publicadas no Brasil pela "
                    "editora JBC."
                ),
            },
            {
                "type": "heading",
                "text": "Os Cavaleiros do Zodíaco (Saint Seiya)",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-3.webp",
                "alt": "Imagem da série clássica dos Cavaleiros do Zodíaco",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "O clássico Os Cavaleiros do Zodíaco estreou no Japão em "
                    "outubro de 1986 e chegou ao Brasil em setembro de 1994. "
                    "Na Rede Manchete, o anime se tornou um sucesso. A primeira "
                    "Saga do Santuário foi dividida em três arcos: Guerra "
                    "Galáctica, Os Cavaleiros de Prata e A Batalha das Doze "
                    "Casas."
                ),
            },
            {
                "type": "heading",
                "text": "Saga do Santuário: Guerra Galáctica",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-4.webp",
                "alt": "Imagem do arco Guerra Galáctica",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Neste primeiro arco somos apresentados a Seiya, Shiryu, "
                    "Hyoga, Shun e Ikki, além dos outros Cavaleiros de Bronze "
                    "que participam da Guerra Galáctica. O vencedor ganharia "
                    "a armadura de ouro de Sagitário. Seiya e Shiryu lutam "
                    "até a morte, mas Seiya consegue trazer Shiryu de volta. "
                    "Quando o Cavaleiro de Fênix retorna e rouba a armadura "
                    "de ouro, começa uma batalha para recuperá-la."
                ),
            },
            {
                "type": "heading",
                "text": "Saga do Santuário: Os Cavaleiros de Prata",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-5.webp",
                "alt": "Imagem do arco dos Cavaleiros de Prata",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Após os eventos do arco anterior, o Santuário envia os "
                    "Cavaleiros de Prata para derrotar os Cavaleiros de Bronze "
                    "no Japão. Eles enfrentam uma patente superior, descobrem "
                    "a existência da Deusa Atena e conhecem os Cavaleiros de "
                    "Aço, exclusivos da adaptação. Também começam a questionar "
                    "o que acontece no Santuário e por que ele entrou em "
                    "guerra contra os Cavaleiros de Bronze."
                ),
            },
            {
                "type": "heading",
                "text": "Saga do Santuário: A Batalha das Doze Casas",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-6.webp",
                "alt": "Imagem da Batalha das Doze Casas",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Saori e os Cavaleiros de Bronze viajam até a Grécia para "
                    "falar com o Mestre do Santuário. Antes de começarem a "
                    "subir, Ptolemy de Sagita atinge Saori com uma flecha "
                    "dourada. Os Cavaleiros precisam subir as 12 Casas do "
                    "Zodíaco e salvá-la em até 12 horas, enfrentando os "
                    "Cavaleiros de Ouro. Este é o clímax da primeira saga."
                ),
            },
            {
                "type": "heading",
                "text": "A Saga da Batalha de Asgard",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-7.webp",
                "alt": "Imagem da Saga da Batalha de Asgard",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Esta saga é filler e seus acontecimentos não existem no "
                    "mangá. Como o anime havia alcançado o mangá, ela permitiu "
                    "esperar que a Saga de Poseidon fosse encerrada e pudesse "
                    "ser adaptada. Teve como base o filme Os Cavaleiros do "
                    "Zodíaco: A Grande Batalha dos Deuses e o capítulo 46.5 "
                    "do mangá."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Depois da batalha das 12 casas, Saori é atacada por Syd, "
                    "Guerreiro Deus de Mizar, que diz seguir as ordens de "
                    "Hilda. Representante de Odin na Terra, Hilda recebe de "
                    "Poseidon o Anel de Nibelungo e declara guerra contra "
                    "Atena."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Considerada por fãs um dos melhores arcos filler, a Saga "
                    "da Batalha de Asgard viria a ser um problema para o anime "
                    "no futuro. Ainda assim, o resultado trouxe uma melhora "
                    "em relação ao que vemos no mangá após a batalha das 12 "
                    "casas."
                ),
            },
            {
                "type": "heading",
                "text": "A Saga de Poseidon",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-8.webp",
                "alt": "Imagem da Saga de Poseidon",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Voltamos às adaptações do mangá e à batalha contra um "
                    "Deus que ainda não despertou. Após os eventos de Asgard, "
                    "Poseidon quer afundar o mundo. Atena decide se sacrificar "
                    "para salvar o planeta."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Os Cavaleiros de Bronze enfrentam Poseidon e seus "
                    "Generais Marinas no Santuário de Poseidon, nas "
                    "profundezas do Mar Mediterrâneo. O anime terminou após "
                    "esta saga, mas o mangá continuou com a Saga de Hades."
                ),
            },
            {
                "type": "heading",
                "text": "A Saga de Hades",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-9.webp",
                "alt": "Imagem da Saga de Hades",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "A página original repetia aqui a descrição da Saga de "
                    "Poseidon. A saga de Hades é apresentada em seguida nas "
                    "partes Santuário, Inferno e Campos Elíseos."
                ),
            },
            {
                "type": "heading",
                "text": "Saga de Hades: Santuário",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-10.webp",
                "alt": "Imagem da Saga de Hades: Santuário",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Esta parte inicia a última saga. Hades ressuscita "
                    "Cavaleiros de Ouro e Prata para capturar Atena e levá-la "
                    "até ele. Cabe aos Cavaleiros de Bronze proteger a deusa "
                    "e salvar o mundo da Guerra Santa."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Saga de Hades: Santuário contém 13 episódios, lançados "
                    "em DVD entre 2002 e 2003."
                ),
            },
            {
                "type": "heading",
                "text": "Saga de Hades: Inferno",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-11.webp",
                "alt": "Imagem da Saga de Hades: Inferno",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Continuação direta de Santuário, Inferno chegou em 2005. "
                    "Após Seiya e Rhadamanthys caírem no Portal do Inferno, "
                    "Hyoga, Shun e Shiryu vão atrás do amigo. Eles enfrentam "
                    "os Espectros de Hades e procuram Atena para entregar sua "
                    "armadura, enquanto descobrem que algo parece errado com "
                    "Shun."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Os episódios foram lançados em DVD entre 2005 e 2007. "
                    "Saga de Hades: Inferno contém 12 episódios."
                ),
            },
            {
                "type": "heading",
                "text": "Saga de Hades: Campos Elíseos",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-12.webp",
                "alt": "Imagem da Saga de Hades: Campos Elíseos",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Após o sacrifício dos Cavaleiros de Ouro para destruir o "
                    "Muro das Lamentações, os Cavaleiros de Bronze seguem "
                    "para os Campos Elíseos. Lá conhecem Thanatos e Hypnos, "
                    "respectivamente os deuses da Morte e do Sono. Para salvar "
                    "Atena e entregar sua armadura, devem derrotar os dois "
                    "deuses. A saga também mostra as Armaduras Divinas dos "
                    "Cavaleiros de Bronze."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "A parte foi lançada em DVD ao longo de cerca de um ano e "
                    "possui 6 episódios."
                ),
            },
            {
                "type": "heading",
                "text": "Saint Seiya: Ômega",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-13.webp",
                "alt": "Imagem de Saint Seiya: Ômega",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Um dos primeiros spin-offs da franquia, Saint Seiya: "
                    "Ômega não é oficialmente canônico e se passa 25 anos "
                    "depois da Guerra Santa do século 20, a Saga de Hades. "
                    "A série acompanha uma nova geração de Cavaleiros."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Depois do conflito com o Deus Marte, Seiya e os outros "
                    "Cavaleiros são impedidos de queimar o Cosmo, e Atena se "
                    "exila em uma ilha. Ela cuida de Kouga, que é treinado "
                    "por Shina para se tornar um Cavaleiro de Atena, enquanto "
                    "Marte planeja usurpar o lugar da deusa no Santuário."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "A série fez sucesso no Japão e recebeu uma segunda "
                    "temporada. Saint Seiya: Ômega possui 97 episódios."
                ),
            },
            {
                "type": "heading",
                "text": "Saint Seiya – Alma de Ouro (Saint Seiya – Soul of Gold)",
            },
            {
                "type": "image",
                "src": "Cavaleiros-do-Zodiaco-14.webp",
                "alt": "Imagem de Saint Seiya: Soul of Gold",
                "caption": "Imagem: Toei Company",
            },
            {
                "type": "paragraph",
                "text": (
                    "Ligado ao final de Saga de Hades: Inferno, o anime mostra "
                    "Aiolia acordando em Asgard após o sacrifício para "
                    "destruir o Muro das Lamentações. Os 12 Cavaleiros de "
                    "Ouro foram revividos para enfrentar uma nova ameaça. "
                    "Cronologicamente, a história se passa entre as partes 2 "
                    "e 3 da Saga de Hades. A série possui 13 episódios."
                ),
            },
            {
                "type": "heading",
                "text": "Saint Seiya – Saintia Shô",
            },
            {
                "type": "paragraph",
                "text": (
                    "Adaptação do mangá Saint Seiya: Saintia Sho, apresenta "
                    "as Saintias, guarda pessoal de Atena e únicas Amazonas "
                    "que não usam máscaras. A história acompanha Shoko, "
                    "Saintia de Cavalo Menor, na batalha entre Atena e Éris, "
                    "a Deusa da Discórdia. Os eventos ocorrem em paralelo à "
                    "Saga do Santuário. O anime tem uma temporada de 10 "
                    "episódios."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Esta é a ordem cronológica dos animes de Cavaleiros do "
                    "Zodíaco. A matéria original informa que os animes citados "
                    "estavam disponíveis na Crunchyroll."
                ),
            },
        ],
    },
    "critica-mortos-de-amor": {
        "title": (
            "Crítica | Mortos de Amor: de amor ninguém morre, "
            "mas de maldição talvez | Editora Pipoca & Nanquim"
        ),
        "category": "Crítica",
        "cover": "CAPA-MORTOSDEAMOR-220x312.jpg.avif",
        "cover_alt": "Capa do mangá Mortos de Amor",
        "blocks": [
            {
                "type": "paragraph",
                "text": "Postado por Gabriel Zoldick | set 6, 2023 |",
                "class": "byline",
            },
            {
                "type": "paragraph",
                "text": "Mangá conta a história de uma cidade onde as pessoas se matam de amor.",
                "class": "lead",
            },
            {
                "type": "paragraph",
                "text": (
                    "Todo mundo (ou pelo menos a maioria das pessoas) já se "
                    "apaixonou por alguém. Dizem que quando alguém está "
                    "acometido pela paixão essa pessoa fica sonhando acordada, "
                    "mas também é verdade que o sentimento traz consigo uma "
                    "carga de ansiedade e uma pergunta que nunca cala: será "
                    "que meu amor vai ser correspondido?"
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Se o apaixonado for um adolescente, então… Parece que é "
                    "o fim do mundo e que, caso o sentimento não seja "
                    "correspondido, o apaixonado pode até mesmo morrer de amor."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Esse comum e também inexplicável sentimento da paixão, "
                    "bem como os anseios dos apaixonados, é justamente o tema "
                    "do mangá Mortos de Amor, de Junji Ito, lançado este ano "
                    "pela editora Pipoca e Nanquim com a tradução de Drik Sada."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Publicado pela primeira vez em 1996 em formato periódico "
                    "na revista Nemuki, o mangá é uma história composta por "
                    "quatro capítulos principais e um extra — lançado em "
                    "2001 na mesma revista."
                ),
            },
            {
                "type": "image",
                "src": "mortos-de-amor-b-e1694440612758.jpeg.avif",
                "alt": "Ilustração da matéria sobre Mortos de Amor",
            },
            {
                "type": "paragraph",
                "text": (
                    "A trama tem como protagonista o adolescente Ryusuke, "
                    "que acaba de se mudar com a família de volta para sua "
                    "cidade natal, a nublada Nazumi. Os moradores dessa "
                    "cidade, onde frequentemente um denso nevoeiro se "
                    "concentra, mantêm vivo um antigo costume: ler a sorte em "
                    "uma encruzilhada. A leitura mais requisitada é, "
                    "obviamente, sobre a sorte no amor."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Entretanto, a situação ganha contornos difíceis de "
                    "enxergar quando um belo garoto vestido de preto começa "
                    "a percorrer as encruzilhadas dizendo palavras horríveis "
                    "a quem encontra. Começa assim um verdadeiro massacre em "
                    "Nazumi, pois as garotas que tiveram sua sorte lida pelo "
                    "Garoto da Encruzilhada se suicidam uma após a outra."
                ),
            },
            {
                "type": "image",
                "src": "mortos-de-amor-f-e1694440339617.jpeg.avif",
                "alt": "Imagem complementar da crítica Mortos de Amor",
            },
            {
                "type": "paragraph",
                "text": (
                    "Uma característica interessante dos quadrinhos de Junji "
                    "Ito é que o autor parece realmente tentar “fazer horror”. "
                    "Quer ele tenha êxito ou não, é perceptível a tentativa "
                    "de construir uma história pautada nos signos de horror "
                    "e não de algo que amedronte simplesmente. De fato, às "
                    "vezes até mesmo falta susto. Não causa medo, porque "
                    "talvez o autor queira justamente que a obra seja lida e "
                    "não que ela faça alguém gritar de tempos em tempos. Pelo "
                    "menos no plano visual, existe um trabalho que pode ser "
                    "bacana olhar com um pouco de atenção."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Nesse sentido, Mortos de Amor não é diferente. Ela não "
                    "é amedrontadora, mas o mistério é interessante o bastante "
                    "para te manter ali até o último capítulo. O final, por "
                    "sua vez, tem uma certa dualidade. Existe um elemento que "
                    "acaba amarrando toda a história e outro que acaba sendo "
                    "meio “é, não tinha muito como ser diferente”. Ainda "
                    "assim, pode-se dizer que o mistério cumpre a função de "
                    "entreter quem está lendo."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Já no que diz ao volume do mangá, fisicamente falando, "
                    "a editora faz uma escolha curiosa. A versão brasileira "
                    "é baseada na edição japonesa de 2011 composta por mais "
                    "cinco outros contos de Junji Ito, que nada têm a ver com "
                    "a história que dá título ao volume."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "A edição compila, portanto, seis histórias, somando dez "
                    "capítulos; ou seja, na metade do volume você já terminou "
                    "de ler a “história principal” — estar na metade do volume, "
                    "tendo já lido uma história longa, acaba dando a sensação "
                    "de que o volume nunca acaba."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Embora duas das outras narrativas — “A mulher das "
                    "costelas” e “Os bizarros irmãos Hikizuri: O namorado da "
                    "filha do meio” — sejam bem legais, é um pouco difícil "
                    "se livrar da sensação de que você já leu um monte e esse "
                    "mangá não chega ao fim."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "A estrutura dessa compilação acaba fazendo com que o "
                    "“tom” da edição mude. Você começa a ler uma história "
                    "única, ela termina, caem mais cinco histórias novas no "
                    "seu colo e o seu cérebro precisa recalcular a rota, "
                    "porque agora o volume não é mais uma compilação dos "
                    "capítulos da narrativa que você estava lendo, mas sim "
                    "de várias histórias diferentes."
                ),
            },
            {
                "type": "image",
                "src": "mortos-de-amor-3.jpeg",
                "alt": "Imagem da edição de Mortos de Amor",
            },
            {
                "type": "paragraph",
                "text": (
                    "Ainda assim, esse detalhe por si só não é o suficiente "
                    "para estragar a experiência de leitura, então, caso "
                    "Mortos de Amor tenha conseguido fisgar seu coração, a "
                    "estrutura do volume acaba ficando em segundo plano."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "No geral, o mangá é um mistério competente o bastante "
                    "para entreter o leitor e fazê-lo se perguntar: quem é "
                    "esse garoto de preto e por que suas palavras em vez de "
                    "apenas derramar lágrimas fazem sangue jorrar das gargantas?"
                ),
            },
        ],
    },
    "inuyasha-kanketsu-hen": {
        "title": "‘InuYasha: Kanketsu-hen’ estreia dublado em outubro na Pluto TV",
        "category": "Notícia",
        "cover": "inuyasha-kanketsu-780x500.jpg.avif",
        "cover_alt": "Imagem da matéria sobre InuYasha: Kanketsu-hen",
        "blocks": [
            {
                "type": "paragraph",
                "text": "Série finalizando a trama chega pela primeira vez dublada em nosso idioma!",
                "class": "lead",
            },
            {
                "type": "paragraph",
                "text": (
                    "A Pluto TV anunciou que InuYasha: Kanketsu-hen (2009; "
                    "InuYasha – The Final Act), que conclui a trama original "
                    "em 26 episódios, chega dublado ao Sob Demanda em 11 de "
                    "outubro. No mesmo dia, também entram no catálogo as "
                    "temporadas 1 a 7 da série original, com todos os episódios."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Essa fase final entrou no Amazon Prime Video apenas em "
                    "espanhol há alguns anos, sendo então a primeira vez que "
                    "será exibida dublada em nosso idioma. A Pluto TV também "
                    "transmite InuYasha em programação linear, pelo canal "
                    "Pluto TV Anime, desde o fim de agosto."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "A animação original, sem Kanketsu-hen, se encontra "
                    "completa e dublada na Netflix em versão integral. Na "
                    "versão editada pela Televix, com congelamento e zoom em "
                    "algumas cenas mais violentas, a série está no Amazon "
                    "Prime Video, sem dublagem em português para os sete "
                    "últimos episódios, disponíveis por lá apenas em espanhol."
                ),
            },
            {
                "type": "image",
                "src": "inuyasha-kanketsu-hen2.jpg",
                "alt": "Imagem adicional de InuYasha: Kanketsu-hen",
            },
        ],
    },
    "mostra-dicria": {
        "title": "Mostra Dicria será exposta no próximo sábado no RJ",
        "category": "Notícia",
        "cover": "Dicria.jpeg",
        "cover_alt": "Imagem da matéria sobre a Mostra Dicria",
        "blocks": [
            {
                "type": "paragraph",
                "text": (
                    "Exposição do MAR traz mangás criados por crianças que "
                    "frequentam a Mangateca Dicria."
                ),
                "class": "lead",
            },
            {
                "type": "paragraph",
                "text": "Jean Clemente | 27 de setembro de 2023 às 18:51",
                "class": "byline",
            },
            {
                "type": "paragraph",
                "text": (
                    "O Museu de Arte do Rio exibirá no próximo sábado (30) a "
                    "Mostra Dicria, feita pela Mangateca Dicria. Os mangás "
                    "autorais foram criados a partir da exposição Funk, um "
                    "grito de ousadia e liberdade. A mostra será aberta às "
                    "14h e será gratuita."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Os visitantes também poderão conferir como foi o processo "
                    "de criação das histórias. Vale destacar que todas foram "
                    "criadas por crianças do Morro do Fallet e crias da Dicria."
                ),
            },
            {
                "type": "heading",
                "text": "O que é o Anime DICRIA?",
            },
            {
                "type": "paragraph",
                "text": (
                    "Criado por Ed Cura, carioca do Morro do Fallet, o Anime "
                    "DICRIA começou como um perfil nas redes sociais, colocando "
                    "personagens de animê em cenas do cotidiano do Rio de "
                    "Janeiro. O nome é uma alusão ao modo como as crianças "
                    "criadas nas favelas do Rio são chamadas, os “crias”."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "A página do Instagram, que já conta com mais de 94 mil "
                    "seguidores, foi criada em fevereiro de 2021 para servir "
                    "como uma espécie de “válvula de escape” em relação à "
                    "pandemia, que interrompeu o trabalho de Ed como fotógrafo "
                    "de eventos, como ele conta ao jornal O Globo."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "Em 2022, foi inaugurada a Mangateca Dicria, localizada "
                    "no bairro de Santa Teresa. O objetivo do espaço é "
                    "incentivar a leitura através dos quadrinhos japoneses."
                ),
            },
            {
                "type": "paragraph",
                "text": (
                    "O JBox é um dos parceiros do projeto da Mangateca, "
                    "auxiliando na parte logística e de divulgação. O site "
                    "não foi, nem será, beneficiário de nenhum valor arrecadado "
                    "pela campanha de apoio ao projeto."
                ),
            },
            {
                "type": "heading",
                "text": "Informações",
            },
            {
                "type": "paragraph",
                "text": "O quê? Mostra Dicria.",
            },
            {
                "type": "paragraph",
                "text": (
                    "Onde? Museu de Arte do Rio – Praça Mauá nº 10, Praça "
                    "Mauá – Rio de Janeiro/RJ."
                ),
            },
            {
                "type": "paragraph",
                "text": "Quando? 30/09, a partir das 14h.",
            },
            {
                "type": "paragraph",
                "text": "Preço: Entrada gratuita.",
            },
        ],
    },
}

FEATURED_ARTICLE_SLUGS = (
    "ordem-cronologica-cavaleiros-do-zodiaco",
    "critica-mortos-de-amor",
    "inuyasha-kanketsu-hen",
    "mostra-dicria",
)
