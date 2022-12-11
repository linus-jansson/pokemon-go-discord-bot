import requests

pokemonNames = requests.get("https://pogoapi.net/api/v1/pokemon_names.json").json()
pokemonData = requests.get("https://pogoapi.net/api/v1/pokemon_stats.json").json() 
pokemonTypes = requests.get("https://pogoapi.net/api/v1/pokemon_types.json").json()

name = "Charmander"

specificData = []

for key, value in pokemonNames.items():
    if value.get("name") == name:
        for data in pokemonData:
            if data.get("pokemon_name") == name:
                specificData.append(data)
        break

for v in specificData:
    if "Normal" in v.values():
        pokeIndex = specificData.index(v)

for v in pokemonTypes:
    if v.get("pokemon_name") == name:
        pokemonType = v.get("type")

print("Name: " + specificData[pokeIndex].get("pokemon_name"))
print("Type: " + pokemonType[-1])
print("Attack: " + str(specificData[pokeIndex].get("base_attack")))
print("Defense: " + str(specificData[pokeIndex].get("base_defense")))
print("Stamina: " + str(specificData[pokeIndex].get("base_stamina")))
