# -*- coding: utf-8 -*-
"""
teams_data.py
Datos de las 32 selecciones de FMMJ WORLD CUP UNITED 26: grupos, presidentes,
colores de anfitriones y convocatoria de 26 jugadores por selección.
100% autocontenido (no depende de ningún archivo externo), para evitar
problemas de despliegue en Streamlit Cloud / GitHub.
"""
import random

random.seed(2026)

GROUPS = {
    "A": [
        {"code": "MEX", "name": "México", "flag": "🇲🇽", "president": "Mati"},
        {"code": "KOR", "name": "Corea del Sur", "flag": "🇰🇷", "president": "Jnka"},
        {"code": "UKR", "name": "Ucrania", "flag": "🇺🇦", "president": "Dibu"},
        {"code": "NOR", "name": "Noruega", "flag": "🇳🇴", "president": "Mati"},
    ],
    "B": [
        {"code": "CAN", "name": "Canadá", "flag": "🇨🇦", "president": "Jnka"},
        {"code": "SUI", "name": "Suiza", "flag": "🇨🇭", "president": "Dibu"},
        {"code": "ITA", "name": "Italia", "flag": "🇮🇹", "president": "Jnka"},
        {"code": "ARG", "name": "Argentina", "flag": "🇦🇷", "president": "Mati"},
    ],
    "C": [
        {"code": "BRA", "name": "Brasil", "flag": "🇧🇷", "president": "Jnka"},
        {"code": "MAR", "name": "Marruecos", "flag": "🇲🇦", "president": "Mati"},
        {"code": "SCO", "name": "Escocia", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "president": "Dibu"},
        {"code": "POR", "name": "Portugal", "flag": "🇵🇹", "president": "Dibu"},
    ],
    "D": [
        {"code": "USA", "name": "Estados Unidos", "flag": "🇺🇸", "president": "Mati"},
        {"code": "PAR", "name": "Paraguay", "flag": "🇵🇾", "president": "Dibu"},
        {"code": "TUR", "name": "Turquía", "flag": "🇹🇷", "president": "Mati"},
        {"code": "ENG", "name": "Inglaterra", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "president": "Jnka"},
    ],
    "E": [
        {"code": "GER", "name": "Alemania", "flag": "🇩🇪", "president": "Jnka"},
        {"code": "AUT", "name": "Austria", "flag": "🇦🇹", "president": "Mati"},
        {"code": "ECU", "name": "Ecuador", "flag": "🇪🇨", "president": "Dibu"},
        {"code": "CUW", "name": "Curazao", "flag": "🇨🇼", "president": "Dibu"},
    ],
    "F": [
        {"code": "NED", "name": "Países Bajos", "flag": "🇳🇱", "president": "Mati"},
        {"code": "JPN", "name": "Japón", "flag": "🇯🇵", "president": "Jnka"},
        {"code": "SWE", "name": "Suecia", "flag": "🇸🇪", "president": "Dibu"},
        {"code": "SEN", "name": "Senegal", "flag": "🇸🇳", "president": "Jnka"},
    ],
    "G": [
        {"code": "BEL", "name": "Bélgica", "flag": "🇧🇪", "president": "Dibu"},
        {"code": "COL", "name": "Colombia", "flag": "🇨🇴", "president": "Jnka"},
        {"code": "CRO", "name": "Croacia", "flag": "🇭🇷", "president": "Mati"},
        {"code": "CIV", "name": "Costa de Marfil", "flag": "🇨🇮", "president": "Mati"},
    ],
    "H": [
        {"code": "ESP", "name": "España", "flag": "🇪🇸", "president": "Mati"},
        {"code": "URU", "name": "Uruguay", "flag": "🇺🇾", "president": "Jnka"},
        {"code": "GHA", "name": "Ghana", "flag": "🇬🇭", "president": "Dibu"},
        {"code": "FRA", "name": "Francia", "flag": "🇫🇷", "president": "Dibu"},
    ],
}

HOSTS = {
    "MEX": {"color": "#006341", "name": "México"},   # verde
    "USA": {"color": "#0A3161", "name": "Estados Unidos"},  # azul
    "CAN": {"color": "#D80621", "name": "Canadá"},   # rojo
}

SURNAME_BANK = {
    "MEX": ["Hernández","García","Martínez","López","González","Rodríguez","Pérez","Sánchez","Ramírez","Flores","Torres","Vázquez","Reyes","Cruz","Morales","Ortiz","Gutiérrez","Chávez","Mendoza","Castro"],
    "KOR": ["Kim","Lee","Park","Choi","Jung","Kang","Cho","Yoon","Jang","Lim","Han","Oh","Seo","Shin","Kwon","Hwang","Song","Ahn","Yoo","Ko"],
    "UKR": ["Shevchenko","Kovalenko","Bondarenko","Tkachenko","Kravchenko","Oliynyk","Shevchuk","Kovalchuk","Melnyk","Boyko","Rudenko","Marchenko","Moroz","Fedorenko","Poliakov","Savchenko","Litvinenko","Pavlenko","Romanenko","Sydorenko"],
    "NOR": ["Hansen","Johansen","Olsen","Larsen","Andersen","Pedersen","Nilsen","Kristiansen","Jensen","Karlsen","Berg","Haugen","Solberg","Dahl","Strand","Moen","Aas","Lie","Bakken","Sæther"],
    "CAN": ["Smith","Brown","Tremblay","Martin","Roy","Gagnon","Wilson","MacDonald","Taylor","Campbell","Anderson","Lefebvre","Cormier","Leblanc","Fraser","Bergeron","Cote","Reid","Stewart","Clark"],
    "SUI": ["Müller","Meier","Schmid","Keller","Weber","Huber","Schneider","Meyer","Steiner","Fischer","Baumann","Gerber","Brunner","Bachmann","Wyss","Zimmermann","Frei","Moser","Widmer","Suter"],
    "ITA": ["Rossi","Russo","Ferrari","Esposito","Bianchi","Romano","Colombo","Ricci","Marino","Greco","Bruno","Gallo","Conti","De Luca","Costa","Giordano","Mancini","Rizzo","Lombardi","Moretti"],
    "ARG": ["González","Fernández","Rodríguez","López","Martínez","Díaz","Pérez","Sánchez","Romero","Álvarez","Torres","Ruiz","Ramírez","Flores","Acosta","Benítez","Medina","Herrera","Aguirre","Molina"],
    "BRA": ["Silva","Santos","Oliveira","Souza","Pereira","Costa","Rodrigues","Almeida","Nascimento","Lima","Araújo","Ferreira","Carvalho","Gomes","Martins","Barbosa","Ribeiro","Alves","Monteiro","Cardoso"],
    "MAR": ["El Amrani","Bennani","Tazi","Alaoui","Idrissi","Cherkaoui","Fassi","Benjelloun","Khattabi","Berrada","Yacoubi","Ouazzani","Sqalli","Chraibi","Bouzid","Amrani","Zouine","Naciri","Lahlou","Tahiri"],
    "SCO": ["Smith","Wilson","Robertson","Campbell","Stewart","Anderson","MacDonald","Scott","Reid","Murray","Taylor","Ross","Clark","Mitchell","Watson","Morrison","Kerr","Fraser","Duncan","Bell"],
    "POR": ["Silva","Santos","Ferreira","Pereira","Oliveira","Costa","Rodrigues","Martins","Sousa","Fernandes","Gonçalves","Gomes","Lopes","Marques","Alves","Almeida","Ribeiro","Pinto","Carvalho","Teixeira"],
    "USA": ["Johnson","Williams","Brown","Jones","Miller","Davis","Wilson","Anderson","Taylor","Thomas","Moore","Jackson","Martin","Lee","Walker","Young","Allen","King","Wright","Scott"],
    "PAR": ["González","Benítez","Ramírez","Rojas","Villalba","Ortiz","Aguilera","Riveros","Cáceres","Fernández","Ayala","Ovelar","Sánchez","Ferreira","Gómez","Ledesma","Franco","Duarte","Insfrán","Peralta"],
    "TUR": ["Yılmaz","Kaya","Demir","Şahin","Çelik","Yıldız","Yıldırım","Öztürk","Aydın","Özdemir","Arslan","Doğan","Kılıç","Aslan","Çetin","Kara","Koç","Kurt","Özkan","Şimşek"],
    "ENG": ["Smith","Jones","Taylor","Brown","Williams","Wilson","Johnson","Davies","Robinson","Wright","Thompson","Evans","Walker","White","Roberts","Green","Hall","Wood","Jackson","Clarke"],
    "GER": ["Müller","Schmidt","Schneider","Fischer","Weber","Meyer","Wagner","Becker","Schulz","Hoffmann","Koch","Richter","Klein","Wolf","Neumann","Braun","Zimmermann","Krüger","Hartmann","Lange"],
    "AUT": ["Gruber","Huber","Bauer","Wagner","Müller","Pichler","Steiner","Moser","Berger","Fuchs","Eder","Fischer","Schmid","Winkler","Weber","Schwarz","Maier","Leitner","Wimmer","Auer"],
    "ECU": ["Vera","Zambrano","Cedeño","Mendoza","Alvarado","Andrade","Chávez","Salazar","Pincay","Quiñónez","Delgado","Vélez","Loor","Bravo","Macías","Suárez","Vásquez","Guerrero","Chalá","Angulo"],
    "CUW": ["Martina","Isenia","Statia","Girigorie","Felida","Rojer","Wiel","Simmons","Livera","Croes","Boekhoudt","Winklaar","Emerenciana","Antonio","Damian","Pieters","Balentina","Thodé","Coffie","Tromp"],
    "NED": ["De Jong","Jansen","De Vries","Van den Berg","Van Dijk","Bakker","Visser","Smit","Meijer","De Boer","Mulder","De Groot","Bos","Vos","Peters","Hendriks","Van Leeuwen","Dekker","Brouwer","De Wit"],
    "JPN": ["Sato","Suzuki","Takahashi","Tanaka","Watanabe","Ito","Yamamoto","Nakamura","Kobayashi","Kato","Yoshida","Yamada","Sasaki","Yamaguchi","Matsumoto","Inoue","Kimura","Hayashi","Shimizu","Saito"],
    "SWE": ["Andersson","Johansson","Karlsson","Nilsson","Eriksson","Larsson","Olsson","Persson","Svensson","Gustafsson","Pettersson","Jonsson","Jansson","Hansson","Bengtsson","Jönsson","Lindberg","Jakobsson","Magnusson","Olofsson"],
    "SEN": ["Diop","Ndiaye","Diallo","Fall","Sarr","Gueye","Ba","Sy","Mbaye","Sow","Cissé","Faye","Sane","Diagne","Kane","Diouf","Thiam","Wade","Camara","Toure"],
    "BEL": ["Peeters","Janssens","Maes","Jacobs","Mertens","Willems","Claes","Goossens","Wouters","De Smet","Dubois","Lambert","Simon","Martin","Michel","Leclercq","Dupont","Renard","Lemoine","Fontaine"],
    "COL": ["Rodríguez","García","Martínez","López","Gómez","Rojas","Torres","Ramírez","Vargas","Castro","Ortiz","Muñoz","Moreno","Jiménez","Herrera","Suárez","Rivera","Peña","Gutiérrez","Cárdenas"],
    "CRO": ["Horvat","Kovačević","Babić","Marić","Jurić","Novak","Vuković","Kovačić","Knežević","Božić","Matić","Perić","Petrović","Radić","Tomić","Barišić","Grgić","Blažević","Šimić","Vidović"],
    "CIV": ["Kouassi","Koné","Traoré","Diabaté","Ouattara","Bamba","Yao","Kouadio","Coulibaly","Diallo","Bakayoko","Kra","Aka","N'Guessan","Konan","Toure","Camara","Diarra","Zadi","Yeo"],
    "ESP": ["García","Rodríguez","González","Fernández","López","Martínez","Sánchez","Pérez","Gómez","Martín","Jiménez","Ruiz","Hernández","Díaz","Moreno","Álvarez","Muñoz","Romero","Alonso","Gutiérrez"],
    "URU": ["Rodríguez","González","Fernández","Pérez","Martínez","Sosa","Silva","Suárez","Pereira","Gómez","Ferreira","Correa","Barrios","Acosta","Bentancur","Cáceres","De León","Techera","Olivera","Núñez"],
    "GHA": ["Mensah","Owusu","Boateng","Asante","Osei","Adjei","Appiah","Amoah","Agyeman","Darko","Yeboah","Amponsah","Frimpong","Acheampong","Gyasi","Ofori","Kusi","Adu","Sarpong","Nkrumah"],
    "FRA": ["Martin","Bernard","Dubois","Thomas","Robert","Richard","Petit","Durand","Leroy","Moreau","Simon","Laurent","Michel","Garcia","David","Bertrand","Roux","Vincent","Fontaine","Rousseau"],
}

INITIALS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def _gen_squad(code):
    surnames = SURNAME_BANK[code]
    combos = []
    for s in surnames:
        for i in INITIALS:
            combos.append(f"{i}. {s}")
    rnd = random.Random(f"{code}-2026")  # generador propio determinístico por selección
    rnd.shuffle(combos)
    positions = (["POR"] * 3) + (["DEF"] * 8) + (["MED"] * 8) + (["DEL"] * 7)
    squad = []
    for idx in range(26):
        squad.append({"dorsal": idx + 1, "nombre": combos[idx], "posicion": positions[idx]})
    return squad


def _build_teams():
    teams = {}
    for group_letter, teamlist in GROUPS.items():
        for t in teamlist:
            teams[t["code"]] = {
                "code": t["code"],
                "name": t["name"],
                "flag": t["flag"],
                "president": t["president"],
                "group": group_letter,
                "is_host": t["code"] in HOSTS,
                "squad": _gen_squad(t["code"]),
            }
    return teams


TEAMS = _build_teams()
