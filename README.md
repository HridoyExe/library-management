# 📚 Library Management API

A **Django REST Framework (DRF)** powered API to manage a library system with authors, books, members, and borrowing operations.

---

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.1-green)
![DRF](https://img.shields.io/badge/DRF-3.15-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

- **Authors**
  - List, retrieve, create, update, delete
  - Search by `id` or `name`

- **Books**
  - List, retrieve, create, update, delete (**Librarian only**)
  - Search by `title`, `isbn`, `category`, or `author name`
  - Track availability status

- **Members**
  - List, retrieve, create, update, delete
  - Search by `id` or `email`

- **Borrow/Return**
  - Borrow a book for a member
  - Return a borrowed book
  - Validates availability and prevents duplicate borrow

- Pagination for listing large datasets  
- Swagger Documentation for easy API exploration

---

## 🗂 Models

### Author
- `id`
- `name`

### Book
- `id`
- `title`
- `isbn`
- `category`
- `availability_status` (True if available)
- `author` (ForeignKey)

### Member
- `id`
- `name`
- `email`

### BorrowRecord
- `id`
- `book` (ForeignKey)
- `member` (ForeignKey)
- `borrow_date`
- `return_date`

---

## 🔗 API Endpoints

### Authors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/authors/` | List all authors |
| GET | `/api/authors/{id}/` | Retrieve author details |
| POST | `/api/authors/` | Create author |
| PUT | `/api/authors/{id}/` | Update author |
| DELETE | `/api/authors/{id}/` | Delete author |

### Books
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books/` | List all books |
| GET | `/api/books/{id}/` | Retrieve book details |
| POST | `/api/books/` | Create book (**Librarian only**) |
| PUT | `/api/books/{id}/` | Update book (**Librarian only**) |
| DELETE | `/api/books/{id}/` | Delete book (**Librarian only**) |

### Members
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/members/` | List all members |
| GET | `/api/members/{id}/` | Retrieve member details |
| POST | `/api/members/` | Create member |
| PUT | `/api/members/{id}/` | Update member |
| DELETE | `/api/members/{id}/` | Delete member |

### Borrow Records
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/borrow-records/borrow_book/` | Borrow a book |
| POST | `/api/borrow-records/{id}/return_book/` | Return a borrowed book |

**Borrow Book Request Example:**
```json
{
  "book_id": 1,
  "member_id": 2
}
