"""
main.py

Command-line interface for generalized_pipe_dreams.py.
"""

from pathlib import Path
import generalized_pipe_dreams as gpd


def ask_for_permutation() -> list[int]:
    """
    Keep asking until the user enters a valid permutation.
    """
    while True:
        text = input("Enter a permutation, such as 31254 or 3 1 2 5 4: ")

        try:
            w = gpd.parse_permutation(text)
            gpd.validate_permutation(w)
            return w

        except ValueError as exc:
            print(f"Invalid permutation: {exc}")
            print()


def ask_for_display_mode() -> str:
    """
    Ask the user which kind of pipe dreams they want to see.
    """
    print()
    print("What do you want to display?")
    print("1. Reduced pipe dreams only")
    print("2. Non-reduced pipe dreams only")
    print("3. All generalized pipe dreams, separated into reduced and non-reduced")
    print("4. Counts only")

    while True:
        choice = input("Choose 1, 2, 3, or 4: ").strip()

        if choice in {"1", "2", "3", "4"}:
            return choice

        print("Please enter 1, 2, 3, or 4.")


def ask_for_output_mode() -> str:
    """
    Ask whether to print, save to a file, or both.
    """
    print()
    print("How do you want the output?")
    print("1. Print to terminal only")
    print("2. Save to .txt file only")
    print("3. Print and save to .txt file")

    while True:
        choice = input("Choose 1, 2, or 3: ").strip()

        if choice in {"1", "2", "3"}:
            return choice

        print("Please enter 1, 2, or 3.")


def ask_for_generation_method(n: int) -> str:
    """
    Ask whether to use move-based generation or brute force.
    """
    print()
    print("How do you want to generate the pipe dreams?")
    print("1. Use generalized chute moves and double-cross flips")
    print("2. Use brute force over every subset of the staircase")

    if n <= 6:
        print("   Brute force is reasonable for this size.")
    else:
        print("   Warning: brute force may be very slow for this size.")

    while True:
        choice = input("Choose 1 or 2: ").strip()

        if choice in {"1", "2"}:
            return choice

        print("Please enter 1 or 2.")


def ask_for_filename(w: list[int]) -> str:
    """
    Ask the user for a .txt filename.

    If the user presses Enter, use a default filename based on the permutation.
    """
    default_name = "pipe_dreams_" + "".join(str(x) for x in w) + ".txt"

    text = input(f"Enter output filename, or press Enter for {default_name}: ").strip()

    if text == "":
        text = default_name

    if not text.endswith(".txt"):
        text += ".txt"

    return text


def generate_pipe_dreams(w: list[int], method: str):
    """
    Generate generalized pipe dreams using the chosen method.
    """
    if method == "1":
        return gpd.all_generalized_pipe_dreams_by_moves(w)

    if method == "2":
        return gpd.all_pipe_dreams_by_filter(w)

    raise ValueError("Unknown generation method.")


def pipe_dream_details(D, n: int) -> str:
    """
    Return the text representation of one pipe dream.
    """
    lines = []

    lines.append(gpd.pipe_dream_to_string(D, n))
    lines.append(f"word: {gpd.reading_word(D, n)}")
    lines.append(f"ordinary permutation: {gpd.pipe_permutation(D, n)}")
    lines.append(f"crosses: {len(D)}")
    lines.append(f"reduced: {gpd.is_reduced_pipe_dream(D, n)}")
    lines.append(f"monomial exponents: {gpd.monomial_exponents(D, n)}")

    return "\n".join(lines)


def render_group(title: str, dreams, n: int) -> str:
    """
    Return a labeled group of pipe dreams as one big string.
    """
    lines = []

    lines.append("")
    lines.append(title)
    lines.append("=" * len(title))
    lines.append(f"Count: {len(dreams)}")

    for i, D in enumerate(dreams, start=1):
        lines.append("")
        lines.append(f"{title} #{i}")
        lines.append("-" * 40)
        lines.append(pipe_dream_details(D, n))

    return "\n".join(lines)


def render_results(w: list[int], dreams, mode: str) -> str:
    """
    Build the full output as a string.

    This makes it easy to either print the output or save it to a file.
    """
    n = len(w)

    reduced = [
        D for D in dreams
        if gpd.is_reduced_pipe_dream(D, n)
    ]

    non_reduced = [
        D for D in dreams
        if not gpd.is_reduced_pipe_dream(D, n)
    ]

    lines = []

    lines.append("=" * 60)
    lines.append(f"Permutation: {w}")
    lines.append(f"Total generalized pipe dreams found: {len(dreams)}")
    lines.append(f"Reduced pipe dreams: {len(reduced)}")
    lines.append(f"Non-reduced pipe dreams: {len(non_reduced)}")
    lines.append("=" * 60)

    if mode == "1":
        lines.append(render_group("Reduced pipe dreams", reduced, n))

    elif mode == "2":
        lines.append(render_group("Non-reduced pipe dreams", non_reduced, n))

    elif mode == "3":
        lines.append(render_group("Reduced pipe dreams", reduced, n))
        lines.append(render_group("Non-reduced pipe dreams", non_reduced, n))

    elif mode == "4":
        pass

    else:
        raise ValueError("Unknown display mode.")

    return "\n".join(lines)


def save_output_to_txt(output: str, filename: str) -> None:
    """
    Save the output string to a .txt file.
    """
    path = Path(filename)
    path.write_text(output, encoding="utf-8")
    print(f"Saved output to: {path.resolve()}")


def main() -> None:
    print("Pipe Dream Generator")
    print("=" * 60)
    print()

    while True:
        w = ask_for_permutation()
        n = len(w)

        mode = ask_for_display_mode()
        method = ask_for_generation_method(n)
        output_mode = ask_for_output_mode()

        dreams = generate_pipe_dreams(w, method)
        dreams = gpd.sorted_pipe_dreams(dreams)

        output = render_results(w, dreams, mode)

        if output_mode in {"1", "3"}:
            print()
            print(output)

        if output_mode in {"2", "3"}:
            print()
            filename = ask_for_filename(w)
            save_output_to_txt(output, filename)

        print()
        again = input("Run another permutation? (y/n): ").strip().lower()

        if again not in {"y", "yes"}:
            print("Goodbye.")
            break

        print()


if __name__ == "__main__":
    main()