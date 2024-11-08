import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# Django backend URL
BACKEND_URL = 'http://127.0.0.1:8080/api/tasks/'

class TaskApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Input to add new tasks
        self.task_input = TextInput(hint_text="Enter new task", size_hint_y=None, height=40)
        self.layout.add_widget(self.task_input)

        # Button to add task
        add_button = Button(text="Add Task", size_hint_y=None, height=40)
        add_button.bind(on_press=self.add_task)
        self.layout.add_widget(add_button)

        # Container for tasks
        self.task_list = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.task_list)

        # Load existing tasks
        self.load_tasks()

        return self.layout

    def load_tasks(self):
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            self.task_list.clear_widgets()
            tasks = response.json()
            for task in tasks:
                self.add_task_widget(task)

    def add_task_widget(self, task):
        task_label = Label(text=task["title"], size_hint_y=None, height=40)
        delete_button = Button(text="Delete", size_hint_y=None, height=40)
        delete_button.bind(on_press=lambda instance, task_id=task["id"]: self.delete_task(task_id, task_label, delete_button))

        task_layout = BoxLayout(size_hint_y=None, height=40)
        task_layout.add_widget(task_label)
        task_layout.add_widget(delete_button)

        self.task_list.add_widget(task_layout)

    def add_task(self, instance):
        task_title = self.task_input.text
        if task_title:
            response = requests.post(BACKEND_URL, json={"title": task_title})
            if response.status_code == 201:
                new_task = response.json()
                self.add_task_widget(new_task)
                self.task_input.text = ""

    def delete_task(self, task_id, task_label, delete_button):
        response = requests.delete(f"{BACKEND_URL}{task_id}/")
        if response.status_code == 204:
            self.task_list.remove_widget(task_label.parent)

if __name__ == '__main__':
    TaskApp().run()
