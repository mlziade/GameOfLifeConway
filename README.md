# Conway's Game of life

# Description

A python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life).

# Implementation

After many iterations, I arrived at an implementation using sets to store alive cells by their coordinates. That way, I don't need to store neither empty cells (like my previous array implementation) or cell's values (like my previous dictionary/hashmap implementation).

To check the state of the cells, I took a "neighbors" approach, where I only check alive cells and their eight neighbors. I previously tried a "bounding box" approach (which was cool to use a bit of math and algebra), but it was not as optimized or necessary if i took the neighbors approach.

# Context
I had the idea of building this back in 2023 when I saw Veritasium's video ["Math's Fundamental Flaw"](https://youtu.be/HeQX2HjkcNo?si=89_5bHk-IF4SBUYd&t=65). It became something of a never-ending project that I would occasionally revisit every few months.

It's cool to see how much my idea of what constitutes a well-structured program has evolved over those three years. It's also cool to see how much I've improved as a developer and how I can now visualize easier/faster implementations without thinking for a long time.

I'm just really happy that I finally got to finish this, but I also wonder if I can improve it with multithreading and use a different compiler, like I previously did with PyPy.
# Rules

## Board

An infinite grid filled with 1's and 0's.

## Rules
For each populated space:

- Each cell with less than 2 live neighbors dies
- Each cell with more than 3 neighbors dies
- Each cell with 2 or 3 neighbors lives

For each empty space:

- Each cell with exactly three neighbors lives

# Journal
Little messages that i for some reason wrote back then hahaha.

- Tanto faz, eu tô chapado e vi esse vídeo "Math's Fundamental Flaw" https://youtu.be/HeQX2HjkcNo?si=89_5bHk-IF4SBUYd&t=65

- 26/06 00:06 Depois de entrar num sprint the código em 2025m resolvi tentar oneshot esse código em uma noite. Vamos ver.

- 26/06 01:50 Ok, não consegui matar tudo em 1 noite, mas esse método parece promissor. Escalável, economico com memoria e "rápido".

- 29/03 16:54 Finalmente terminei 😊

