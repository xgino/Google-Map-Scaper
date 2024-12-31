import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def generate_keywords(config, num):
    """
    Generate keyword combinations and save to a .txt file.

    Args:
        config (dict): Contains "countries", "places", and "keywords".
        num (int): Identifier for the output file.

    Returns:
        str: Name of the generated file.
    """
    countries = config.get("countries", [])
    places = config.get("places", [])
    keywords = config.get("keywords", [])

    combinations = [
        f"{c}, {p}, {k}"
        for c in countries
        for p in places
        for k in keywords
    ]

    filename = f"./keywords_{num}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(combinations))

    logging.info(f"Saved {len(combinations)} keywords to {filename}.")
    return filename


def main():
    # Configurations for generating keywords
    # Marketing Agency, Advertising Agency, Digital Marketing, Event Planner
    # Event Management, Restaurants, Startup, Retail

    done = [
        "Gyms", "Fitness", "Consultants", "Recruitment Agencies", "Sales Teams",
        "Restaurants", "Tourism", "Freelancers", "Coworking Spaces", "B2B",
        "Digital Advertising", "Retail Stores", "Branding", "Event Organizers", "IT Services",
        "Tech-Savvy", "Tech", "Branding Agencies", "Networking Events", "Real Estate Agencies",
        "Marketing Agency", "Advertising Agency", "Digital Marketing", "Event Planner",
        "Event Management", "Startup", "Retail"
    ]

    mailplus_keywords = [
        # Marketing and Advertising
        "digital marketing agency", "SEO consultant", "content marketing firm", 
        "branding agency", "advertising agency", "lead generation company", 
        "social media marketing agency",

        # Sales and Recruitment
        "sales consulting firm", "sales training company", "recruitment agency",
        "headhunting service", "B2B sales team", "sales outsourcing service",

        # Startups and Tech
        "tech startup", "SaaS company", "mobile app developer", 
        "AI company", "cloud service provider", "software development company", 
        "web development agency",

        # Professional Services
        "consulting firm", "business strategy consultant", "financial advisory firm", 
        "accounting firm", "tax consultancy", "law firm", 

        # E-commerce and Retail
        "e-commerce business", "online store owner", "retail chain", 
        "boutique shop", "dropshipping company", "wholesale distributor",

        # Real Estate
        "real estate agency", "commercial real estate broker", 
        "property management company", "real estate developer", 

        # Education and Training
        "corporate training provider", "vocational training center", 
        "online course creator", "educational consultant", "tutoring service", 

        # Healthcare and Wellness
        "private clinic", "medical device company", "fitness trainer", 
        "yoga studio", "nutritionist service", "wellness coach", 

        # Events and Entertainment
        "event planner", "wedding organizer", "conference organizer", 
        "trade show exhibitor", "festival promoter", "party rental company",

        # Manufacturing and Industry
        "industrial equipment supplier", "B2B wholesaler", "machinery manufacturer", 
        "factory owner", "automotive parts distributor",

        # Logistics and Transportation
        "courier service", "freight forwarding company", "logistics provider", 
        "fleet management company", "shipping company", "moving service",

        # Non-Profit Organizations
        "charity organization", "non-profit organization", "advocacy group", 
        "community outreach program", "educational foundation", 

        # Freelancers and Consultants
        "freelance copywriter", "freelance graphic designer", 
        "business consultant", "freelance marketer", "career coach", 

        # Miscellaneous
        "B2B service provider", "networking event organizer", 
        "franchise business owner", "corporate service provider"
    ]

    Bolar_keywords = [
            # Marketing and Advertising
            "digital marketing agency", "social media agency", "SEO consultant",
            "content marketing specialist", "pay-per-click advertising", "branding agency",
            
            # Real Estate and Construction
            "real estate agency", "commercial property broker", "architectural design firm",
            "construction company", "interior design studio", "property developer",

            # Retail and Consumer Goods
            "retail store", "wholesale distributor", "grocery store chain",
            "franchise business", "e-commerce business", "boutique store",

            # Automotive
            "car dealership", "vehicle rental company", "auto parts store",
            "car wash", "fleet management service", "auto repair shop",

            # Food and Hospitality
            "restaurant chain", "catering company", "coffee shop franchise",
            "hotel", "resort", "food truck",

            # Professional Services
            "consulting firm", "recruitment agency", "IT service provider",
            "financial advisor", "accounting firm", "law firm",

            # Education and Training
            "vocational training institute", "corporate training provider", 
            "online education platform", "university", "tutoring service",

            # Healthcare and Wellness
            "private clinic", "fitness center", "yoga studio", "spa", 
            "wellness retreat", "chiropractic clinic",

            # Logistics and Transportation
            "courier service", "shipping company", "moving company",
            "trucking company", "logistics provider", "freight forwarding service",

            # Events and Entertainment
            "event planner", "wedding planner", "trade show organizer",
            "concert promoter", "festival organizer", "party rental service",

            # Technology and Startups
            "SaaS company", "IT consulting firm", "mobile app developer",
            "cloud service provider", "tech startup", "software company",

            # Manufacturing and Industry
            "industrial supplier", "machinery manufacturer", "B2B wholesaler",
            "factory", "equipment rental service", "industrial automation company",

            # Non-Profits and Public Organizations
            "community center", "advocacy group", "charity organization",
            "non-profit organization", "educational foundation", "youth center"
        ]


    configs_list = [
        {
            "countries": ["Nederland"],
            "places": [
                "Aa en Hunze", "Aalsmeer", "Aalten", "Aanschot", "Achtkarspelen", "Alblasserdam", "Albrandswaard", "Alkmaar",
                "Almelo", "Almere", "Alphen aan den Rijn", "Altena", "Amersfoort", "Amstelveen", "Amsterdam", "Apeldoorn",
                "Arnhem", "Assen", "Asten", "Baarn", "Barendrecht", "Barneveld", "Beekdaelen", "Berg en Dal",
                "Bergeijk", "Bergen op Zoom", "Berkelland", "Bernheze", "Best", "Beuningen", "Beuningen", "Beverwijk",
                "Binnenstad", "Binnenstad-Noord", "Bladel", "Bloemendaal", "Bodegraven-Reeuwijk", "Borger-Odoorn", "Borne", "Borsele",
                "Bos- en Gasthuisdistrict", "Boskoop", "Boxtel", "Breda", "Breda centrum", "Breda noord", "Breda noord-west", "Breda oost",
                "Breda west", "Breda zuid-oost", "Bronckhorst", "Brummen", "Brunssum", "Buitenveldert-West", "Bunschoten", "Buren",
                "Buytenwegh de Leyens", "Capelle aan den IJssel", "Castricum", "Centrum", "Centrum", "Centrum", "Charlois", "Coevorden",
                "Cranendonck", "Cuijk", "Culemborg", "Culemborg Oost", "Dalfsen", "Dantumadiel", "De Bilt", "De Fryske Marren",
                "De Mare", "De Ronde Venen", "De Wolden", "Delfshaven", "Delft", "Den Helder", "Deurne", "Deventer",
                "Diemen", "Dijk en Waard", "Dinkelland", "Doetinchem", "Dongen", "Dongen", "Dordrecht", "Drechterland",
                "Driebergen", "Drimmelen", "Dronten", "Druten", "Duiven", "Dukenburg", "Echt-Susteren", "Edam-Volendam",
                "Ede", "Ede-West", "Eemsdelta", "Eersel", "Eijsden-Margraten", "Eindhoven", "Elburg", "Emmen",
                "Enkhuizen", "Enschede", "Epe", "Ermelo", "Erp", "Etten-Leur", "Feijenoord", "Frankendael",
                "Geertruidenberg", "Geldrop", "Geldrop-Mierlo", "Gemert-Bakel", "Gennep", "Geuzenveld", "Gilze en Rijen", "Goeree-Overflakkee",
                "Goes", "Goirle", "Gooise Meren", "Gorinchem", "Gouda", "Graafsepoort", "Groningen", "Gulpen-Wittem",
                "Haaksbergen", "Haarlem", "Haarlemmermeer", "Halderberge", "Hardenberg", "Hardenberg", "Harderwijk", "Hardinxveld-Giessendam",
                "Harlingen", "Heemskerk", "Heemstede", "Heerde", "Heerenveen", "Heerlen", "Heeze-Leende", "Heiloo",
                "Hellendoorn", "Helmond", "Helpman e.o.", "Hendrik-Ido-Ambacht", "Het Hogeland", "Heumen", "Heusden", "Hillegersberg-Schiebroek",
                "Hillegom", "Hilvarenbeek", "Hilversum", "Hoeksche Waard", "Hof van Twente", "Hollands Kroon", "Hoofddorp", "Hoogeveen",
                "Hoogvliet", "Hoorn", "Horst aan de Maas", "Houten", "Huissen", "Huizen", "Hulst", "IJsselmonde",
                "IJsselstein", "Jordaan", "Kaag en Braassem", "Kampen", "Kampen", "Katwijk", "Katwijk aan Zee", "Kerk en Zanen",
                "Kerkrade", "Koggenland", "Kralingen-Crooswijk", "Krimpen aan den IJssel", "Krimpenerwaard", "Laarbeek", "Land van Cuijk", "Landgraaf",
                "Landlust", "Lansingerland", "Leeuwarden", "Leiden", "Leiden-Noord", "Leiderdorp", "Leidschendam-Voorburg", "Lelystad",
                "Leudal", "Leusden", "Lingewaard", "Lisse", "Lochem", "Loon op Zand", "Losser", "Maasdriel",
                "Maasgouw", "Maashorst", "Maaspoort", "Maassluis", "Maastricht", "Medemblik", "Meerssen", "Meerzicht",
                "Meierijstad", "Meppel", "Midden-Delfland", "Midden-Drenthe", "Midden-Groningen", "Middenmeer", "Mijdrecht", "Moerdijk",
                "Molenlanden", "Montferland", "Museumkwartier", "Naarden", "Neder-Betuwe", "Nederweert", "Nieuw-Vennep", "Nieuw-West",
                "Nieuwe Pijp", "Nieuwegein", "Nieuwerkerk aan den IJssel wijk 04", "Nieuwkoop", "Nijkerk", "Nijkerk-stad", "Nijmegen", "Nijmegen-Midden",
                "Nijmegen-Nieuw-West", "Nijmegen-Noord", "Nijmegen-Oost", "Nijmegen-Oud-West", "Nijmegen-Zuid", "Nissewaard", "Noord", "Noord",
                "Noord woongebied", "Noorddijk e.o.", "Noordenveld", "Noordoost", "Noordoost", "Noordoostpolder", "Noordwest", "Noordwijk",
                "Noordwijk Binnen", "Nootdorp", "Nuenen, Gerwen en Nederwetten", "Nunspeet", "Oegstgeest", "Oirschot", "Oisterwijk", "Oldambt",
                "Oldebroek", "Oldenzaal", "Olst-Wijhe", "Ommen", "Ontginning", "Oost", "Oost", "Oost Gelre",
                "Oostelijk Havengebied", "Oosterheem", "Oosterhout", "Oosterparkwijk", "Ooststellingwerf", "Opsterland", "Osdorp-Oost", "Oss",
                "Oud-Beijerland", "Oud-Gestel", "Oud-Noord", "Oud-Oost", "Oud-Strijp", "Oud-West", "Oud-Zuid", "Oude IJsselstreek",
                "Oude Pijp", "Oude Stad", "Overbetuwe", "Overschie", "Papendrecht", "Peel en Maas", "Pijnacker", "Pijnacker-Nootdorp",
                "Prins Alexander", "Purmerend", "Putten", "Putten", "Raalte", "Raalte", "Reimerswaal", "Renkum",
                "Rheden", "Rhenen", "Ridderkerk", "Rijen", "Rijnsburg", "Rijssen-Holten", "Roerdalen", "Roermond",
                "Rokkeveen", "Roodenburgerdistrict", "Roosendaal", "Rotterdam", "Rotterdam Centrum", "Rucphen", "Schagen", "Scheldebuurt",
                "Schiedam", "Schijndel", "Schil rondom het centrum", "Schouwen-Duiveland", "Seghwaert", "Sint-Michielsgestel", "Sint-Oedenrode", "Sittard-Geleen",
                "Sliedrecht", "Sluis", "Smallingerland", "Soest", "Someren", "Son en Breugel", "Staatsliedenbuurt", "Stadskanaal",
                "Stadskanaal", "Stede Broec", "Steenbergen", "Steenwijk", "Steenwijkerland", "Stichtse Vecht", "Terneuzen", "Texel",
                "Teylingen", "Tholen", "Tiel", "Tiel kern", "Tilburg", "Tubbergen", "Twenterand", "Tynaarlo",
                "Tytsjerksteradiel", "Uden", "Uithoorn", "Urk", "Utrecht", "Utrechtse Heuvelrug", "Valkenburg aan de Geul", "Valkenswaard",
                "Veendam", "Veenendaal", "Veere", "Veghel", "Veldhoven", "Velsen", "Venlo", "Venray",
                "Vijfheerenlanden", "Vlaardingen", "Vlissingen", "Voorne aan Zee", "Voorschoten", "Voorst", "Vught", "Waadhoeke",
                "Waalre", "Waalwijk", "Waalwijk", "Waddinxveen", "Wageningen", "Wassenaar", "Waterland", "Weert",
                "West", "West", "West Betuwe", "West Maas en Waal", "Westerkwartier", "Westerveld", "Westerwolde", "Westland",
                "Westlandgracht", "Weststellingwerf", "Wierden", "Wijchen", "Wijdemeren", "Wijk 00", "Wijk 00", "Wijk 00",
                "Wijk 00", "Wijk 00 Bergen op Zoom-Oude stad en omgeving", "Wijk 00 Best", "Wijk 00 Binnensingelgebied", "Wijk 00 Borne", "Wijk 00 Boxtel", "Wijk 00 Centrum", "Wijk 00 Dieren",
                "Wijk 00 Epe", "Wijk 00 Harlingen", "Wijk 00 Heemstede-Centrum", "Wijk 00 IJsselstein", "Wijk 00 Kerkrade-West", "Wijk 00 Krimpen aan den IJssel", "Wijk 00 Nuenen", "Wijk 00 Nunspeet",
                "Wijk 00 Putten", "Wijk 00 Roden", "Wijk 00 Schaesberg", "Wijk 00 Stad", "Wijk 00 Urk", "Wijk 00 Valkenswaard", "Wijk 00 Veendam-kern", "Wijk 00 Veldhoven",
                "Wijk 00 Waalre", "Wijk 00 Wijk bij Duurstede", "Wijk 00 Winschoten", "Wijk 00 Zevenbergen", "Wijk 01 Drunen", "Wijk 01 Emmeloord", "Wijk 01 Goes", "Wijk 01 Heerenveen",
                "Wijk 01 Kerkrade-Oost", "Wijk 01 Maarssen", "Wijk 01 Naaldwijk", "Wijk 01 Noordoostelijk deel der gemeente", "Wijk 01 Sittard", "Wijk 01 Sneek", "Wijk 01 Twello-Nijbroek", "Wijk 01 West",
                "Wijk 01 Wijchen kern", "Wijk 01 Woerden-Midden", "Wijk 02 Bergen op Zoom-Oost", "Wijk 02 Boswinkel - Stadsveld", "Wijk 02 Buitenwijk West", "Wijk 02 Didam", "Wijk 02 Noordwest", "Wijk 02 Overhoven",
                "Wijk 02 Overwhere", "Wijk 02 Velp", "Wijk 02 Volendam", "Wijk 03 Overvecht", "Wijk 04 Benoordenhout", "Wijk 04 Buitenwijk Oost", "Wijk 04 Enschede-Noord", "Wijk 04 Noordoost",
                "Wijk 05 Geleen", "Wijk 05 Oost", "Wijk 05 Vlijmen", "Wijk 06 Binnenstad", "Wijk 06 Buitenwijk Zuidoost", "Wijk 06 Enschede-Zuid", "Wijk 06 Nieuwland", "Wijk 07 Scheveningen",
                "Wijk 07 Weidevenne", "Wijk 07 Zuid", "Wijk 08 Glanerbrug en omgeving", "Wijk 08 Zuidwest", "Wijk 09 Geuzen- en Statenkwartier", "Wijk 09 Leidsche Rijn", "Wijk 09 Sterrenburg", "Wijk 10 Binnenstad",
                "Wijk 10 Coevorden", "Wijk 10 Vleuten-De Meern", "Wijk 11 Binnenstad", "Wijk 11 Stadspolders", "Wijk 12 Bomen- en Bloemenbuurt", "Wijk 12 Maarssenbroek", "Wijk 17 Loosduinen", "Wijk 18 Waldeck",
                "Wijk 20 Valkenboskwartier", "Wijk 21 Regentessekwartier", "Wijk 22 Stadshagen", "Wijk 24 Voorhof", "Wijk 25 Buitenhof", "Wijk 25 Mariahoeve en Marlot", "Wijk 26 Bezuidenhout", "Wijk 27 Stationsbuurt",
                "Wijk 28 Centrum", "Wijk 28 Wippolder", "Wijk 29 Schildersbuurt", "Wijk 31 Rustenburg en Oostbroek", "Wijk 32 Leyenburg", "Wijk 33 Bouwlust", "Wijk 33 Kersenboogerd-Zuid", "Wijk 34 Morgenstond",
                "Wijk 36 Moerwijk", "Wijk 38 Laakkwartier en Spoorwijk", "Wijk 40 Wateringse Veld", "Wijk 42 Ypenburg", "Wijk 44 Leidschenveen", "Wijk 50 Hoogeveen", "Wijk 54 Barneveld", "Wijk bij Duurstede",
                "Winterswijk", "Woensdrecht", "Woerden", "Wormerland", "Zaanstad", "Zaltbommel", "Zandvoort", "Zeewolde",
                "Zeist", "Zeist Centrum", "Zeist-Noord", "Zevenaar", "Zevenaar", "Zoetermeer", "Zuid", "Zuid",
                "Zuid", "Zuidoost", "Zuidoost", "Zuidplas", "Zundert", "Zutphen", "Zwartewaterland", "Zwijndrecht",
                "Zwolle"
            ],
            "keywords": ["Healthcare Clinics", "Hospitals", "Medical Centers", "Dental Offices", "E-commerce Stores", "Online Marketplaces", "Dropshipping Businesses", "Automobile Showrooms", "Architectural Studios", "Beauty Salons", "Spas", "Wellness Centers"],
        },
        {
            "countries": ["Nederland"],
            "places": [
                "Aa en Hunze", "Aalsmeer", "Aalten", "Aanschot", "Achtkarspelen", "Alblasserdam", "Albrandswaard", "Alkmaar",
                "Almelo", "Almere", "Alphen aan den Rijn", "Altena", "Amersfoort", "Amstelveen", "Amsterdam", "Apeldoorn",
                "Arnhem", "Assen", "Asten", "Baarn", "Barendrecht", "Barneveld", "Beekdaelen", "Berg en Dal",
                "Bergeijk", "Bergen op Zoom", "Berkelland", "Bernheze", "Best", "Beuningen", "Beuningen", "Beverwijk",
                "Binnenstad", "Binnenstad-Noord", "Bladel", "Bloemendaal", "Bodegraven-Reeuwijk", "Borger-Odoorn", "Borne", "Borsele",
                "Bos- en Gasthuisdistrict", "Boskoop", "Boxtel", "Breda", "Breda centrum", "Breda noord", "Breda noord-west", "Breda oost",
                "Breda west", "Breda zuid-oost", "Bronckhorst", "Brummen", "Brunssum", "Buitenveldert-West", "Bunschoten", "Buren",
                "Buytenwegh de Leyens", "Capelle aan den IJssel", "Castricum", "Centrum", "Centrum", "Centrum", "Charlois", "Coevorden",
                "Cranendonck", "Cuijk", "Culemborg", "Culemborg Oost", "Dalfsen", "Dantumadiel", "De Bilt", "De Fryske Marren",
                "De Mare", "De Ronde Venen", "De Wolden", "Delfshaven", "Delft", "Den Helder", "Deurne", "Deventer",
                "Diemen", "Dijk en Waard", "Dinkelland", "Doetinchem", "Dongen", "Dongen", "Dordrecht", "Drechterland",
                "Driebergen", "Drimmelen", "Dronten", "Druten", "Duiven", "Dukenburg", "Echt-Susteren", "Edam-Volendam",
                "Ede", "Ede-West", "Eemsdelta", "Eersel", "Eijsden-Margraten", "Eindhoven", "Elburg", "Emmen",
                "Enkhuizen", "Enschede", "Epe", "Ermelo", "Erp", "Etten-Leur", "Feijenoord", "Frankendael",
                "Geertruidenberg", "Geldrop", "Geldrop-Mierlo", "Gemert-Bakel", "Gennep", "Geuzenveld", "Gilze en Rijen", "Goeree-Overflakkee",
                "Goes", "Goirle", "Gooise Meren", "Gorinchem", "Gouda", "Graafsepoort", "Groningen", "Gulpen-Wittem",
                "Haaksbergen", "Haarlem", "Haarlemmermeer", "Halderberge", "Hardenberg", "Hardenberg", "Harderwijk", "Hardinxveld-Giessendam",
                "Harlingen", "Heemskerk", "Heemstede", "Heerde", "Heerenveen", "Heerlen", "Heeze-Leende", "Heiloo",
                "Hellendoorn", "Helmond", "Helpman e.o.", "Hendrik-Ido-Ambacht", "Het Hogeland", "Heumen", "Heusden", "Hillegersberg-Schiebroek",
                "Hillegom", "Hilvarenbeek", "Hilversum", "Hoeksche Waard", "Hof van Twente", "Hollands Kroon", "Hoofddorp", "Hoogeveen",
                "Hoogvliet", "Hoorn", "Horst aan de Maas", "Houten", "Huissen", "Huizen", "Hulst", "IJsselmonde",
                "IJsselstein", "Jordaan", "Kaag en Braassem", "Kampen", "Kampen", "Katwijk", "Katwijk aan Zee", "Kerk en Zanen",
                "Kerkrade", "Koggenland", "Kralingen-Crooswijk", "Krimpen aan den IJssel", "Krimpenerwaard", "Laarbeek", "Land van Cuijk", "Landgraaf",
                "Landlust", "Lansingerland", "Leeuwarden", "Leiden", "Leiden-Noord", "Leiderdorp", "Leidschendam-Voorburg", "Lelystad",
                "Leudal", "Leusden", "Lingewaard", "Lisse", "Lochem", "Loon op Zand", "Losser", "Maasdriel",
                "Maasgouw", "Maashorst", "Maaspoort", "Maassluis", "Maastricht", "Medemblik", "Meerssen", "Meerzicht",
                "Meierijstad", "Meppel", "Midden-Delfland", "Midden-Drenthe", "Midden-Groningen", "Middenmeer", "Mijdrecht", "Moerdijk",
                "Molenlanden", "Montferland", "Museumkwartier", "Naarden", "Neder-Betuwe", "Nederweert", "Nieuw-Vennep", "Nieuw-West",
                "Nieuwe Pijp", "Nieuwegein", "Nieuwerkerk aan den IJssel wijk 04", "Nieuwkoop", "Nijkerk", "Nijkerk-stad", "Nijmegen", "Nijmegen-Midden",
                "Nijmegen-Nieuw-West", "Nijmegen-Noord", "Nijmegen-Oost", "Nijmegen-Oud-West", "Nijmegen-Zuid", "Nissewaard", "Noord", "Noord",
                "Noord woongebied", "Noorddijk e.o.", "Noordenveld", "Noordoost", "Noordoost", "Noordoostpolder", "Noordwest", "Noordwijk",
                "Noordwijk Binnen", "Nootdorp", "Nuenen, Gerwen en Nederwetten", "Nunspeet", "Oegstgeest", "Oirschot", "Oisterwijk", "Oldambt",
                "Oldebroek", "Oldenzaal", "Olst-Wijhe", "Ommen", "Ontginning", "Oost", "Oost", "Oost Gelre",
                "Oostelijk Havengebied", "Oosterheem", "Oosterhout", "Oosterparkwijk", "Ooststellingwerf", "Opsterland", "Osdorp-Oost", "Oss",
                "Oud-Beijerland", "Oud-Gestel", "Oud-Noord", "Oud-Oost", "Oud-Strijp", "Oud-West", "Oud-Zuid", "Oude IJsselstreek",
                "Oude Pijp", "Oude Stad", "Overbetuwe", "Overschie", "Papendrecht", "Peel en Maas", "Pijnacker", "Pijnacker-Nootdorp",
                "Prins Alexander", "Purmerend", "Putten", "Putten", "Raalte", "Raalte", "Reimerswaal", "Renkum",
                "Rheden", "Rhenen", "Ridderkerk", "Rijen", "Rijnsburg", "Rijssen-Holten", "Roerdalen", "Roermond",
                "Rokkeveen", "Roodenburgerdistrict", "Roosendaal", "Rotterdam", "Rotterdam Centrum", "Rucphen", "Schagen", "Scheldebuurt",
                "Schiedam", "Schijndel", "Schil rondom het centrum", "Schouwen-Duiveland", "Seghwaert", "Sint-Michielsgestel", "Sint-Oedenrode", "Sittard-Geleen",
                "Sliedrecht", "Sluis", "Smallingerland", "Soest", "Someren", "Son en Breugel", "Staatsliedenbuurt", "Stadskanaal",
                "Stadskanaal", "Stede Broec", "Steenbergen", "Steenwijk", "Steenwijkerland", "Stichtse Vecht", "Terneuzen", "Texel",
                "Teylingen", "Tholen", "Tiel", "Tiel kern", "Tilburg", "Tubbergen", "Twenterand", "Tynaarlo",
                "Tytsjerksteradiel", "Uden", "Uithoorn", "Urk", "Utrecht", "Utrechtse Heuvelrug", "Valkenburg aan de Geul", "Valkenswaard",
                "Veendam", "Veenendaal", "Veere", "Veghel", "Veldhoven", "Velsen", "Venlo", "Venray",
                "Vijfheerenlanden", "Vlaardingen", "Vlissingen", "Voorne aan Zee", "Voorschoten", "Voorst", "Vught", "Waadhoeke",
                "Waalre", "Waalwijk", "Waalwijk", "Waddinxveen", "Wageningen", "Wassenaar", "Waterland", "Weert",
                "West", "West", "West Betuwe", "West Maas en Waal", "Westerkwartier", "Westerveld", "Westerwolde", "Westland",
                "Westlandgracht", "Weststellingwerf", "Wierden", "Wijchen", "Wijdemeren", "Wijk 00", "Wijk 00", "Wijk 00",
                "Wijk 00", "Wijk 00 Bergen op Zoom-Oude stad en omgeving", "Wijk 00 Best", "Wijk 00 Binnensingelgebied", "Wijk 00 Borne", "Wijk 00 Boxtel", "Wijk 00 Centrum", "Wijk 00 Dieren",
                "Wijk 00 Epe", "Wijk 00 Harlingen", "Wijk 00 Heemstede-Centrum", "Wijk 00 IJsselstein", "Wijk 00 Kerkrade-West", "Wijk 00 Krimpen aan den IJssel", "Wijk 00 Nuenen", "Wijk 00 Nunspeet",
                "Wijk 00 Putten", "Wijk 00 Roden", "Wijk 00 Schaesberg", "Wijk 00 Stad", "Wijk 00 Urk", "Wijk 00 Valkenswaard", "Wijk 00 Veendam-kern", "Wijk 00 Veldhoven",
                "Wijk 00 Waalre", "Wijk 00 Wijk bij Duurstede", "Wijk 00 Winschoten", "Wijk 00 Zevenbergen", "Wijk 01 Drunen", "Wijk 01 Emmeloord", "Wijk 01 Goes", "Wijk 01 Heerenveen",
                "Wijk 01 Kerkrade-Oost", "Wijk 01 Maarssen", "Wijk 01 Naaldwijk", "Wijk 01 Noordoostelijk deel der gemeente", "Wijk 01 Sittard", "Wijk 01 Sneek", "Wijk 01 Twello-Nijbroek", "Wijk 01 West",
                "Wijk 01 Wijchen kern", "Wijk 01 Woerden-Midden", "Wijk 02 Bergen op Zoom-Oost", "Wijk 02 Boswinkel - Stadsveld", "Wijk 02 Buitenwijk West", "Wijk 02 Didam", "Wijk 02 Noordwest", "Wijk 02 Overhoven",
                "Wijk 02 Overwhere", "Wijk 02 Velp", "Wijk 02 Volendam", "Wijk 03 Overvecht", "Wijk 04 Benoordenhout", "Wijk 04 Buitenwijk Oost", "Wijk 04 Enschede-Noord", "Wijk 04 Noordoost",
                "Wijk 05 Geleen", "Wijk 05 Oost", "Wijk 05 Vlijmen", "Wijk 06 Binnenstad", "Wijk 06 Buitenwijk Zuidoost", "Wijk 06 Enschede-Zuid", "Wijk 06 Nieuwland", "Wijk 07 Scheveningen",
                "Wijk 07 Weidevenne", "Wijk 07 Zuid", "Wijk 08 Glanerbrug en omgeving", "Wijk 08 Zuidwest", "Wijk 09 Geuzen- en Statenkwartier", "Wijk 09 Leidsche Rijn", "Wijk 09 Sterrenburg", "Wijk 10 Binnenstad",
                "Wijk 10 Coevorden", "Wijk 10 Vleuten-De Meern", "Wijk 11 Binnenstad", "Wijk 11 Stadspolders", "Wijk 12 Bomen- en Bloemenbuurt", "Wijk 12 Maarssenbroek", "Wijk 17 Loosduinen", "Wijk 18 Waldeck",
                "Wijk 20 Valkenboskwartier", "Wijk 21 Regentessekwartier", "Wijk 22 Stadshagen", "Wijk 24 Voorhof", "Wijk 25 Buitenhof", "Wijk 25 Mariahoeve en Marlot", "Wijk 26 Bezuidenhout", "Wijk 27 Stationsbuurt",
                "Wijk 28 Centrum", "Wijk 28 Wippolder", "Wijk 29 Schildersbuurt", "Wijk 31 Rustenburg en Oostbroek", "Wijk 32 Leyenburg", "Wijk 33 Bouwlust", "Wijk 33 Kersenboogerd-Zuid", "Wijk 34 Morgenstond",
                "Wijk 36 Moerwijk", "Wijk 38 Laakkwartier en Spoorwijk", "Wijk 40 Wateringse Veld", "Wijk 42 Ypenburg", "Wijk 44 Leidschenveen", "Wijk 50 Hoogeveen", "Wijk 54 Barneveld", "Wijk bij Duurstede",
                "Winterswijk", "Woensdrecht", "Woerden", "Wormerland", "Zaanstad", "Zaltbommel", "Zandvoort", "Zeewolde",
                "Zeist", "Zeist Centrum", "Zeist-Noord", "Zevenaar", "Zevenaar", "Zoetermeer", "Zuid", "Zuid",
                "Zuid", "Zuidoost", "Zuidoost", "Zuidplas", "Zundert", "Zutphen", "Zwartewaterland", "Zwijndrecht",
                "Zwolle"
            ],
            "keywords": ["Universities", "Colleges", "Training Institutes", "Online Learning Platforms", "Hotels", "Resorts", "Guesthouses", "Vacation Rentals", "Aesthetic Clinics", "Photography Studios", "Photo Booth Rentals", "Vehicle Rental Services"],
        },
        {
            "countries": ["Nederland"],
            "places": [
                "Aa en Hunze", "Aalsmeer", "Aalten", "Aanschot", "Achtkarspelen", "Alblasserdam", "Albrandswaard", "Alkmaar",
                "Almelo", "Almere", "Alphen aan den Rijn", "Altena", "Amersfoort", "Amstelveen", "Amsterdam", "Apeldoorn",
                "Arnhem", "Assen", "Asten", "Baarn", "Barendrecht", "Barneveld", "Beekdaelen", "Berg en Dal",
                "Bergeijk", "Bergen op Zoom", "Berkelland", "Bernheze", "Best", "Beuningen", "Beuningen", "Beverwijk",
                "Binnenstad", "Binnenstad-Noord", "Bladel", "Bloemendaal", "Bodegraven-Reeuwijk", "Borger-Odoorn", "Borne", "Borsele",
                "Bos- en Gasthuisdistrict", "Boskoop", "Boxtel", "Breda", "Breda centrum", "Breda noord", "Breda noord-west", "Breda oost",
                "Breda west", "Breda zuid-oost", "Bronckhorst", "Brummen", "Brunssum", "Buitenveldert-West", "Bunschoten", "Buren",
                "Buytenwegh de Leyens", "Capelle aan den IJssel", "Castricum", "Centrum", "Centrum", "Centrum", "Charlois", "Coevorden",
                "Cranendonck", "Cuijk", "Culemborg", "Culemborg Oost", "Dalfsen", "Dantumadiel", "De Bilt", "De Fryske Marren",
                "De Mare", "De Ronde Venen", "De Wolden", "Delfshaven", "Delft", "Den Helder", "Deurne", "Deventer",
                "Diemen", "Dijk en Waard", "Dinkelland", "Doetinchem", "Dongen", "Dongen", "Dordrecht", "Drechterland",
                "Driebergen", "Drimmelen", "Dronten", "Druten", "Duiven", "Dukenburg", "Echt-Susteren", "Edam-Volendam",
                "Ede", "Ede-West", "Eemsdelta", "Eersel", "Eijsden-Margraten", "Eindhoven", "Elburg", "Emmen",
                "Enkhuizen", "Enschede", "Epe", "Ermelo", "Erp", "Etten-Leur", "Feijenoord", "Frankendael",
                "Geertruidenberg", "Geldrop", "Geldrop-Mierlo", "Gemert-Bakel", "Gennep", "Geuzenveld", "Gilze en Rijen", "Goeree-Overflakkee",
                "Goes", "Goirle", "Gooise Meren", "Gorinchem", "Gouda", "Graafsepoort", "Groningen", "Gulpen-Wittem",
                "Haaksbergen", "Haarlem", "Haarlemmermeer", "Halderberge", "Hardenberg", "Hardenberg", "Harderwijk", "Hardinxveld-Giessendam",
                "Harlingen", "Heemskerk", "Heemstede", "Heerde", "Heerenveen", "Heerlen", "Heeze-Leende", "Heiloo",
                "Hellendoorn", "Helmond", "Helpman e.o.", "Hendrik-Ido-Ambacht", "Het Hogeland", "Heumen", "Heusden", "Hillegersberg-Schiebroek",
                "Hillegom", "Hilvarenbeek", "Hilversum", "Hoeksche Waard", "Hof van Twente", "Hollands Kroon", "Hoofddorp", "Hoogeveen",
                "Hoogvliet", "Hoorn", "Horst aan de Maas", "Houten", "Huissen", "Huizen", "Hulst", "IJsselmonde",
                "IJsselstein", "Jordaan", "Kaag en Braassem", "Kampen", "Kampen", "Katwijk", "Katwijk aan Zee", "Kerk en Zanen",
                "Kerkrade", "Koggenland", "Kralingen-Crooswijk", "Krimpen aan den IJssel", "Krimpenerwaard", "Laarbeek", "Land van Cuijk", "Landgraaf",
                "Landlust", "Lansingerland", "Leeuwarden", "Leiden", "Leiden-Noord", "Leiderdorp", "Leidschendam-Voorburg", "Lelystad",
                "Leudal", "Leusden", "Lingewaard", "Lisse", "Lochem", "Loon op Zand", "Losser", "Maasdriel",
                "Maasgouw", "Maashorst", "Maaspoort", "Maassluis", "Maastricht", "Medemblik", "Meerssen", "Meerzicht",
                "Meierijstad", "Meppel", "Midden-Delfland", "Midden-Drenthe", "Midden-Groningen", "Middenmeer", "Mijdrecht", "Moerdijk",
                "Molenlanden", "Montferland", "Museumkwartier", "Naarden", "Neder-Betuwe", "Nederweert", "Nieuw-Vennep", "Nieuw-West",
                "Nieuwe Pijp", "Nieuwegein", "Nieuwerkerk aan den IJssel wijk 04", "Nieuwkoop", "Nijkerk", "Nijkerk-stad", "Nijmegen", "Nijmegen-Midden",
                "Nijmegen-Nieuw-West", "Nijmegen-Noord", "Nijmegen-Oost", "Nijmegen-Oud-West", "Nijmegen-Zuid", "Nissewaard", "Noord", "Noord",
                "Noord woongebied", "Noorddijk e.o.", "Noordenveld", "Noordoost", "Noordoost", "Noordoostpolder", "Noordwest", "Noordwijk",
                "Noordwijk Binnen", "Nootdorp", "Nuenen, Gerwen en Nederwetten", "Nunspeet", "Oegstgeest", "Oirschot", "Oisterwijk", "Oldambt",
                "Oldebroek", "Oldenzaal", "Olst-Wijhe", "Ommen", "Ontginning", "Oost", "Oost", "Oost Gelre",
                "Oostelijk Havengebied", "Oosterheem", "Oosterhout", "Oosterparkwijk", "Ooststellingwerf", "Opsterland", "Osdorp-Oost", "Oss",
                "Oud-Beijerland", "Oud-Gestel", "Oud-Noord", "Oud-Oost", "Oud-Strijp", "Oud-West", "Oud-Zuid", "Oude IJsselstreek",
                "Oude Pijp", "Oude Stad", "Overbetuwe", "Overschie", "Papendrecht", "Peel en Maas", "Pijnacker", "Pijnacker-Nootdorp",
                "Prins Alexander", "Purmerend", "Putten", "Putten", "Raalte", "Raalte", "Reimerswaal", "Renkum",
                "Rheden", "Rhenen", "Ridderkerk", "Rijen", "Rijnsburg", "Rijssen-Holten", "Roerdalen", "Roermond",
                "Rokkeveen", "Roodenburgerdistrict", "Roosendaal", "Rotterdam", "Rotterdam Centrum", "Rucphen", "Schagen", "Scheldebuurt",
                "Schiedam", "Schijndel", "Schil rondom het centrum", "Schouwen-Duiveland", "Seghwaert", "Sint-Michielsgestel", "Sint-Oedenrode", "Sittard-Geleen",
                "Sliedrecht", "Sluis", "Smallingerland", "Soest", "Someren", "Son en Breugel", "Staatsliedenbuurt", "Stadskanaal",
                "Stadskanaal", "Stede Broec", "Steenbergen", "Steenwijk", "Steenwijkerland", "Stichtse Vecht", "Terneuzen", "Texel",
                "Teylingen", "Tholen", "Tiel", "Tiel kern", "Tilburg", "Tubbergen", "Twenterand", "Tynaarlo",
                "Tytsjerksteradiel", "Uden", "Uithoorn", "Urk", "Utrecht", "Utrechtse Heuvelrug", "Valkenburg aan de Geul", "Valkenswaard",
                "Veendam", "Veenendaal", "Veere", "Veghel", "Veldhoven", "Velsen", "Venlo", "Venray",
                "Vijfheerenlanden", "Vlaardingen", "Vlissingen", "Voorne aan Zee", "Voorschoten", "Voorst", "Vught", "Waadhoeke",
                "Waalre", "Waalwijk", "Waalwijk", "Waddinxveen", "Wageningen", "Wassenaar", "Waterland", "Weert",
                "West", "West", "West Betuwe", "West Maas en Waal", "Westerkwartier", "Westerveld", "Westerwolde", "Westland",
                "Westlandgracht", "Weststellingwerf", "Wierden", "Wijchen", "Wijdemeren", "Wijk 00", "Wijk 00", "Wijk 00",
                "Wijk 00", "Wijk 00 Bergen op Zoom-Oude stad en omgeving", "Wijk 00 Best", "Wijk 00 Binnensingelgebied", "Wijk 00 Borne", "Wijk 00 Boxtel", "Wijk 00 Centrum", "Wijk 00 Dieren",
                "Wijk 00 Epe", "Wijk 00 Harlingen", "Wijk 00 Heemstede-Centrum", "Wijk 00 IJsselstein", "Wijk 00 Kerkrade-West", "Wijk 00 Krimpen aan den IJssel", "Wijk 00 Nuenen", "Wijk 00 Nunspeet",
                "Wijk 00 Putten", "Wijk 00 Roden", "Wijk 00 Schaesberg", "Wijk 00 Stad", "Wijk 00 Urk", "Wijk 00 Valkenswaard", "Wijk 00 Veendam-kern", "Wijk 00 Veldhoven",
                "Wijk 00 Waalre", "Wijk 00 Wijk bij Duurstede", "Wijk 00 Winschoten", "Wijk 00 Zevenbergen", "Wijk 01 Drunen", "Wijk 01 Emmeloord", "Wijk 01 Goes", "Wijk 01 Heerenveen",
                "Wijk 01 Kerkrade-Oost", "Wijk 01 Maarssen", "Wijk 01 Naaldwijk", "Wijk 01 Noordoostelijk deel der gemeente", "Wijk 01 Sittard", "Wijk 01 Sneek", "Wijk 01 Twello-Nijbroek", "Wijk 01 West",
                "Wijk 01 Wijchen kern", "Wijk 01 Woerden-Midden", "Wijk 02 Bergen op Zoom-Oost", "Wijk 02 Boswinkel - Stadsveld", "Wijk 02 Buitenwijk West", "Wijk 02 Didam", "Wijk 02 Noordwest", "Wijk 02 Overhoven",
                "Wijk 02 Overwhere", "Wijk 02 Velp", "Wijk 02 Volendam", "Wijk 03 Overvecht", "Wijk 04 Benoordenhout", "Wijk 04 Buitenwijk Oost", "Wijk 04 Enschede-Noord", "Wijk 04 Noordoost",
                "Wijk 05 Geleen", "Wijk 05 Oost", "Wijk 05 Vlijmen", "Wijk 06 Binnenstad", "Wijk 06 Buitenwijk Zuidoost", "Wijk 06 Enschede-Zuid", "Wijk 06 Nieuwland", "Wijk 07 Scheveningen",
                "Wijk 07 Weidevenne", "Wijk 07 Zuid", "Wijk 08 Glanerbrug en omgeving", "Wijk 08 Zuidwest", "Wijk 09 Geuzen- en Statenkwartier", "Wijk 09 Leidsche Rijn", "Wijk 09 Sterrenburg", "Wijk 10 Binnenstad",
                "Wijk 10 Coevorden", "Wijk 10 Vleuten-De Meern", "Wijk 11 Binnenstad", "Wijk 11 Stadspolders", "Wijk 12 Bomen- en Bloemenbuurt", "Wijk 12 Maarssenbroek", "Wijk 17 Loosduinen", "Wijk 18 Waldeck",
                "Wijk 20 Valkenboskwartier", "Wijk 21 Regentessekwartier", "Wijk 22 Stadshagen", "Wijk 24 Voorhof", "Wijk 25 Buitenhof", "Wijk 25 Mariahoeve en Marlot", "Wijk 26 Bezuidenhout", "Wijk 27 Stationsbuurt",
                "Wijk 28 Centrum", "Wijk 28 Wippolder", "Wijk 29 Schildersbuurt", "Wijk 31 Rustenburg en Oostbroek", "Wijk 32 Leyenburg", "Wijk 33 Bouwlust", "Wijk 33 Kersenboogerd-Zuid", "Wijk 34 Morgenstond",
                "Wijk 36 Moerwijk", "Wijk 38 Laakkwartier en Spoorwijk", "Wijk 40 Wateringse Veld", "Wijk 42 Ypenburg", "Wijk 44 Leidschenveen", "Wijk 50 Hoogeveen", "Wijk 54 Barneveld", "Wijk bij Duurstede",
                "Winterswijk", "Woensdrecht", "Woerden", "Wormerland", "Zaanstad", "Zaltbommel", "Zandvoort", "Zeewolde",
                "Zeist", "Zeist Centrum", "Zeist-Noord", "Zevenaar", "Zevenaar", "Zoetermeer", "Zuid", "Zuid",
                "Zuid", "Zuidoost", "Zuidoost", "Zuidplas", "Zundert", "Zutphen", "Zwartewaterland", "Zwijndrecht",
                "Zwolle"
            ],
            "keywords": ["Logistics Companies", "Courier Services", "Shipping Firms", "Freight Companies", "Factories", "Production Units", "Supply Chain Companies", "Car Dealerships", "Freelance Photographers", "Event Photographers", "Tech Startups"],
        },
        {
            "countries": ["Nederland"],
            "places": [
                "Aa en Hunze", "Aalsmeer", "Aalten", "Aanschot", "Achtkarspelen", "Alblasserdam", "Albrandswaard", "Alkmaar",
                "Almelo", "Almere", "Alphen aan den Rijn", "Altena", "Amersfoort", "Amstelveen", "Amsterdam", "Apeldoorn",
                "Arnhem", "Assen", "Asten", "Baarn", "Barendrecht", "Barneveld", "Beekdaelen", "Berg en Dal",
                "Bergeijk", "Bergen op Zoom", "Berkelland", "Bernheze", "Best", "Beuningen", "Beuningen", "Beverwijk",
                "Binnenstad", "Binnenstad-Noord", "Bladel", "Bloemendaal", "Bodegraven-Reeuwijk", "Borger-Odoorn", "Borne", "Borsele",
                "Bos- en Gasthuisdistrict", "Boskoop", "Boxtel", "Breda", "Breda centrum", "Breda noord", "Breda noord-west", "Breda oost",
                "Breda west", "Breda zuid-oost", "Bronckhorst", "Brummen", "Brunssum", "Buitenveldert-West", "Bunschoten", "Buren",
                "Buytenwegh de Leyens", "Capelle aan den IJssel", "Castricum", "Centrum", "Centrum", "Centrum", "Charlois", "Coevorden",
                "Cranendonck", "Cuijk", "Culemborg", "Culemborg Oost", "Dalfsen", "Dantumadiel", "De Bilt", "De Fryske Marren",
                "De Mare", "De Ronde Venen", "De Wolden", "Delfshaven", "Delft", "Den Helder", "Deurne", "Deventer",
                "Diemen", "Dijk en Waard", "Dinkelland", "Doetinchem", "Dongen", "Dongen", "Dordrecht", "Drechterland",
                "Driebergen", "Drimmelen", "Dronten", "Druten", "Duiven", "Dukenburg", "Echt-Susteren", "Edam-Volendam",
                "Ede", "Ede-West", "Eemsdelta", "Eersel", "Eijsden-Margraten", "Eindhoven", "Elburg", "Emmen",
                "Enkhuizen", "Enschede", "Epe", "Ermelo", "Erp", "Etten-Leur", "Feijenoord", "Frankendael",
                "Geertruidenberg", "Geldrop", "Geldrop-Mierlo", "Gemert-Bakel", "Gennep", "Geuzenveld", "Gilze en Rijen", "Goeree-Overflakkee",
                "Goes", "Goirle", "Gooise Meren", "Gorinchem", "Gouda", "Graafsepoort", "Groningen", "Gulpen-Wittem",
                "Haaksbergen", "Haarlem", "Haarlemmermeer", "Halderberge", "Hardenberg", "Hardenberg", "Harderwijk", "Hardinxveld-Giessendam",
                "Harlingen", "Heemskerk", "Heemstede", "Heerde", "Heerenveen", "Heerlen", "Heeze-Leende", "Heiloo",
                "Hellendoorn", "Helmond", "Helpman e.o.", "Hendrik-Ido-Ambacht", "Het Hogeland", "Heumen", "Heusden", "Hillegersberg-Schiebroek",
                "Hillegom", "Hilvarenbeek", "Hilversum", "Hoeksche Waard", "Hof van Twente", "Hollands Kroon", "Hoofddorp", "Hoogeveen",
                "Hoogvliet", "Hoorn", "Horst aan de Maas", "Houten", "Huissen", "Huizen", "Hulst", "IJsselmonde",
                "IJsselstein", "Jordaan", "Kaag en Braassem", "Kampen", "Kampen", "Katwijk", "Katwijk aan Zee", "Kerk en Zanen",
                "Kerkrade", "Koggenland", "Kralingen-Crooswijk", "Krimpen aan den IJssel", "Krimpenerwaard", "Laarbeek", "Land van Cuijk", "Landgraaf",
                "Landlust", "Lansingerland", "Leeuwarden", "Leiden", "Leiden-Noord", "Leiderdorp", "Leidschendam-Voorburg", "Lelystad",
                "Leudal", "Leusden", "Lingewaard", "Lisse", "Lochem", "Loon op Zand", "Losser", "Maasdriel",
                "Maasgouw", "Maashorst", "Maaspoort", "Maassluis", "Maastricht", "Medemblik", "Meerssen", "Meerzicht",
                "Meierijstad", "Meppel", "Midden-Delfland", "Midden-Drenthe", "Midden-Groningen", "Middenmeer", "Mijdrecht", "Moerdijk",
                "Molenlanden", "Montferland", "Museumkwartier", "Naarden", "Neder-Betuwe", "Nederweert", "Nieuw-Vennep", "Nieuw-West",
                "Nieuwe Pijp", "Nieuwegein", "Nieuwerkerk aan den IJssel wijk 04", "Nieuwkoop", "Nijkerk", "Nijkerk-stad", "Nijmegen", "Nijmegen-Midden",
                "Nijmegen-Nieuw-West", "Nijmegen-Noord", "Nijmegen-Oost", "Nijmegen-Oud-West", "Nijmegen-Zuid", "Nissewaard", "Noord", "Noord",
                "Noord woongebied", "Noorddijk e.o.", "Noordenveld", "Noordoost", "Noordoost", "Noordoostpolder", "Noordwest", "Noordwijk",
                "Noordwijk Binnen", "Nootdorp", "Nuenen, Gerwen en Nederwetten", "Nunspeet", "Oegstgeest", "Oirschot", "Oisterwijk", "Oldambt",
                "Oldebroek", "Oldenzaal", "Olst-Wijhe", "Ommen", "Ontginning", "Oost", "Oost", "Oost Gelre",
                "Oostelijk Havengebied", "Oosterheem", "Oosterhout", "Oosterparkwijk", "Ooststellingwerf", "Opsterland", "Osdorp-Oost", "Oss",
                "Oud-Beijerland", "Oud-Gestel", "Oud-Noord", "Oud-Oost", "Oud-Strijp", "Oud-West", "Oud-Zuid", "Oude IJsselstreek",
                "Oude Pijp", "Oude Stad", "Overbetuwe", "Overschie", "Papendrecht", "Peel en Maas", "Pijnacker", "Pijnacker-Nootdorp",
                "Prins Alexander", "Purmerend", "Putten", "Putten", "Raalte", "Raalte", "Reimerswaal", "Renkum",
                "Rheden", "Rhenen", "Ridderkerk", "Rijen", "Rijnsburg", "Rijssen-Holten", "Roerdalen", "Roermond",
                "Rokkeveen", "Roodenburgerdistrict", "Roosendaal", "Rotterdam", "Rotterdam Centrum", "Rucphen", "Schagen", "Scheldebuurt",
                "Schiedam", "Schijndel", "Schil rondom het centrum", "Schouwen-Duiveland", "Seghwaert", "Sint-Michielsgestel", "Sint-Oedenrode", "Sittard-Geleen",
                "Sliedrecht", "Sluis", "Smallingerland", "Soest", "Someren", "Son en Breugel", "Staatsliedenbuurt", "Stadskanaal",
                "Stadskanaal", "Stede Broec", "Steenbergen", "Steenwijk", "Steenwijkerland", "Stichtse Vecht", "Terneuzen", "Texel",
                "Teylingen", "Tholen", "Tiel", "Tiel kern", "Tilburg", "Tubbergen", "Twenterand", "Tynaarlo",
                "Tytsjerksteradiel", "Uden", "Uithoorn", "Urk", "Utrecht", "Utrechtse Heuvelrug", "Valkenburg aan de Geul", "Valkenswaard",
                "Veendam", "Veenendaal", "Veere", "Veghel", "Veldhoven", "Velsen", "Venlo", "Venray",
                "Vijfheerenlanden", "Vlaardingen", "Vlissingen", "Voorne aan Zee", "Voorschoten", "Voorst", "Vught", "Waadhoeke",
                "Waalre", "Waalwijk", "Waalwijk", "Waddinxveen", "Wageningen", "Wassenaar", "Waterland", "Weert",
                "West", "West", "West Betuwe", "West Maas en Waal", "Westerkwartier", "Westerveld", "Westerwolde", "Westland",
                "Westlandgracht", "Weststellingwerf", "Wierden", "Wijchen", "Wijdemeren", "Wijk 00", "Wijk 00", "Wijk 00",
                "Wijk 00", "Wijk 00 Bergen op Zoom-Oude stad en omgeving", "Wijk 00 Best", "Wijk 00 Binnensingelgebied", "Wijk 00 Borne", "Wijk 00 Boxtel", "Wijk 00 Centrum", "Wijk 00 Dieren",
                "Wijk 00 Epe", "Wijk 00 Harlingen", "Wijk 00 Heemstede-Centrum", "Wijk 00 IJsselstein", "Wijk 00 Kerkrade-West", "Wijk 00 Krimpen aan den IJssel", "Wijk 00 Nuenen", "Wijk 00 Nunspeet",
                "Wijk 00 Putten", "Wijk 00 Roden", "Wijk 00 Schaesberg", "Wijk 00 Stad", "Wijk 00 Urk", "Wijk 00 Valkenswaard", "Wijk 00 Veendam-kern", "Wijk 00 Veldhoven",
                "Wijk 00 Waalre", "Wijk 00 Wijk bij Duurstede", "Wijk 00 Winschoten", "Wijk 00 Zevenbergen", "Wijk 01 Drunen", "Wijk 01 Emmeloord", "Wijk 01 Goes", "Wijk 01 Heerenveen",
                "Wijk 01 Kerkrade-Oost", "Wijk 01 Maarssen", "Wijk 01 Naaldwijk", "Wijk 01 Noordoostelijk deel der gemeente", "Wijk 01 Sittard", "Wijk 01 Sneek", "Wijk 01 Twello-Nijbroek", "Wijk 01 West",
                "Wijk 01 Wijchen kern", "Wijk 01 Woerden-Midden", "Wijk 02 Bergen op Zoom-Oost", "Wijk 02 Boswinkel - Stadsveld", "Wijk 02 Buitenwijk West", "Wijk 02 Didam", "Wijk 02 Noordwest", "Wijk 02 Overhoven",
                "Wijk 02 Overwhere", "Wijk 02 Velp", "Wijk 02 Volendam", "Wijk 03 Overvecht", "Wijk 04 Benoordenhout", "Wijk 04 Buitenwijk Oost", "Wijk 04 Enschede-Noord", "Wijk 04 Noordoost",
                "Wijk 05 Geleen", "Wijk 05 Oost", "Wijk 05 Vlijmen", "Wijk 06 Binnenstad", "Wijk 06 Buitenwijk Zuidoost", "Wijk 06 Enschede-Zuid", "Wijk 06 Nieuwland", "Wijk 07 Scheveningen",
                "Wijk 07 Weidevenne", "Wijk 07 Zuid", "Wijk 08 Glanerbrug en omgeving", "Wijk 08 Zuidwest", "Wijk 09 Geuzen- en Statenkwartier", "Wijk 09 Leidsche Rijn", "Wijk 09 Sterrenburg", "Wijk 10 Binnenstad",
                "Wijk 10 Coevorden", "Wijk 10 Vleuten-De Meern", "Wijk 11 Binnenstad", "Wijk 11 Stadspolders", "Wijk 12 Bomen- en Bloemenbuurt", "Wijk 12 Maarssenbroek", "Wijk 17 Loosduinen", "Wijk 18 Waldeck",
                "Wijk 20 Valkenboskwartier", "Wijk 21 Regentessekwartier", "Wijk 22 Stadshagen", "Wijk 24 Voorhof", "Wijk 25 Buitenhof", "Wijk 25 Mariahoeve en Marlot", "Wijk 26 Bezuidenhout", "Wijk 27 Stationsbuurt",
                "Wijk 28 Centrum", "Wijk 28 Wippolder", "Wijk 29 Schildersbuurt", "Wijk 31 Rustenburg en Oostbroek", "Wijk 32 Leyenburg", "Wijk 33 Bouwlust", "Wijk 33 Kersenboogerd-Zuid", "Wijk 34 Morgenstond",
                "Wijk 36 Moerwijk", "Wijk 38 Laakkwartier en Spoorwijk", "Wijk 40 Wateringse Veld", "Wijk 42 Ypenburg", "Wijk 44 Leidschenveen", "Wijk 50 Hoogeveen", "Wijk 54 Barneveld", "Wijk bij Duurstede",
                "Winterswijk", "Woensdrecht", "Woerden", "Wormerland", "Zaanstad", "Zaltbommel", "Zandvoort", "Zeewolde",
                "Zeist", "Zeist Centrum", "Zeist-Noord", "Zevenaar", "Zevenaar", "Zoetermeer", "Zuid", "Zuid",
                "Zuid", "Zuidoost", "Zuidoost", "Zuidplas", "Zundert", "Zutphen", "Zwartewaterland", "Zwijndrecht",
                "Zwolle"
            ],
            "keywords": ["Public Surveys", "Music Festivals", "Trade Shows", "Expos", "Sporting Events", "Construction Firms", "Property Managers", "Auto Repair Shops", "Innovative Apps", "Software Developers", "Product Design Agencies"],
        },
    ]

    # Generate keyword files
    for i, config in enumerate(configs_list):
        generate_keywords(config, i)


if __name__ == "__main__":
    main()
