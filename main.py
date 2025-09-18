from library import (
    add_member, list_members,
    add_book, list_books, search_books,
    borrow_book, return_book,
    delete_member, delete_book,
    overdue_books
)

def main_menu():
    while True:
        print("\n📚 Library Management")
        print("1. Add Member")
        print("2. List Members")
        print("3. Add Book")
        print("4. List Books")
        print("5. Search Books")
        print("6. Borrow Book")
        print("7. Return Book")
        print("8. Delete Member")
        print("9. Delete Book")
        print("10. Overdue Books")
        print("0. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            print(add_member(name, email))

        elif choice == "2":
            members = list_members()
            for m in members:
                print(f"{m['member_id']}: {m['name']} ({m['email']})")

        elif choice == "3":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            category = input("Category: ").strip()
            stock = int(input("Stock: ").strip())
            print(add_book(title, author, category, stock))

        elif choice == "4":
            books = list_books()
            for b in books:
                print(f"{b['book_id']}: {b['title']} by {b['author']} ({b['category']}) — Stock: {b['stock']}")

        elif choice == "5":
            keyword = input("Search keyword: ").strip()
            books = search_books(keyword)
            for b in books:
                print(f"{b['book_id']}: {b['title']} by {b['author']} ({b['category']}) — Stock: {b['stock']}")

        elif choice == "6":
            mid = int(input("Member ID: ").strip())
            bid = int(input("Book ID: ").strip())
            print(borrow_book(mid, bid))

        elif choice == "7":
            rid = int(input("Borrow record ID: ").strip())
            print(return_book(rid))

        elif choice == "8":
            mid = int(input("Member ID to delete: ").strip())
            print(delete_member(mid))

        elif choice == "9":
            bid = int(input("Book ID to delete: ").strip())
            print(delete_book(bid))

        elif choice == "10":
            overdue = overdue_books()
            if overdue:
                print("Overdue books:")
                for r in overdue:
                    print(r)
            else:
                print("✅ No overdue books.")

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
