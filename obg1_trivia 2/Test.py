import unittest
from unittest.mock import patch
from obg1_prog_avz import (
    load_questions,
    select_random_questions,
    generate_options,
    calculate_score,
    play_game,
    decorated_function,
    partial_calculate_score,
    calculate_total_score,
    double_scores
)

class TestTriviaGame(unittest.TestCase):

    def test_load_questions(self):
        """Prueba que las preguntas se carguen correctamente desde el archivo CSV."""
        questions = load_questions('JEOPARDY_CSV.csv')
        self.assertGreaterEqual(len(questions), 5)  # Suponiendo que el archivo tiene al menos 5 preguntas

    def test_generate_options(self):
        """Prueba la generación de opciones, asegurando que incluye la respuesta correcta."""
        correct_answer = "Correcta"
        all_answers = ["Correcta", "Incorrecta 1", "Incorrecta 2", "Incorrecta 3"]
        options = generate_options(correct_answer, all_answers)
        self.assertEqual(len(options), 3)
        self.assertIn(correct_answer, options)

    def test_select_random_questions(self):
        """Prueba la selección aleatoria de preguntas."""
        questions = [("Question1", "Answer1"), ("Question2", "Answer2"), ("Question3", "Answer3")]
        selected_questions = select_random_questions(questions, 2)
        self.assertEqual(len(selected_questions), 2)

    def test_select_random_questions_less_than_count(self):
        """Prueba que se maneje correctamente el caso donde hay menos preguntas que el número solicitado."""
        questions = [("Question1", "Answer1")]
        selected_questions = select_random_questions(questions, 5)
        self.assertEqual(len(selected_questions), 1)

    def test_calculate_score(self):
        """Prueba el cálculo de puntaje."""
        score = calculate_score(3)
        self.assertEqual(score, 30)

    def mock_input(prompt):
        return '3'  # Simulamos que el usuario siempre elige la tercera opción, que es la correcta.

    @patch('builtins.input', mock_input)  # Reemplaza input() con mock_input durante la prueba
    def test_play_game_with_correct_answers(self):
        """Prueba el juego con respuestas correctas."""
        questions = [("Question1", ["Option1", "Option2", "Answer1"], "Answer1")]
        score = play_game(questions)
        self.assertEqual(score, 10)

    def mock_input_incorrect(prompt):
        return '1'  # Simulamos que el usuario siempre elige la primera opción, que es incorrecta.

    @patch('builtins.input', mock_input_incorrect)  # Reemplaza input() con mock_input_incorrect durante la prueba
    def test_play_game_with_incorrect_answers(self):
        """Prueba el juego con respuestas incorrectas."""
        questions = [("Question1", ["Option1", "Option2", "Answer1"], "Answer1")]
        score = play_game(questions, score=0)
        self.assertEqual(score, 0)

    def test_play_game_no_questions(self):
        """Prueba el caso donde no hay preguntas."""
        questions = []
        score = play_game(questions)
        self.assertEqual(score, 0)

    def test_decorated_function(self):
        """Prueba que el decorador funcione correctamente."""
        @decorated_function
        def dummy_function():
            return True
        result = dummy_function()
        self.assertTrue(result)

    def test_generate_options_no_correct_answer(self):
        """Prueba que se maneje correctamente el caso donde no hay respuestas correctas en all_answers."""
        correct_answer = "Correcta"
        all_answers = ["Incorrecta 1", "Incorrecta 2", "Incorrecta 3"]
        options = generate_options(correct_answer, all_answers)
        self.assertEqual(len(options), 3)
        self.assertIn(correct_answer, options)
    
    def test_generate_options_single_answer(self):
        """Prueba la generación de opciones con solo una respuesta disponible."""
        correct_answer = "Correcta"
        all_answers = ["Correcta"]
        options = generate_options(correct_answer, all_answers)
        self.assertEqual(len(options), 1)
        self.assertIn(correct_answer, options)

    def test_partial_calculate_score(self):
        """Prueba el uso de partial en calculate_score."""
        score = partial_calculate_score(3)
        self.assertEqual(score, 45)

    def test_calculate_total_score(self):
        """Prueba el uso de reduce para calcular el puntaje total."""
        scores = [10, 20, 30]
        total_score = calculate_total_score(scores)
        self.assertEqual(total_score, 60)

    def test_double_scores(self):
        """Prueba el uso de map para duplicar los puntajes."""
        scores = [10, 20, 30]
        doubled = double_scores(scores)
        self.assertEqual(doubled, [20, 40, 60])


if __name__ == "__main__":
    unittest.main()
