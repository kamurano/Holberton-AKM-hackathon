from model.quiz import QuizModel

class QuizRepository:
    def __init__(self):
        self.quiz_model = QuizModel()

    def get(self, quiz_id):
        quiz = self.quiz_model.get_record_by_id("quiz", quiz_id)
        if not quiz:
            return False, {"message": "Quiz not found"}
        return True, quiz

    def get_all(self):
        return self.quiz_model.get_all_records("quiz")

    def create(self, avg_score, title, questions, question_description, answers, correct_answers, stars):
        self.quiz_model.insert("quiz", avg_score, title, questions, question_description, answers, correct_answers, stars)
        return True, {"message": "Quiz created"}

    def update(self, quiz_id, avg_score, title, questions, question_description, answers, correct_answers, stars):
        quiz = self.quiz_model.get_record_by_id("quiz", quiz_id)
        if not quiz:
            return False, {"message": "Quiz not found"}
        self.quiz_model.update_record_by_id("quiz", quiz_id, avg_score, title, questions, question_description, answers, correct_answers, stars)
        return True, {"message": "Quiz updated"}

    def delete(self, quiz_id):
        quiz = self.quiz_model.get_record_by_id("quiz", quiz_id)
        if not quiz:
            return False, {"message": "Quiz not found"}
        self.quiz_model.delete_record_by_id("quiz", quiz_id)
        return True, {"message": "Quiz deleted"}