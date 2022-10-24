interface Player {
    name: string
    alias: string
    image: string
    level: number
    rank: {
        rank_n: number
        rank_p: number
        solo: {
            rank: string
            image: string
            lp: number
            win: number
            lose: number
            winrate: number
        }
        flex: {
            rank: string
            image: string
            lp: number
            win: number
            lose: number
            winrate: number
        }
    }
    champs: Champ[]
	masteries: Mastery[]
}

interface Champ {
    name: string
    image: string
    games: number
    winrate: number
    kda: number
    kills: number
    deaths: number
    assists: number
    cs: number
    csmin: number
    gold: number
    max_kills: number
    max_deaths: number
    avg_damage_dealt: number
    avg_damage_taken: number
    double_kills: number
    triple_kills: number
    quadra_kills: number
    penta_kills: number
}

interface Mastery {
	name: string
	image: string
	level: number
	points: number
}