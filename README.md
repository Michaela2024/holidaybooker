# CS50 Web Programming Capstone – Holiday Booking System

##  Project Overview

The **Holiday Booking System** is a web application that allows registered users to book weekly stays at listed properties. Users can view, edit, and cancel their bookings, while property owners can list properties with location and guest constraints. The application integrates **real-time validation**, **role-based access**, **dynamic price calculation**, and **interactive maps** to provide a full-featured, professional-grade experience.

---

##  Distinctiveness and Complexity

The Holiday Booking System stands out from typical CS50 Web Programming projects by integrating multiple layers of business logic, real-time validation, and interactive features into a cohesive, production-grade experience. Unlike simpler CRUD applications, this project combines **role-based access control, booking constraints, dynamic pricing, geospatial mapping, and AJAX-driven interactivity**, demonstrating a depth of design and implementation beyond standard course assignments.

A core aspect is the **role-based constraint** for users. Each registered user can assume only one role at a time: either a **property owner** or a **holiday booker**. This prevents conflicts such as booking one’s own property. Role enforcement occurs across the backend and frontend, dynamically adapting the UI and available actions to the user’s current role.

Bookings enforce multiple **business rules** that mirror real-world vacation rental systems. Check-in and check-out dates must be **Saturdays**, each booking must span **exactly seven nights**, and properties have a **maximum guest limit**. Validation occurs both client-side with JavaScript and server-side through Django forms and models. Upon submission, bookings are immediately **confirmed**, displaying total price, status, and details on the user’s “My Bookings” page. Users can edit or cancel bookings via a **modal interface** with AJAX, providing seamless updates without page reloads.

The **property detail page** includes an **interactive OpenStreetMap map** implemented with **Leaflet.js**. Property addresses are geocoded using the **Nominatim API**, converting addresses into coordinates displayed on the map. This demonstrates external API integration, real-time data handling, and geospatial reasoning. 

From an architectural perspective, the system is built with a **modular Django structure**, separating apps for bookings, properties, and users. Database models enforce relational integrity, while templates and static files are organised for maintainability. JavaScript and AJAX provide dynamic, client-side behavior, enabling live validation, modal editing, and real-time updates. The combination of **frontend responsiveness**, **backend validation**, **role-based access**, and **geospatial visualisation** makes this project significantly more complex than typical student assignments.

---

##  Features

- Role-based user accounts: owner or booker (one role at a time)  
- Create bookings with validation for dates, guests, and duration  
- Edit or cancel confirmed bookings via modal interface  
- Real-time total price calculation  
- Booking statuses displayed with badges (confirmed, cancelled, pending)  
- Property detail pages with **interactive OpenStreetMap maps**  
- AJAX for editing/cancelling bookings without page reload  
- Responsive design using Bootstrap  
- Backend validation for all business rules  

---

## File Structure

| **layout.html** | Base template with header, footer, navigation, and common scripts/styles. |
| **index.html** | Homepage showing available properties to browse and search. |
| **login.html** | User login page. |
| **register.html** | User registration page; allows role selection (owner or booker). |
| **my_bookings.html** | Displays user’s bookings; supports editing, cancelling, and viewing details with total price and status. |
| **property_detail.html** | Shows property details including **location, max guests, and interactive map**. Users can book from this page. |

---

## ## How to Run

- Create an environment, install python and create dependencies
- Clone the repo and enter the folder cd holidaybooker
- Apply migrations and create a superuser
- Start the server (python manage.py runserver)
- Access the app at http://127.0.0.1:8000/ and admin at http://127.0.0.1:8000/admin.
- Add properties via the admin before making bookings.


