from src import process_boards
from src import templates

def main():
    process_boards.print_init_message()
    image_path, image_model = process_boards.analyze_all_boards()
    templates.print_init_message()
    templates.check_all_templates(image_path, image_model, process_boards.boards_paths)
    templates.print_results(process_boards.boards_paths)

if __name__ == '__main__':
    main()
