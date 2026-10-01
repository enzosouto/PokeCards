import { ref } from 'vue'
import seed from '../data/pokemon-seed.json'
import type { PokedexEntry, TypeName } from './types'

const SPRITE_BASE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon'
const EXTRA_CACHE_KEY = 'pokedex_extra_v1'
const SEED_LAST_ID = 493

function generationForNumber(n: number): number {
  if (n <= 151) return 1
  if (n <= 251) return 2
  if (n <= 386) return 3
  if (n <= 493) return 4
  if (n <= 649) return 5
  if (n <= 721) return 6
  if (n <= 809) return 7
  if (n <= 905) return 8
  return 9
}

interface SeedPokemon {
  id: number
  name: string
  generation: number
  spriteUrl: string
}

interface SeedTypeLink {
  pokemonId: number
  typeId: number
  slot: number
}

interface SeedType {
  id: number
  name: TypeName
}

interface SeedData {
  pokemon: SeedPokemon[]
  types: SeedType[]
  pokemonTypes: SeedTypeLink[]
}

function buildSeedEntries(): PokedexEntry[] {
  const data = seed as unknown as SeedData
  const typeById = new Map(data.types.map((t) => [t.id, t.name]))
  const typesByPokemonId = new Map<number, TypeName[]>()
  for (const link of data.pokemonTypes) {
    const name = typeById.get(link.typeId)
    if (!name) continue
    const list = typesByPokemonId.get(link.pokemonId) ?? []
    list[link.slot - 1] = name
    typesByPokemonId.set(link.pokemonId, list)
  }
  return data.pokemon.map((p) => ({
    id: p.id,
    name: p.name,
    spriteUrl: p.spriteUrl || `${SPRITE_BASE}/${p.id}.png`,
    generation: p.generation,
    types: (typesByPokemonId.get(p.id) ?? []).filter(Boolean),
  }))
}

async function fetchExtraGenerations(): Promise<PokedexEntry[]> {
  const cached = localStorage.getItem(EXTRA_CACHE_KEY)
  if (cached) {
    try {
      return JSON.parse(cached)
    } catch {
      // corrupt cache — refetch below
    }
  }
  try {
    const res = await fetch(`https://pokeapi.co/api/v2/pokemon?limit=2000&offset=${SEED_LAST_ID}`)
    if (!res.ok) return []
    const data = (await res.json()) as { results: Array<{ name: string; url: string }> }
    const extra: PokedexEntry[] = data.results
      .map((r) => {
        const id = Number(r.url.split('/').filter(Boolean).pop())
        return {
          id,
          name: r.name,
          spriteUrl: `${SPRITE_BASE}/${id}.png`,
          generation: generationForNumber(id),
          types: [] as TypeName[],
        }
      })
      .filter((p) => p.id > SEED_LAST_ID && p.id < 10000)
      .sort((a, b) => a.id - b.id)
    localStorage.setItem(EXTRA_CACHE_KEY, JSON.stringify(extra))
    return extra
  } catch {
    return []
  }
}

export const pokedexList = ref<PokedexEntry[]>(buildSeedEntries())
export const pokedexLoading = ref(false)
let extended = false

/** Gen I-IV loads instantly from the baked seed; this tops it up with every
 * later generation PokéAPI knows about, fetched once and cached. */
export async function ensureFullPokedex(): Promise<void> {
  if (extended) return
  extended = true
  pokedexLoading.value = true
  const extra = await fetchExtraGenerations()
  if (extra.length) pokedexList.value = [...pokedexList.value, ...extra]
  pokedexLoading.value = false
}

export function findPokemon(id: number): PokedexEntry | undefined {
  return pokedexList.value.find((p) => p.id === id)
}
