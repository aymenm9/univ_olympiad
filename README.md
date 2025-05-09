# 🥇 1st Place
# 🏛️ Univ Olympiad - Civil Registration Management API

This project is a **Django REST Framework-based system** for managing civil registration data including **births, deaths, certificates, and burial permits**, as well as organizational structures like **APCs**, **Hospitals**, and **Courts**. It enforces strict **role-based access control**, automates document generation (PDFs), and supports JWT-based authentication.

---

## 📌 Overview

The API supports:

- ✅ **Civil Records Management** (birth/death registrations, certificates, burial permits)
- 🏢 **Administrative Structures** (DSPs, APCs, Hospitals, Courts)
- 👤 **User Management & Authentication** (role-based access)
- 📈 **Statistical Reporting**
- 🤖 **AI Endpoint for Death Data**
- 🗣️ **Chatbot API**

---

## 🏗️ Organizational Hierarchy

- **DSP (Direction de la Santé Publique)**: Top-level unit, created via Django Admin.
  - Manages multiple:
    - **APCs (Communal People’s Assemblies)**
    - **Hospitals**
    - **Courts**

Each sub-entity has its own users and handles related records.

---

## 🔐 Role-Based Access Control

| Role   | Scope                                                                 |
|--------|-----------------------------------------------------------------------|
| **Admin**  | Full access in their org. Can manage records and create accounts for coworkers. |
| **Worker** | Can create/edit records within assigned entity (e.g. hospital staff).         |
| **Guest**  | Read-only access, including sensitive/personal data.                         |

---

## 🔄 Data Flow & Record Validation

### Birth Registration

1. **Hospital Worker** creates a birth record.
2. A **non-valid birth certificate** is automatically generated.
3. The **APC Admin** for the related APC must confirm it to validate the certificate.

### Death Registration

1. **Hospital Worker** creates a death record.
2. If death is marked as **not normal**, the **burial permit is withheld**.
3. **Court Admin** must approve the record before burial permit is issued.

---

## 📂 Key API Endpoints

### Civil Records

- `/api/birth/`, `/api/birth/{birth_number}/`
- `/api/birth_certificate/`, `/api/birth_certificate_confirm/{birth_number}/`
- `/api/birth_certificate_pdf/{birth_number}/`, `/api/public_birth_certificate/`
- `/api/death/`, `/api/death_certificate/`
- `/api/death_certificate_confirm/{death_number}/`
- `/api/death_certificate_pdf/{death_number}/`, `/api/public_death_certificate/`
- `/api/generate_death_ai/`
- `/api/burial_permit/`, `/api/burial_permit_confirm/{death_number}/`
- `/api/burial_permit_pdf/{death_number}/`

### Entities

- `/api/apc/`, `/api/apc_list/`
- `/api/hospital/`, `/api/hospital_list/`
- `/api/court/`, `/api/court_list/`

### Users & Auth

- `/api/users/`, `/api/user/`
- `/api/password_change/`
- `/api/token/`, `/api/token/refresh/`

### Statistics

- `/api/statistics/`
- `/api/statistics/by_month/`
- `/api/statistics_v2/`

### Utility

- `/api/chatbot/` (GET, POST, DELETE)
- `/api/schema/` (OpenAPI format)

---

## ⚙️ Technologies Used

- **Python 3**
- **Django**
- **Django REST Framework**
- **JWT Authentication**
- **WeasyPrint** (for PDF generation)
- **SQLite** (or configurable DB backend)

---