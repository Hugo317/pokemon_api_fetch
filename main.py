import requests
import json
import csv
import time

base_url = "https://pokeapi.co/api/v2/"


def build_all_csv(base_url):

    pokemon_list = []
    poke_type_list = []
    poke_region_list = []
    poke_move_list = []

    def get_poke_list(base_url):

        return requests.get(f"{base_url}pokemon?limit=100000&offset=0").json()["results"]

    def is_baby_myth_or_leg(species_url):
        response = requests.get(species_url).json()
        is_baby = response["is_baby"]
        is_mythical = response["is_mythical"]
        is_legendary = response["is_legendary"]
        return [is_baby,is_mythical,is_legendary]

    def clean_pokemon(pokemon):
        pokemon.pop("past_abilities",None)
        pokemon.pop("past_types",None)
        pokemon.pop("past_stats",None)
        pokemon.pop("held_items")
        pokemon.pop("cries")
        pokemon.pop("sprites")
        pokemon.pop("abilities")
        pokemon.pop("game_indices")
        pokemon.pop("order")
        pokemon.pop("forms")
        pokemon.pop("is_default")

        pokemon["moves"] = [(move["move"]["name"],move["move"]["url"].rstrip("/").split("/")[-1])
                            for move in pokemon["moves"]]
        return pokemon       

    def get_poke_json(base_url, nr):
        r = requests.get(f"{base_url}pokemon/{nr}")
        if r.status_code != 200:
            print(f"pokemon {nr} failed: {r.status_code}")
        pokemon = r.json()
        return pokemon

    def unpack_stats(pokemon):
        pokemon.update({stat["stat"]["name"]: stat["base_stat"] for stat in pokemon["stats"]})
        pokemon.pop("stats")
        return pokemon



    for entry in get_poke_list(base_url):
        poke_id = entry["url"].rstrip("/").split("/")[-1]
        time.sleep(0.2)
        pokemon = unpack_stats((clean_pokemon(get_poke_json(base_url,poke_id))))     

        is_baby,is_mythical,is_legendary = is_baby_myth_or_leg(pokemon["species"]["url"])

        pokemon.pop("species")

        poke_types = [{"pokemon_id": pokemon["id"],
                        "type_id": tp["type"]["url"].rstrip("/").split("/")[-1],
                        "pokemon_name": pokemon["name"],
                        "type_name": tp["type"]["name"]} for tp in pokemon.pop("types")]

        pokemon.update({"is_baby":is_baby,
                        "is_mythical":is_mythical,
                        "is_legendary":is_legendary})

        moves = [{"pokemon_id": pokemon["id"],
                "move_id": move_id,
                "pokemon_name": pokemon["name"],
                "move_name": move_name} for move_name,move_id in pokemon.pop("moves")]


        regions = [{"pokemon_id": pokemon["id"],
                "region_id": version_id,
                "pokemon_name": pokemon["name"],
                "region_name": version_name}
                for version_name, version_id in
                {(v["version"]["name"], v["version"]["url"].rstrip("/").split("/")[-1])
                 for entry in requests.get(pokemon.pop("location_area_encounters")).json()
                 for v in entry["version_details"]}]

        
        poke_move_list.extend(moves)
        poke_region_list.extend(regions)
        poke_type_list.extend(poke_types)
        pokemon_list.append(pokemon)
        print(f"{poke_id}")

    with open("pokemon.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=pokemon_list[0].keys())
        writer.writeheader()
        writer.writerows(pokemon_list)

    with open("types.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=poke_type_list[0].keys())
        writer.writeheader()
        writer.writerows(poke_type_list)

    with open("moves.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=poke_move_list[0].keys())
        writer.writeheader()
        writer.writerows(poke_move_list)

    with open("regions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=poke_region_list[0].keys())
        writer.writeheader()
        writer.writerows(poke_region_list)

        





build_all_csv(base_url)


