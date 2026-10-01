# pokemon_api_fetch

Scripts and notebooks that pull Pokémon data from the public [PokeAPI](https://pokeapi.co/)
and assemble it into CSVs for analysis.

## Output

| File | Contents |
|---|---|
| `pokemon.csv` / `pokemon.json` | Per-Pokémon stats, types and metadata |
| `moves.csv` | Moves and their attributes |
| `types.csv` | Type data |
| `regions.csv` | Region data |

## Usage

`main.py` and `fetch_api.ipynb` fetch from PokeAPI and write the CSVs above.
The data feeds the analysis in
[`pokemon_data_analysis`](https://github.com/Hugo317/pokemon_data_analysis).
