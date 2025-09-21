import tkinter as tk
from tkinter import messagebox
import string

class CodeBreakerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 CODE BREAKER")
        self.root.configure(bg='#FFE7C7')
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        self.word = ""
        self.difficulty = None
        self.guessed = []
        self.guessed_letters = set()
        self.attempts = 6
        self.hint_letter_pos = None

        self.create_start_screen()

    def create_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg='#FFE7C7')
        main_frame.pack(expand=True, fill='both')

        content_frame = tk.Frame(main_frame, bg='#FFE7C7')
        content_frame.place(relx=0.5, rely=0.5, anchor='center')

        title = tk.Label(content_frame, text="🔐 Welcome to CODE BREAKER!", font=("Arial", 20),
                         bg='#FFE7C7', fg='#333333')
        title.pack(pady=20)

        diff_label = tk.Label(content_frame, text="Choose difficulty:", font=("Arial", 14),
                              bg='#FFE7C7', fg='#333333')
        diff_label.pack(pady=(0, 10))

        self.diff_var = tk.StringVar(value="1")
        difficulties = [
            ("Easy (3-5 letters)", "1"),
            ("Medium (6-8 letters)", "2"),
            ("Hard (9+ letters)", "3"),
            ("Any length", "4")
        ]

        diff_frame = tk.Frame(content_frame, bg='#FFE7C7')
        diff_frame.pack(pady=10)

        for text, val in difficulties:
            rb = tk.Radiobutton(diff_frame, text=text, variable=self.diff_var, value=val,
                               font=("Arial", 12), bg='#FFE7C7', fg='#333333',
                               selectcolor='#d1e7dd', activebackground='#FFE7C7',
                               anchor='w', width=20)
            rb.pack(pady=2)

        btn_start = tk.Button(content_frame, text="Start Game", command=self.word_entry_screen,
                              font=("Arial", 14), bg='#d1e7dd', fg='#333333',
                              activebackground='#a3cfbb', relief='flat', padx=20)
        btn_start.pack(pady=30)

    def word_entry_screen(self):
        self.difficulty = self.diff_var.get()

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg='#FFE7C7')
        main_frame.pack(expand=True, fill='both')

        content_frame = tk.Frame(main_frame, bg='#FFE7C7')
        content_frame.place(relx=0.5, rely=0.5, anchor='center')

        label = tk.Label(content_frame, text="Enter your own word to guess:", font=("Arial", 16),
                         bg='#FFE7C7', fg='#333333')
        label.pack(pady=20)

        self.word_entry = tk.Entry(content_frame, font=("Arial", 16), show="*",
                                   bg='#ffffff', fg='#333333', insertbackground='#333333')
        self.word_entry.pack(pady=10)
        self.word_entry.focus()

        self.error_label = tk.Label(content_frame, text="", fg="#d9534f", font=("Arial", 12),
                                   bg='#FFE7C7')
        self.error_label.pack()

        btn_submit = tk.Button(content_frame, text="Submit Word", command=self.validate_word,
                               font=("Arial", 14), bg='#d1e7dd', fg='#333333',
                               activebackground='#a3cfbb', relief='flat', padx=20)
        btn_submit.pack(pady=20)

        btn_back = tk.Button(content_frame, text="Back", command=self.create_start_screen,
                             bg='#c0c0c0', fg='#333333', activebackground='#a3cfbb', relief='flat')
        btn_back.pack()

    def validate_word(self):
        word = self.word_entry.get().strip()
        if not word.isalpha():
            self.error_label.config(text="⚠ Please enter letters only.")
            return

        word_len = len(word)
        if self.difficulty == "1" and not (3 <= word_len <= 5):
            self.error_label.config(text="⚠ Easy mode: word must be 3-5 letters.")
            return
        elif self.difficulty == "2" and not (6 <= word_len <= 8):
            self.error_label.config(text="⚠ Medium mode: word must be 6-8 letters.")
            return
        elif self.difficulty == "3" and word_len < 9:
            self.error_label.config(text="⚠ Hard mode: word must be 9+ letters.")
            return

        self.word = word.upper()
        self.guessed = ["_"] * len(self.word)
        self.guessed_letters = set()
        self.attempts = 6

        answer = messagebox.askyesno("Hint Letter", "GUESSER: Do you want one letter revealed as a hint?")
        if answer:
            self.hint_letter_pos = len(self.word) // 2
            hint_letter = self.word[self.hint_letter_pos]
            self.guessed[self.hint_letter_pos] = hint_letter
            self.guessed_letters.add(hint_letter)
            self.attempts = 5
        else:
            self.hint_letter_pos = None

        self.create_game_screen()

    def create_game_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg='#FFE7C7')
        main_frame.pack(expand=True, fill='both')

        content_frame = tk.Frame(main_frame, bg='#FFE7C7')
        content_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.word_label = tk.Label(content_frame, text=" ".join(self.guessed), font=("Courier", 30),
                                  bg='#FFE7C7', fg='#333333')
        self.word_label.pack(pady=30)

        self.attempts_label = tk.Label(content_frame, text=f"Attempts left: {self.attempts}",
                                       font=("Arial", 14), bg='#FFE7C7', fg='#d9534f')
        self.attempts_label.pack(pady=5)

        self.guessed_label = tk.Label(content_frame, text="Guessed letters: ", font=("Arial", 14),
                                      bg='#FFE7C7', fg='#555555')
        self.guessed_label.pack(pady=5)

        letters_frame = tk.Frame(content_frame, bg='#FFE7C7')
        letters_frame.pack(pady=20)

        self.letter_buttons = {}
        for i, letter in enumerate(string.ascii_uppercase):
            btn = tk.Button(letters_frame, text=letter, width=3, font=("Arial", 12),
                            command=lambda l=letter: self.guess_letter(l),
                            bg='#d1e7dd', fg='#333333', activebackground='#a3cfbb',
                            relief='flat', bd=1)
            btn.grid(row=i // 9, column=i % 9, padx=2, pady=2)
            self.letter_buttons[letter] = btn

        for letter in self.guessed_letters:
            if letter in self.letter_buttons:
                self.letter_buttons[letter].config(state="disabled", bg='#c0c0c0')

        self.message_label = tk.Label(content_frame, text="", font=("Arial", 14),
                                      bg='#FFE7C7', fg='#28a745')
        self.message_label.pack(pady=10)

        self.btn_restart = tk.Button(content_frame, text="Restart Game", command=self.create_start_screen,
                                     font=("Arial", 14), bg='#b39ddb', fg='#333333',
                                     activebackground='#9575cd', relief='flat', padx=20)
        self.btn_restart.pack(pady=10)

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            self.message_label.config(text="⏳ You already tried that letter.")
            return

        self.guessed_letters.add(letter)
        self.letter_buttons[letter].config(state="disabled", bg='#c0c0c0')

        if letter in self.word:
            self.message_label.config(text="✅ Good guess!")
            for i, l in enumerate(self.word):
                if l == letter:
                    self.guessed[i] = letter
        else:
            self.attempts -= 1
            self.message_label.config(text="❌ Wrong guess!")

        self.update_game_state()

    def update_game_state(self):
        self.word_label.config(text=" ".join(self.guessed))
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")
        guessed_letters_sorted = sorted(self.guessed_letters)
        self.guessed_label.config(text="Guessed letters: " + " ".join(guessed_letters_sorted))

        if "_" not in self.guessed:
            messagebox.showinfo("🎉 Congratulations!", f"You cracked the word: {self.word}")
            self.disable_all_letters()
        elif self.attempts <= 0:
            messagebox.showinfo("💀 Game Over", f"Out of attempts! The word was: {self.word}")
            self.disable_all_letters()

    def disable_all_letters(self):
        for btn in self.letter_buttons.values():
            btn.config(state="disabled", bg='#c0c0c0')

def main():
    root = tk.Tk()
    app = CodeBreakerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
