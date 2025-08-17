# Tribute to Mozilla tutorial on Django
![App Screenshot](https://i.ibb.co/wrzgw07Y/Screenshot-2025-07-16-130529.png)

## Purpose

Build an application for a local library where people can find their favorite books and get them on loan.

## User Groups

- **User:**  
  - Check the availability of books in the library.
  - Borrow books for a maximum duration.
  - Search for books by title.

- **Librarian:**  
  - Manage book instances.

## Technology Stack

- **Backend:** Django  
- **Frontend:** VueJS  
- **Containerization:** Docker

## Features

- User authentication with ID proof.
- Account approval by librarian after ID verification.
- Librarian ability to blacklist a user.


## Running the Application

Follow these steps to run the application using Docker:

1. Clone the repository:
    ```bash
    git clone https://github.com/vikassrivastava18/Local-library.git
    cd Local-library
    ```

2. Build the Docker containers:
    ```bash
    docker-compose build
    ```

3. Start the application:
    ```bash
    docker-compose up
    ```

4. Access the application in your browser at `http://localhost:8080`.

## Stopping the Application

To stop the application, run:
```bash
docker-compose down
```

