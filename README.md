# Conway's Game of life

# Description

A python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life).

# Implementation

After many iterations, I arrived at an implementation using sets to store alive cells by their coordinates. That way, I don't need to store neither empty cells (like my previous array implementation) or cell's values (like my previous dictionary/hashmap implementation).

To check the state of the cells, I took a "neighbors" approach, where I only check alive cells and their eight neighbors. I previously tried a "bounding box" approach (which was cool to use a bit of math and algebra), but it was not as optimized or necessary if i took the neighbors approach.

## Features

- **Async implementation with asyncio**: Uses asynchronous programming to handle cell state calculations in parallel for improved performance
- **Pattern selection**: Load different initial patterns from a JSON file (patterns p1-p12 available)
- **Game log generation**: Optional logging of game statistics including timing data, rounds played, and pattern information
- **Configurable max rounds**: Set a maximum number of rounds to prevent infinite games

# Rules

## Board

The game takes place on an infinite two-dimensional grid where each cell is either alive (`1`) or dead (`0`).

## Game Rules

For every generation, the following rules are applied:

- **Survival:** A living cell with 2 or 3 living neighbors remains alive.
- **Death by underpopulation:** A living cell with fewer than 2 living neighbors dies.
- **Death by overpopulation:** A living cell with more than 3 living neighbors dies.
- **Birth:** A dead cell with exactly 3 living neighbors becomes alive.

# Context
I had the idea of building this back in 2023 when I saw Veritasium's video ["Math's Fundamental Flaw"](https://youtu.be/HeQX2HjkcNo?si=89_5bHk-IF4SBUYd&t=65). It became something of a never-ending project that I would occasionally revisit every few months.

It's cool to see how much my idea of what constitutes a well-structured program has evolved over those three years. It's also cool to see how much I've improved as a developer and how I can now visualize easier/faster implementations without thinking for a long time.

I'm just really happy that I finally got to finish this, but I also wonder if I can improve it with multithreading and use a different compiler, like I previously did with PyPy.

# Usage

Run the game with:
```bash
python main.py [--pattern PATTERN] [--logs true/false] [--rounds NUMBER]
```

Options:
- `--pattern`: Choose initial pattern (p1-p12, default: p3)
- `--logs`: Enable game log saving (default: false)
- `--rounds`: Set maximum number of rounds (default: unlimited)

# Journal
Little messages that i for some reason wrote back then hahaha.

- Tanto faz, eu tô chapado e vi esse vídeo "Math's Fundamental Flaw" https://youtu.be/HeQX2HjkcNo?si=89_5bHk-IF4SBUYd&t=65

- 26/06 00:06 Depois de entrar num sprint the código em 2025m resolvi tentar oneshot esse código em uma noite. Vamos ver.

- 26/06 01:50 Ok, não consegui matar tudo em 1 noite, mas esse método parece promissor. Escalável, economico com memoria e "rápido".

- 29/03 16:54 Finalmente terminei 😊

- 20/07: Voltei no código depois de repensar um pouco nas minhas prtáticas de analise de algoritmo após notar como o tempo de execução pode crescer rapidamente. Ainda precisa pensar em algo para optimizar. Talvez focar em casos específicos como o shooter, e entender que os tiros se movem de maneira previsivel no grid. Talvez essa seja uma questão do prório vídeo de projetos P x NP.
