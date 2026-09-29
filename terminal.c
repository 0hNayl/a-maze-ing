import curses

OPTIONS: list[str] = [
    "Régénérer un nouveau labyrinthe",
    "Afficher ou masquer le chemin",
    "Changer la couleur des murs",
    "Choisir la couleur du 42",
    "Quitter",
]

TOUCHES_ENTREE: tuple[int, ...] = (curses.KEY_ENTER, 10, 13)


def afficher(
    stdscr: curses.window,
    ligne: int,
    colonne: int,
    texte: str,
    attr: int = 0,
) -> None:
    hauteur, largeur = stdscr.getmaxyx()

    if ligne < hauteur and colonne < largeur:
        stdscr.addstr(ligne, colonne, texte[:largeur - colonne - 1], attr)


def dessiner_menu(stdscr: curses.window, selection: int) -> None:
    stdscr.erase()
    afficher(stdscr, 0, 0, "=== Menu ===", curses.A_BOLD)
    afficher(
        stdscr, 1, 0,
        f"↑/↓ pour naviguer, Entrée pour valider, "
        f"1-{len(OPTIONS)} accès direct",
    )
    for i, option in enumerate(OPTIONS):
        numero = f"{i + 1}. {option}"
        if i == selection:
            afficher(stdscr, i + 3, 2, f"> {numero}", curses.A_REVERSE)
        else:
            afficher(stdscr, i + 3, 2, f"  {numero}")
    stdscr.refresh()


def executer(stdscr: curses.window, option: str) -> None:
    stdscr.erase()
    afficher(stdscr, 0, 0, f"Tu as choisi : {option}", curses.A_BOLD)
    afficher(stdscr, 2, 0, "Appuie sur une touche pour revenir au menu...")
    stdscr.refresh()

    stdscr.getch()


def menu(stdscr: curses.window) -> None:
    curses.curs_set(0)
    curses.use_default_colors()  
    stdscr.keypad(True)

    selection = 0

    while True:
        dessiner_menu(stdscr, selection)
        touche = stdscr.getch()
        if touche == curses.KEY_UP:
            selection = (selection - 1) % len(OPTIONS)
        elif touche == curses.KEY_DOWN:
            selection = (selection + 1) % len(OPTIONS)
        elif ord("1") <= touche <= ord("0") + len(OPTIONS):
            selection = touche - ord("1")

        elif touche in TOUCHES_ENTREE:
            option = OPTIONS[selection]
            if option == "Quitter":
                break  
            executer(stdscr, option)

        elif touche == curses.KEY_RESIZE:
            pass


def main() -> None:
    try:
        curses.wrapper(menu)
    except KeyboardInterrupt:
        pass
    print("Au revoir !")


if __name__ == "__main__":
    main()