import requests
import os
import datetime
def tasks_exception(counter_actual_tasks,counter_finished_tasks,user):
    if counter_actual_tasks+counter_finished_tasks>0:
        return True
    Exception(f"У пользователя {user['name']} нет задач")
def create_report(id,user,directory):
    filename = f"{directory}/{user['name']}.txt"
    filetxt = os.path.join(directory,filename)
    if os.path.exists(filetxt):
        old_filetxt = "old_" + user['username'] + "_" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M") + ".txt"
        os.rename(filename, os.path.join(directory, old_filetxt))
    counter_actual_tasks = 0
    counter_finished_tasks = 0
    actual_tasks= []
    finished_tasks = []
    todos_api0 = f'https://json.medrocket.ru/todos?userId={id}'
    todos_api = requests.get(todos_api0)
    todos = todos_api.json()
    for todo in todos:
        if ('completed' in todo):
            if (todo['completed']==True):
                counter_finished_tasks +=1
                finished_tasks.append(todo)
            else:
                counter_actual_tasks +=1
                actual_tasks.append(todo)
    if tasks_exception(counter_actual_tasks,counter_finished_tasks,user) == True:
        text = f"# Отчёт для {user['company']['name']} \n"
        text+= f"{user['name']} <{user['email']}> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n"
        text+= 'Всего задач: '+str(counter_actual_tasks+counter_finished_tasks) + '\n'
        text+= '\n'
        text+= f'## Актуальные задачи ({counter_actual_tasks}):'
        for i in actual_tasks:
            if (len(i["title"])>46):
                text+= f'- {i["title"][:46]}... \n'
            else:
                text += f'- {i["title"]} \n'
        text+= '\n'
        text+=f'## Завершённые задачи ({counter_finished_tasks}):'
        for j in finished_tasks:
            if (len(j["title"])>46):
                text+= f'- {j["title"][:46]}... \n'
            else:
                text += f'- {j["title"]} \n'
        with open(filename,'w',encoding='UTF-8') as file:
            file.write(text)




def main():
    directory = "tasks"
    if not os.path.exists(directory):
        os.makedirs(directory)
    users_api0 = 'https://json.medrocket.ru/users'
    users_api = requests.get(users_api0)
    users = users_api.json()
    for user in users:
        create_report(user['id'],user,directory)
if __name__ == "__main__":
    main()