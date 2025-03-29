import tkinter as tk
from tkinter import filedialog, scrolledtext
import random
import requests
from bs4 import BeautifulSoup

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary Trainer")
        self.root.geometry("1300x700")
        self.root.configure(bg="#222")
        
        # Variables to store vocabulary and current word
        self.vocabulary = []  # List to store vocabulary lines
        self.current_word = None  # Current word/phrase being displayed
        self.current_language = "german"  # Tracks the current language (german/english)
        self.score = 0  # Initialize score
        self.total_questions = 0  # Total number of questions asked
        self.correct_answers = 0  # Number of correct answers
        self.flip_mode = False  # Tracks whether flip mode is active
        
        # Left Side - Vocabulary, Study Text, and Translation Boxes
        self.create_left_section()
        
        # Middle - Buttons for LOAD, SAVE, etc.
        self.create_middle_section()
        
        # Right Side - Example Sentences, Test Section, Dictionary Search
        self.create_right_section()

    def create_left_section(self):
        left_frame = tk.Frame(self.root, bg="#222")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.vocabulary_textbox = self.create_labeled_textbox(left_frame, "Vocabulary:", True, height=10)
        self.study_textbox = self.create_labeled_textbox(left_frame, "Study Text Box:", True, height=10)
        self.translation_textbox = self.create_labeled_textbox(left_frame, "Translation Box:", True, height=10)
   
    def create_middle_section(self):
        middle_frame = tk.Frame(self.root, bg="#222")
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=35)
        
        # Buttons for Vocabulary Box
        tk.Button(middle_frame, text="LOAD-VOC", bg="#336699", fg="white", command=self.load_vocabulary).pack(pady=5)
        tk.Button(middle_frame, text="SAVE-VOC", bg="#008844", fg="white", command=self.save_vocabulary).pack(pady=5)
        tk.Button(middle_frame, text="SORT", bg="#AA8800", fg="black", command=self.sort_vocabulary).pack(pady=10)
        tk.Button(middle_frame, text="CLR-VOC", bg="#AA0000", fg="white", command=self.clear_vocabulary).pack(pady=15)
        
        # Buttons for Study Text Box
        tk.Button(middle_frame, text="LOAD-TXT", bg="#336699", fg="white", command=self.load_study_text).pack(pady=15)
        tk.Button(middle_frame, text="SAVE-TXT", bg="#008844", fg="white", command=self.save_study_text).pack(pady=5)
        tk.Button(middle_frame, text="CLR-TXT", bg="#AA0000", fg="white", command=self.clear_study_text).pack(pady=5)
        tk.Button(middle_frame, text="NOTES", bg="#AA8800", fg="black", command=self.add_notes).pack(pady=20)
        
        # Buttons for Translation Box
        tk.Button(middle_frame, text="LOAD-TRA", bg="#336699", fg="white", command=self.load_translation).pack(pady=20)
        tk.Button(middle_frame, text="SAVE-TRA", bg="#008844", fg="white", command=self.save_translation).pack(pady=5)
        tk.Button(middle_frame, text="CLR-TRA", bg="#AA0000", fg="white", command=self.clear_translation).pack(pady=15)
   
    def create_right_section(self):
        right_frame = tk.Frame(self.root, bg="#222")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Example Sentences
        self.example_sentences_textbox = self.create_labeled_textbox(right_frame, "EXAMPLE SENTENCES", True, height=10)
        
        # New Input Box for Glosbe Search
        self.glosbe_search_entry = tk.Entry(right_frame, bg="black", fg="white", insertbackground="white", font=("Tahoma", 11))
        self.glosbe_search_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons for Example Sentences
        btn_frame = tk.Frame(right_frame, bg="#222")
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="Glosbe Examples", bg="#004466", fg="white", command=self.fetch_glosbe_examples).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save Examples", bg="#008844", fg="white", command=self.save_examples).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="CLEAR", bg="#AA0000", fg="white", command=self.clear_example_sentences).pack(side=tk.LEFT, padx=5)
        
        # Vocabulary Test Section
        test_frame = tk.Frame(right_frame, bg="#222")
        test_frame.pack(fill=tk.X, pady=10)
        tk.Label(test_frame, text="Take a Vocabulary Test from File:", fg="gold", bg="#222").pack(anchor='w')
        
        btn_frame2 = tk.Frame(test_frame, bg="#222")
        btn_frame2.pack(fill=tk.X)
        tk.Button(btn_frame2, text="Choose File", bg="#336699", fg="white", command=self.load_test_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame2, text="Flip Sentences", bg="#AA8800", fg="black", command=self.toggle_flip_mode).pack(side=tk.LEFT, padx=5)
        
        self.test_filename_label = tk.Label(test_frame, text="File is:", fg="white", bg="#222")
        self.test_filename_label.pack(anchor='w')
        
        self.test_textbox = scrolledtext.ScrolledText(test_frame, height=6, wrap=tk.WORD, bg="#333", fg="white", font=("Tahoma", 11))
        self.test_textbox.pack(fill=tk.X)
        
        # Answer Input
        tk.Label(right_frame, text="Type your answer below and then PRESS the ENTER key", fg="gold", bg="#222").pack(anchor='w')
        self.answer_entry = tk.Entry(right_frame, bg="black", fg="white", insertbackground="white", font=("Tahoma", 11))
        self.answer_entry.pack(fill=tk.X)
        self.answer_entry.bind("<Return>", self.check_answer)
        
        answer_frame = tk.Frame(right_frame, bg="#222")
        answer_frame.pack(fill=tk.X)
        tk.Button(answer_frame, text="Next Word", bg="#005588", fg="white", command=self.next_word).pack(side=tk.LEFT, padx=5)
        tk.Button(answer_frame, text="Clear Input", bg="yellow", fg="black", command=self.clear_input).pack(side=tk.LEFT, padx=5)
        tk.Label(answer_frame, text="Score:", fg="white", bg="#222").pack(side=tk.LEFT, padx=5)
        self.score_label = tk.Label(answer_frame, text="0%", fg="white", bg="#222")
        self.score_label.pack(side=tk.LEFT)
        
        # Dictionary Search
        tk.Label(right_frame, text="SEARCH ONLINE DICTIONARIES", fg="gold", bg="#222").pack(anchor='w', pady=5)
        self.dictionary_entry = tk.Entry(right_frame, bg="black", fg="white", insertbackground="white", font=("Tahoma", 11))
        self.dictionary_entry.pack(fill=tk.X)
        
        dict_btn_frame = tk.Frame(right_frame, bg="#222")
        dict_btn_frame.pack(fill=tk.X)
        tk.Button(dict_btn_frame, text="Langenscheidt", bg="#446688", fg="white", command=self.fetch_langenscheidt).pack(side=tk.LEFT, padx=5)
   
    def create_labeled_textbox(self, parent, label_text, add_scrollbar=False, height=5):
        frame = tk.Frame(parent, bg="#222")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame, text=label_text, fg="gold", bg="#222").pack(anchor='w')
        textbox = scrolledtext.ScrolledText(frame, height=height, wrap=tk.WORD, bg="#333", fg="white", font=("Tahoma", 11))
        textbox.pack(fill=tk.BOTH, expand=True)
        return textbox
   
    def load_vocabulary(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                self.vocabulary_textbox.insert(tk.END, content)
                self.vocabulary = [line.strip() for line in content.splitlines() if line.strip()]
   
    def save_vocabulary(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                content = self.vocabulary_textbox.get(1.0, tk.END)
                file.write(content)
   
    def sort_vocabulary(self):
        content = self.vocabulary_textbox.get(1.0, tk.END)
        sorted_content = ''.join(sorted(content.splitlines(True)))
        self.vocabulary_textbox.delete(1.0, tk.END)
        self.vocabulary_textbox.insert(tk.END, sorted_content)
   
    def clear_vocabulary(self):
        self.vocabulary_textbox.delete(1.0, tk.END)
   
    def load_study_text(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                self.study_textbox.insert(tk.END, content)
   
    def save_study_text(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                content = self.study_textbox.get(1.0, tk.END)
                file.write(content)
   
    def clear_study_text(self):
        self.study_textbox.delete(1.0, tk.END)
   
    def add_notes(self):
        # Placeholder for adding notes functionality
        pass
   
    def load_translation(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                self.translation_textbox.insert(tk.END, content)
   
    def save_translation(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                content = self.translation_textbox.get(1.0, tk.END)
                file.write(content)
   
    def clear_translation(self):
        self.translation_textbox.delete(1.0, tk.END)
   
    def fetch_glosbe_examples(self):
        word = self.glosbe_search_entry.get().strip()
        if not word:
            return
        
        url = f"https://glosbe.com/de/en/{word}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.example_sentences_textbox.insert(tk.END, f"Failed to retrieve the page. Status code: {response.status_code}\n")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        examples_list = []
        
        for example in soup.find_all('div', class_='mt-1 w-full flex text-gray-900 text-sm py-1 px-2 dir-aware-border-start-2 border-gray-300 translation__example'):
            german_p = example.find('p', class_='w-1/2 dir-aware-pr-1')
            german = german_p.text.strip() if german_p else "N/A"
            
            english_p = example.find('p', class_='w-1/2 px-1 ml-2')
            english = english_p.text.strip() if english_p else "N/A"
            
            example_pair = f"{german} = {english}\n"
            examples_list.append(example_pair)
        
        self.example_sentences_textbox.delete(1.0, tk.END)
        for example in examples_list:
            self.example_sentences_textbox.insert(tk.END, example)
   
    def fetch_langenscheidt(self):
        word = self.dictionary_entry.get().strip()
        if not word:
            return
        
        url = f"https://en.langenscheidt.com/german-english/{word}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.vocabulary_textbox.insert(tk.END, f"Failed to retrieve the page. Status code: {response.status_code}\n")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        myList = []
        
        for transl in soup.find_all('a', class_='blue'):
            myStr = transl.find('span', class_='btn-inner').text
            article = soup.find('span', class_='full').text
            if article == 'Femininum | feminine':
                article = 'die'
            elif article == 'Maskulinum | masculine':
                article = 'der'
            elif article == 'Neutrum | neuter':
                article = 'das'
            else:
                article = ''
            myStr = myStr.strip()
            myList.append(myStr)
        
        meaning = ', '.join(myList)
        self.vocabulary_textbox.insert(tk.END, f"{word}, {article} = {meaning}\n")
   
    def save_examples(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                content = self.example_sentences_textbox.get(1.0, tk.END)
                file.write(content)
   
    def clear_example_sentences(self):
        self.example_sentences_textbox.delete(1.0, tk.END)
   
    def load_test_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.test_filename_label.config(text=f"File is: {filename}")
            with open(filename, 'r', encoding='utf-8') as file:
                self.vocabulary = [line.strip() for line in file.readlines() if line.strip()]
            self.display_random_word()
   
    def display_random_word(self):
        if not self.vocabulary:
            self.test_textbox.delete(1.0, tk.END)
            self.test_textbox.insert(tk.END, "No vocabulary loaded.\n")
            return
        
        self.current_word = random.choice(self.vocabulary)
        self.test_textbox.delete(1.0, tk.END)
        self.test_textbox.insert(tk.END, "Please translate the following:\n")
        
        if self.flip_mode:
            english_word = self.current_word.split(' = ')[1]
            self.test_textbox.insert(tk.END, f"--> {english_word}\n")
        else:
            german_word = self.current_word.split(' = ')[0]
            self.test_textbox.insert(tk.END, f"--> {german_word}\n")
   
    def toggle_flip_mode(self):
        self.flip_mode = not self.flip_mode
        self.display_random_word()
   
    def next_word(self):
        self.display_random_word()
    
    def clear_input(self):
        self.answer_entry.delete(0, tk.END)
    
    def check_answer(self, event=None):
        user_answer = self.answer_entry.get().strip()
        if self.flip_mode:
            correct_answers = self.current_word.split(' = ')[0].split(', ')
        else:
            correct_answers = self.current_word.split(' = ')[1].split(', ')
        
        self.total_questions += 1
        
        if user_answer.lower() in [answer.lower() for answer in correct_answers]:
            self.test_textbox.insert(tk.END, "*** Congratulations! You are correct ***\n")
            self.correct_answers += 1
        else:
            self.test_textbox.insert(tk.END, f"*** I'm sorry. The correct answer is: {', '.join(correct_answers)} ***\n")
        
        # Calculate score
        if self.total_questions > 0:
            self.score = round((self.correct_answers / self.total_questions) * 100)
            self.score_label.config(text=f"{self.score}%")
        
        self.clear_input()

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()