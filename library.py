import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)


def add_member(name, email):
    payload = {"name": name, "email": email}
    resp = sb.table("members").insert(payload).execute()
    return resp.data


def list_members():
    resp = sb.table("members").select("*").order("member_id").execute()
    return resp.data


def delete_member(member_id):
    borrowed = sb.table("borrow_records").select("*") \
        .eq("member_id", member_id) \
        .is_("return_date", "null") \
        .execute()
    if borrowed.data:
        return "Cannot delete member — they still have borrowed books."

    history = sb.table("borrow_records").select("*").eq("member_id", member_id).execute()
    if history.data:
        return "Cannot delete member — they have borrow history."

    resp = sb.table("members").delete().eq("member_id", member_id).execute()
    if resp.data:
        return f"Member {member_id} deleted."
    else:
        return "Member not found."


def add_book(title, author, category, stock):
    payload = {"title": title, "author": author, "category": category, "stock": stock}
    resp = sb.table("books").insert(payload).execute()
    return resp.data


def list_books():
    resp = sb.table("books").select("*").order("book_id").execute()
    return resp.data


def search_books(keyword):
    resp = sb.table("books").select("*").or_(
        f"title.ilike.%{keyword}%,author.ilike.%{keyword}%,category.ilike.%{keyword}%"
    ).execute()
    return resp.data


def delete_book(book_id):
    borrowed = sb.table("borrow_records").select("*") \
        .eq("book_id", book_id) \
        .is_("return_date", "null") \
        .execute()
    if borrowed.data:
        return " Cannot delete book — it is currently borrowed."

    history = sb.table("borrow_records").select("*").eq("book_id", book_id).execute()
    if history.data:
        return "Cannot delete book — it has borrow history."

    resp = sb.table("books").delete().eq("book_id", book_id).execute()
    if resp.data:
        return f"Book {book_id} deleted."
    else:
        return "Book not found."


def borrow_book(member_id, book_id):
    book = sb.table("books").select("*").eq("book_id", book_id).execute()
    if not book.data:
        return "Book not found."
    if book.data[0]["stock"] <= 0:
        return "No stock available."

    payload = {"member_id": member_id, "book_id": book_id}
    resp = sb.table("borrow_records").insert(payload).execute()

    sb.table("books").update({"stock": book.data[0]["stock"] - 1}).eq("book_id", book_id).execute()

    return resp.data


def return_book(record_id):
    now = datetime.utcnow().isoformat()
    resp = sb.table("borrow_records").update({"return_date": now}).eq("record_id", record_id).execute()

    if resp.data:
        book_id = resp.data[0]["book_id"]
        book = sb.table("books").select("*").eq("book_id", book_id).execute()
        if book.data:
            sb.table("books").update({"stock": book.data[0]["stock"] + 1}).eq("book_id", book_id).execute()

    return resp.data


def overdue_books():
    limit_date = (datetime.utcnow() - timedelta(days=14)).isoformat()
    resp = sb.table("borrow_records").select("*") \
        .lt("borrow_date", limit_date) \
        .is_("return_date", "null") \
        .execute()
    return resp.data
