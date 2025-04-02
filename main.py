import random
import tkinter as tk
from tkinter import messagebox, ttk


def load_questions(filename):
    questions = []
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n\n')
        for block in content:
            lines = block.strip().split('\n')
            question = lines[0]
            answers = lines[1:-1]
            correct_answer = lines[-1].strip()
            correct_answer_full = next(ans for ans in answers if ans.startswith(correct_answer))
            questions.append((question, answers, correct_answer, correct_answer_full))
    return questions


def start_exam(mode):
    global selected_questions, question_index, score, user_answers
    selected_questions = random.sample(questions, num_questions)
    question_index = 0
    score = 0
    user_answers = []
    show_question(mode)


def show_question(mode):
    global question_label, answer_buttons
    if question_index < len(selected_questions):
        question, answers, correct_answer, _ = selected_questions[question_index]
        question_label.config(text=question)

        for i in range(len(answer_buttons)):
            if i < len(answers):
                answer_buttons[i].config(
                    text=answers[i],
                    state=tk.NORMAL,
                    command=lambda ans=answers[i]: check_answer(ans, correct_answer, mode)
                )
            else:
                answer_buttons[i].config(text="", state=tk.DISABLED)
    else:
        finish_exam()


def check_answer(user_answer, correct_answer, mode):
    global question_index, score, user_answers
    _, _, _, correct_answer_full = selected_questions[question_index]
    is_correct = user_answer[0] == correct_answer
    user_answers.append(
        (selected_questions[question_index][0], user_answer, correct_answer_full, "✅" if is_correct else "❌"))

    if mode == "practice":
        if is_correct:
            messagebox.showinfo("Wynik", "✅ Poprawna odpowiedź!")
        else:
            messagebox.showerror("Wynik", f"❌ Błędna odpowiedź! Poprawna to: {correct_answer_full}")
    else:
        if is_correct:
            score += 1

    question_index += 1
    show_question(mode)


def finish_exam():
    update_previous_exam_tab()
    messagebox.showinfo("Koniec egzaminu",
                        f"Twój wynik: {score}/{num_questions} ({(score / num_questions) * 100:.2f}%)")


def update_previous_exam_tab():
    for row in tree.get_children():
        tree.delete(row)
    for question, user_ans, correct_ans, result in user_answers:
        tree.insert("", "end", values=(question, user_ans, correct_ans, result))


def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        set_dark_mode()
    else:
        set_light_mode()


def set_dark_mode():
    global dark_mode
    # Ustawienie tła na ciemny motyw
    root.config(bg="#333333")  # Tło całej aplikacji
    question_label.config(bg="#333333", fg="white")  # Etykieta pytania
    for btn in answer_buttons:
        btn.config(bg="#444444", fg="white", activebackground="#555555", relief="flat")  # Przyciski odpowiedzi
    for tab in [exam_tab, previous_exam_tab]:
        tab.config(bg="#333333")  # Tło ramek w zakładkach
    dark_mode_button.config(bg="#666666", fg="white", activebackground="#777777")  # Przycisk zmiany motywu
    # Tworzenie niestandardowego stylu dla nagłówków
    style = ttk.Style()
    style.configure("Treeview.Heading", background="#333333", foreground="white")
    tree.tag_configure('dark', background="#444444", foreground="white")  # Tabela
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Usunięcie poprzedniego sposobu ustawiania kolorów nagłówków
    tree.configure(style="Treeview")


def set_light_mode():
    # Ustawienie tła na jasny motyw
    root.config(bg="#f4f4f9")  # Tło całej aplikacji
    question_label.config(bg="#f4f4f9", fg="black")  # Etykieta pytania
    for btn in answer_buttons:
        btn.config(bg="#f1f1f1", fg="black", activebackground="#e0e0e0", relief="raised")  # Przyciski odpowiedzi
    for tab in [exam_tab, previous_exam_tab]:
        tab.config(bg="#f4f4f9")  # Tło ramek w zakładkach
    dark_mode_button.config(bg="#444444", fg="black", activebackground="#555555")  # Przycisk zmiany motywu
    for col in tree["columns"]:
        tree.heading(col, background="#f4f4f9", foreground="black")
    tree.tag_configure('light', background="#f1f1f1", foreground="black")  # Tabela


def main():
    global questions, root, question_label, answer_buttons, num_questions, tree, dark_mode_button, dark_mode, notebook, exam_tab, previous_exam_tab
    filename = "ccna_questions.txt"
    questions = load_questions(filename)
    num_questions = 50
    dark_mode = False  # Zmienna globalna zdefiniowana na początku

    root = tk.Tk()
    root.title("CCNA Quiz")
    root.geometry("800x600")
    root.config(bg="#f4f4f9")  # Początkowy jasny motyw

    notebook = ttk.Notebook(root)
    exam_tab = tk.Frame(notebook, bg="#f4f4f9")
    previous_exam_tab = tk.Frame(notebook, bg="#f4f4f9")
    notebook.add(exam_tab, text="Egzamin")
    notebook.add(previous_exam_tab, text="Poprzedni egzamin")
    notebook.pack(expand=True, fill="both")

    tk.Label(exam_tab, text="Wybierz tryb:", font=("Segoe UI", 14), bg="#f4f4f9").pack(pady=10)
    tk.Button(exam_tab, text="Ćwicz", command=lambda: start_exam("practice"), font=("Segoe UI", 12), width=20, height=2, relief="raised", bg="#4CAF50", fg="white", activebackground="#45a049").pack(pady=10)
    tk.Button(exam_tab, text="Zdaj egzamin", command=lambda: start_exam("exam"), font=("Segoe UI", 12), width=20, height=2, relief="raised", bg="#008CBA", fg="white", activebackground="#007B9D").pack(pady=10)

    question_label = tk.Label(exam_tab, text="", wraplength=400, font=("Segoe UI", 16), bg="#f4f4f9")
    question_label.pack(pady=20)

    answer_buttons = [tk.Button(exam_tab, text="", font=("Segoe UI", 12), width=75, height=2, relief="raised", bg="#f1f1f1", activebackground="#e0e0e0") for _ in range(4)]
    for btn in answer_buttons:
        btn.pack(pady=5)

    dark_mode_button = tk.Button(exam_tab, text="Tryb ciemny", command=toggle_dark_mode, font=("Segoe UI", 12), width=20, height=2, relief="raised", bg="#444444", fg="black", activebackground="#555555")
    dark_mode_button.pack(pady=20)

    columns = ("Pytanie", "Twoja odpowiedź", "Poprawna odpowiedź", "Wynik")
    tree = ttk.Treeview(previous_exam_tab, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")
    tree.pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
