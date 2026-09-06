# Trekking Management Application - V2

## Overview

The **Trekking Management Application (TMA)** is a role-based web application developed as part of the **Modern Application Development II (MAD-II)** course. The application is designed to simplify and automate the management of trekking events by providing a centralized platform for administrators, trek staff, and trekkers.

Traditional trekking organizations often rely on spreadsheets, phone calls, and manual coordination for managing trek schedules, participant registrations, staff assignments, and booking records. This project digitizes these operations through a secure and user-friendly web application.

The system enables administrators to manage trekking routes and staff, allows trek staff to coordinate assigned treks, and provides trekkers with an easy way to discover, book, and track trekking activities.

---

## Objectives

- Digitize trekking management operations.
- Simplify trek scheduling and participant management.
- Prevent manual errors such as duplicate bookings and overbooking.
- Maintain complete trekking history for every participant.
- Automate reminders and report generation using background jobs.
- Improve performance using Redis caching.

---

## User Roles

### Admin

The administrator manages the complete trekking platform.

Responsibilities include:

- Create, update, and remove trekking routes
- Add and manage trek staff
- Assign staff members to treks
- View all users, staff, bookings, and trekking history
- Search treks, users, and staff
- Deactivate or blacklist users and staff
- Monitor trekking statistics and reports

---

### Trek Staff

Trek staff members manage only the treks assigned to them.

Responsibilities include:

- View assigned treks
- Manage available trek slots
- Update trek status
- View registered participants
- Mark treks as started or completed

---

### Trekker (User)

Trekkers can register and participate in trekking activities.

Responsibilities include:

- Register and log in
- View available treks
- Search and filter trekking routes
- Book treks
- View booking status
- Access personal trekking history
- Update profile information

---

## Core Features

- Secure role-based authentication
- Trek creation and management
- Trek staff management
- Trek booking system
- Trek availability management
- Booking history tracking
- Search and filtering of treks
- Prevention of duplicate bookings
- Prevention of overbooking
- Trek status tracking
- Monthly activity reports
- Daily trek reminders
- CSV export of booking history
- Redis-based API caching
- Asynchronous background jobs using Celery

---

## Technology Stack

### Backend

- Flask
- SQLAlchemy
- SQLite
- Redis
- Celery

### Frontend

- Vue.js
- Bootstrap

---

## Database

The application uses **SQLite** as its primary database.

The database schema is created programmatically using SQLAlchemy models, ensuring that no manual database creation is required.

---

## Background Jobs

Celery and Redis are used to execute asynchronous tasks, including:

- Daily reminders for upcoming treks
- Monthly trekking activity reports
- Export of trekking history as CSV

---

## Course Information

**Course:** Modern Application Development II (MAD-II)

**Project:** Trekking Management Application - V2

**Institution:** IIT Madras BS Degree Programme