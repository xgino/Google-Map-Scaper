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
    configs_list = [
        {
            "countries": ["Nederland"],
            "places": [
                "Nijmegen", "Nijmegen-Midden", "Nijmegen-Nieuw-West", "Nijmegen-Noord", "Nijmegen-Oost", "Nijmegen-Oud-West", "Nijmegen-Zuid"
            ],
            "keywords": ["Dental Offices", "Auto Repair Shops"],
        },
        {
            "countries": ["Nederland"],
            "places": [
                "Nijmegen", "Nijmegen-Midden", "Nijmegen-Nieuw-West", "Nijmegen-Noord", "Nijmegen-Oost", "Nijmegen-Oud-West", "Nijmegen-Zuid"
            ],
            "keywords": ["Universities", "Hotels"],
        },
        {
            "countries": ["Nederland"],
            "places": [
                "Nijmegen", "Nijmegen-Midden", "Nijmegen-Nieuw-West", "Nijmegen-Noord", "Nijmegen-Oost", "Nijmegen-Oud-West", "Nijmegen-Zuid"
            ],
            "keywords": ["Logistics Companies", "Car Dealerships"],
        },
        {
            "countries": ["Nederland"],
            "places": [
                "Nijmegen", "Nijmegen-Midden", "Nijmegen-Nieuw-West", "Nijmegen-Noord", "Nijmegen-Oost", "Nijmegen-Oud-West", "Nijmegen-Zuid"
            ],
            "keywords": ["Music Festivals", "Sporting Events"],
        },
    ]

    # Generate keyword files
    for i, config in enumerate(configs_list):
        generate_keywords(config, i)


if __name__ == "__main__":
    main()
