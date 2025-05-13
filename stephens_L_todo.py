#imported modules needed
import argparse
import json


#setting up the file and feedback statements (req 1)
filename = "todo.json"
def load_todolist(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
        
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("todo file is corrupted or empty")
        return []
    
def save_todolist(todo_list, filename):
    with open(filename, 'w') as file:
        json.dump(todo_list, file, indent=4)


#adding items to todo list (req 3)
def add_item(args):
    todo_list = load_todolist(args.list_name)
    new_id = max([item['id'] for item in todo_list], default=0) + 1
    new_item = {
        "id" : new_id,
        'catagory' : args.catagory,
        'description': args.description,
        'status' : "incomplete"}
    
    todo_list.append(new_item)
    save_todolist(todo_list, args.list_name)
    print(f'Added to do item with ID {new_id}')

#showing the todo list (req 2)
def show_items(args):
    todo_list = load_todolist(args.list_name)
    if not todo_list:
        print("no to do items found.")
        return
    for item in todo_list:
        print(f"[{item['id']}] {item['category']} - {item['description']} ({item['status']})")


#updating the to do items (req 4)
def update_items(args):
    todo_list = load_todolist(args.list_name)
    for item in todo_list:
        if item ['id'] == args.id:
            if args.catagory:
                item['catagory'] = args.catagory
            if args.description:
                item["description"] = args.description
            if args.status:
                if args.status.lower() not in ["incomplete", "in progress", "complete"]:
                    print("Invalid status. Use 'incomplete', 'in progress', or 'complete'.")
                    return
                item["status"] = args.status.lower()
            save_todolist(todo_list, args.list_name)
            print(f"Updated item with ID {args.id}")
            return
    print(f"No item with ID {args.id} found.")

#setting up argparse and subcommands (req 4)
def main():
    parser = argparse.ArgumentParser(description= "todo list cli tool")
    parser.add_argument('--list-name', type=str, default=filename, help="name of the todo list file")
    subparser = parser.add_subparsers(dest='command')

    #adding commands (rec3)
    add_parser = subparser.add_parser("add", help="add a new todo item")
    add_parser.add_argument("catagory", type=str, help="catagory of the task")
    add_parser.add_argument('description', type=str, help='description of the task')
    add_parser.set_defaults(func=add_item)

    #showing the commands
    show_parser = subparser.add_parser("show", help="show all todo items")
    show_parser.set_defaults(func=show_items)

    #update commands
    update_parser = subparser.add_parser('update', help='update a current todo item')
    update_parser.add_argument('id', type=int, help= 'id of the todo item')
    update_parser.add_argument('--catagory', type=str, help='new catagory of the todo item')
    update_parser.add_argument('--description', type=str, help="new description of tod item")
    update_parser.add_argument('--status', type=str, help="new status (incomplete/in progress/complete)")
    update_parser.set_defaults(func=update_items)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
