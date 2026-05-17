import argparse
import json
import random
from collections import Counter
from typing import Dict, List, Sequence, Tuple


State = str
Matrix = Dict[State, Dict[State, float]]


DEFAULT_MODEL = {
    "states": ["Soleado", "Nublado", "Lluvioso"],
    "transition_matrix": {
        "Soleado": {"Soleado": 0.65, "Nublado": 0.25, "Lluvioso": 0.10},
        "Nublado": {"Soleado": 0.30, "Nublado": 0.45, "Lluvioso": 0.25},
        "Lluvioso": {"Soleado": 0.20, "Nublado": 0.35, "Lluvioso": 0.45},
    },
    "initial_distribution": {"Soleado": 0.50, "Nublado": 0.30, "Lluvioso": 0.20},
}


def validate_distribution(distribution: Dict[State, float], states: Sequence[State]) -> None:
    missing = set(states) - set(distribution)
    extra = set(distribution) - set(states)
    if missing or extra:
        raise ValueError(f"La distribucion no coincide con los estados. Faltan={missing}, sobran={extra}")

    total = sum(distribution.values())
    if any(probability < 0 for probability in distribution.values()):
        raise ValueError("Las probabilidades no pueden ser negativas.")
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Las probabilidades deben sumar 1. Suma actual={total:.6f}")


def validate_transition_matrix(matrix: Matrix, states: Sequence[State]) -> None:
    if set(matrix) != set(states):
        raise ValueError("La matriz de transicion debe tener una fila por cada estado.")
    for state, row in matrix.items():
        validate_distribution(row, states)
        if not row:
            raise ValueError(f"La fila de transicion para {state} esta vacia.")


def weighted_choice(distribution: Dict[State, float], rng: random.Random) -> State:
    threshold = rng.random()
    cumulative = 0.0
    last_state = next(reversed(distribution))

    for state, probability in distribution.items():
        cumulative += probability
        if threshold <= cumulative:
            return state

    return last_state


def simulate_chain(
    states: Sequence[State],
    transition_matrix: Matrix,
    initial_distribution: Dict[State, float],
    steps: int,
    rng: random.Random,
) -> List[State]:
    validate_distribution(initial_distribution, states)
    validate_transition_matrix(transition_matrix, states)
    if steps < 0:
        raise ValueError("El numero de pasos debe ser mayor o igual a cero.")

    current_state = weighted_choice(initial_distribution, rng)
    path = [current_state]

    for _ in range(steps):
        current_state = weighted_choice(transition_matrix[current_state], rng)
        path.append(current_state)

    return path


def run_experiments(
    states: Sequence[State],
    transition_matrix: Matrix,
    initial_distribution: Dict[State, float],
    steps: int,
    simulations: int,
    seed: int | None,
) -> Tuple[List[List[State]], Dict[State, float], Dict[State, float]]:
    if simulations <= 0:
        raise ValueError("El numero de simulaciones debe ser mayor que cero.")

    rng = random.Random(seed)
    paths = [
        simulate_chain(states, transition_matrix, initial_distribution, steps, rng)
        for _ in range(simulations)
    ]

    final_counts = Counter(path[-1] for path in paths)
    final_distribution = {
        state: final_counts[state] / simulations
        for state in states
    }

    visit_counts = Counter(state for path in paths for state in path)
    total_visits = sum(visit_counts.values())
    visit_distribution = {
        state: visit_counts[state] / total_visits
        for state in states
    }

    return paths, final_distribution, visit_distribution


def stationary_distribution(
    states: Sequence[State],
    transition_matrix: Matrix,
    iterations: int = 1000,
    tolerance: float = 1e-12,
) -> Dict[State, float]:
    validate_transition_matrix(transition_matrix, states)
    distribution = {state: 1 / len(states) for state in states}

    for _ in range(iterations):
        updated = {state: 0.0 for state in states}
        for origin in states:
            for destination in states:
                updated[destination] += distribution[origin] * transition_matrix[origin][destination]

        difference = max(abs(updated[state] - distribution[state]) for state in states)
        distribution = updated
        if difference < tolerance:
            break

    return distribution


def load_model(path: str | None) -> dict:
    if path is None:
        return DEFAULT_MODEL
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def print_distribution(title: str, distribution: Dict[State, float]) -> None:
    print(title)
    for state, probability in distribution.items():
        print(f"  {state}: {probability:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulador de cadena de Markov para estados climaticos."
    )
    parser.add_argument("--model", help="Ruta a un archivo JSON con estados, matriz e inicial.")
    parser.add_argument("--steps", type=int, default=20, help="Numero de transiciones por simulacion.")
    parser.add_argument("--simulations", type=int, default=1000, help="Cantidad de simulaciones.")
    parser.add_argument("--seed", type=int, default=None, help="Semilla para reproducibilidad.")
    parser.add_argument("--show-paths", type=int, default=5, help="Cantidad de trayectorias a mostrar.")
    args = parser.parse_args()

    model = load_model(args.model)
    states = model["states"]
    transition_matrix = model["transition_matrix"]
    initial_distribution = model["initial_distribution"]

    paths, final_distribution, visit_distribution = run_experiments(
        states=states,
        transition_matrix=transition_matrix,
        initial_distribution=initial_distribution,
        steps=args.steps,
        simulations=args.simulations,
        seed=args.seed,
    )
    stationary = stationary_distribution(states, transition_matrix)

    print("Simulacion de cadena de Markov")
    print(f"Estados: {', '.join(states)}")
    print(f"Pasos por simulacion: {args.steps}")
    print(f"Cantidad de simulaciones: {args.simulations}")
    if args.seed is not None:
        print(f"Semilla: {args.seed}")

    print("\nTrayectorias de ejemplo")
    for index, path in enumerate(paths[: args.show_paths], start=1):
        print(f"  {index}. {' -> '.join(path)}")

    print()
    print_distribution("Distribucion del estado final:", final_distribution)
    print()
    print_distribution("Distribucion de visitas durante toda la simulacion:", visit_distribution)
    print()
    print_distribution("Distribucion estacionaria aproximada:", stationary)


if __name__ == "__main__":
    main()
