from typing import List, Tuple, Callable, Optional, Union
import csv
import random
from itertools import chain
from functools import reduce, partial, lru_cache, wraps

# 1. Recursión (utilizada en la función play_game)
# 2. Generadores (utilizados en question_generator)
# 3. Listas por Comprensión (utilizadas en varias partes del código)
# 4. Decoradores (utilizados en start_game y otros)
# 5. itertools.chain (utilizado en generate_options)
# 6. Mónadas (aproximación usando Optional para representar valores que pueden estar ausentes)
# 7. Funciones lambda (utilizadas en generate_options y filter)
# 8. Map, Filter, Reduce (utilizados en varias partes del código)
# 9. Partial, LRU_cache (utilizados en load_questions y otros)

def bind_optional(value: Optional[Union[str, int]], func: Callable[[Union[str, int]], Optional[Union[str, int]]]) -> Optional[Union[str, int]]:
    """
    Aplica una función a un valor opcional (mónada). Si el valor es None, retorna None.

    :param value: Valor opcional (puede ser None).
    :param func: Función a aplicar al valor.
    :return: El resultado de aplicar la función al valor, o None si el valor es None.
    """
    return func(value) if value is not None else None

@lru_cache(maxsize=32)
def load_questions(file_path: str) -> List[Tuple[str, str]]:
    """
    Cargar preguntas de trivia desde un archivo CSV.

    :param file_path: La ruta al archivo CSV.
    :return: Una lista de tuplas, cada una contiene una pregunta y la respuesta correcta.
    """
    with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        questions = [(row['Question'], row['Answer']) for row in reader]

    print(f"Se cargaron {len(questions)} preguntas.")
    return questions

def generate_options(correct_answer: str, all_answers: List[str]) -> List[str]:
    """
    Generar una lista de opciones que incluye la respuesta correcta y respuestas incorrectas seleccionadas al azar.

    :param correct_answer: La respuesta correcta.
    :param all_answers: Lista de todas las posibles respuestas.
    :return: Una lista de opciones que incluye la respuesta correcta.
    """
    wrong_answers = list(filter(lambda x: x != correct_answer, all_answers))
    wrong_answers = random.sample(wrong_answers, 2)  # Seleccionar 2 respuestas incorrectas
    options = list(chain(wrong_answers, [correct_answer]))
    random.shuffle(options)
    return options

def select_random_questions(questions: List[Tuple[str, str]], count: int = 5) -> List[Tuple[str, List[str], str]]:
    """
    Seleccionar un subconjunto aleatorio de preguntas de la lista.

    :param questions: La lista de todas las preguntas.
    :param count: El número de preguntas a seleccionar.
    :return: Una muestra aleatoria de preguntas con opciones generadas.
    """
    if len(questions) < count:
        print(f"Solo hay {len(questions)} preguntas disponibles. Reduciendo el tamaño de la muestra para coincidir.")
        count = len(questions)

    selected_questions = random.sample(questions, count)
    all_answers = [q[1] for q in questions]  # Obtener todas las posibles respuestas
    questions_with_options = [(q[0], generate_options(q[1], all_answers), q[1]) for q in selected_questions]
    
    return questions_with_options

def ask_question(question: Tuple[str, List[str], str]) -> bool:
    """
    Presentar una pregunta al usuario y verificar si la respuesta es correcta.

    :param question: Una tupla que contiene la pregunta, una lista de opciones y la respuesta correcta.
    :return: True si la respuesta del usuario es correcta, False en caso contrario.
    """
    print(question[0])
    for i, option in enumerate(question[1]):
        print(f"{i + 1}. {option}")
    
    while True:
        try:
            answer = input("Seleccione la opción correcta (1-3): ")
            if answer not in ['1', '2', '3']:
                raise ValueError("Por favor, ingrese un número entre 1 y 3.")
            return question[1][int(answer) - 1] == question[2]
        except ValueError as e:
            print(e)

def calculate_score(correct_answers: int, points_per_question: int = 10) -> int:
    """
    Calcular el puntaje total basado en el número de respuestas correctas.

    :param correct_answers: El número de respuestas correctas.
    :param points_per_question: Los puntos otorgados por cada respuesta correcta.
    :return: El puntaje total.
    """
    return correct_answers * points_per_question

def question_generator(questions: List[Tuple[str, List[str], str]]) -> Callable[[], Optional[Tuple[str, List[str], str]]]:
    """
    Generador que produce preguntas una por una.

    :param questions: La lista de preguntas.
    :return: Un generador que produce preguntas.
    """
    def gen():
        for question in questions:
            yield question
    return gen

def play_game(questions: List[Tuple[str, List[str], str]], score: int = 0) -> int:
    """
    Jugar el juego de trivia iterando a través de las preguntas seleccionadas.

    :param questions: La lista de preguntas a preguntar.
    :param score: El puntaje actual.
    :return: El puntaje final después de responder todas las preguntas.
    """
    if not questions:
        return score

    generator = question_generator(questions)()
    question = bind_optional(next(generator, None), lambda q: q)

    if question is not None:
        correct = ask_question(question)
        if correct:
            score += 10
        return play_game(questions[1:], score)

    return score

def decorated_function(func: Callable) -> Callable:
    """
    Decorador para anunciar el inicio y el fin de una función.

    :param func: La función a decorar.
    :return: La función envuelta.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Inicio de la función")
        result = func(*args, **kwargs)
        print("Fin de la función")
        return result
    return wrapper

@decorated_function
def start_game():
    """
    Iniciar el juego de trivia cargando preguntas y jugando a través de ellas.

    Esta función es el punto de entrada principal para el juego.
    """
    questions = load_questions('JEOPARDY_CSV.csv')
    selected_questions = select_random_questions(questions)
    final_score = play_game(selected_questions)
    print(f"Tu puntaje final es: {final_score}")

# Ejemplo de uso de partial para crear una función especializada
partial_calculate_score = partial(calculate_score, points_per_question=15)

def calculate_total_score(scores: List[int]) -> int:
    """
    Calcular el puntaje total acumulando puntajes individuales usando reduce.

    :param scores: Una lista de puntajes individuales.
    :return: El puntaje total acumulado.
    """
    return reduce(lambda x, y: x + y, scores)

# Ejemplo de uso de map para duplicar los puntajes
def double_scores(scores: List[int]) -> List[int]:
    """
    Duplica cada puntaje en una lista de puntajes usando map.

    :param scores: Una lista de puntajes individuales.
    :return: Una nueva lista de puntajes donde cada uno ha sido duplicado.
    """
    return list(map(lambda x: x * 2, scores))

if __name__ == "__main__":
    start_game()











