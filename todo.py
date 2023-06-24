import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

file_path = 'todo.json'

class GetMixin:
    def get_data(self):
        with open(file_path) as file:
            return json.load(file)
        
    def get_id(self):
        with open('id.txt') as file:
            id = int(file.read())
            id += 1
        with open('id.txt', 'w') as file:
            file.write(str(id))
        return id 

class CreateMixin(GetMixin):
    def create(self):
        data = super().get_data()
        try:
            new_task = {

                'id': super().get_id(),
                'todo':input('Введите задание что вы хотите сделать: '),
                'deadline':datetime.strptime(input('Введите дедлайн (YYYY-MM-DD): '), "%Y-%m-%d")
                
                }
        except ValueError:
            print('Ввели некорректные данные')
            self.create()
        else:
            new_task['days_left'] = (new_task['deadline'].date() - datetime.now().date()).days
            data.append(new_task)
            

            with open(file_path, 'w') as file:
                json.dump(data, file, cls=DateTimeEncoder)  # Используйте пользовательский сериализатор
            print('Successfully created')

class ListingMixin(GetMixin):
    def listing(self):
        print('Список задач')
        data = super().get_data()
        print(data)
        print('End')

class RetrieveMixin(GetMixin):
    def retrieve(self):
        data = super().get_data()

        try:
            id = int(input('Введите номер задачи: '))
        except ValueError:
            print('Ввели некорректные данные')
            self.retrieve()
        else:
            one_task= list(filter(lambda x: x['id'] == id, data))
           
            if not one_task:
                print('Такой задачи нет')
            else:
                print(one_task[0])
class UpdateMixin(GetMixin):
    def update(self):
        data = super().get_data()

        while True:
            try:
                id = int(input('Введите номер задачи: '))
                break
            except ValueError:
                print('Ввели некорректные данные')

        one_task = list(filter(lambda x: x['id'] == id, data))

        if not one_task:
            print('Такой задачи нет')
            return
        task = data.index(one_task[0])

        while True:
            choice = input('Что вы хотите изменить? 1 - todo, 2 - deadline: ')
            if choice not in {'1', '2'}:
                print('Такого поля нет')
                continue
            elif choice == 1:
                data[task]['todo'] = input('Введите новый todo: ')

            elif choice == 2:
                try:
                    data[task]['deadline'] = input('Введите новый deadline: ')
                    data[task]['days_left'] = (task['deadline'].date() - datetime.now().date()).days
                except ValueError:
                    print('========')

                with open(file_path, 'w')as file:
                    json.dump(data, file)

class DeleteMixin(GetMixin):
    def delete(self):
        data = super().get_data()
        try:
            id = int(input('Введите номер задачи: '))
        except ValueError:
            print('Ввели некорректные данные')
            self.delete()
        else:
            one_product = list(filter(lambda x: x['id'] == id, data))
            if not one_product:
                print('Такой задачи нет')
            product = data.index(one_product[0])
            data.pop(product)

            with open(file_path, 'w')as file:
                json.dump(data, file)
            print('Удалили')

class Todo(CreateMixin,ListingMixin,RetrieveMixin,UpdateMixin,DeleteMixin):
    def __init__(self):
        pass

todo = Todo()

while True:
    o = int(input('Please choose what you want to do, list above. Write only number: '))
    if o ==1:
        todo.create()
    elif o ==2:
        todo.listing()
    elif o ==3:
        todo.update()
    elif o ==4:
        todo.delete()
    elif o=='exit':
        break
    else:
        print('Not found command')