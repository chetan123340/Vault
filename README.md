## App Vault - Securely Manage and Access Book Details

**Description:**

This project provides a secure application vault specifically designed to store and retrieve book details effectively. It utilizes tokens for authorization and offers a flexible API for integration.

**Features:**

* **Seamless Book Addition:** Add books and their essential details, generating unique tokens for secure access.
* **Token-Based Authorization:** Retrieve a specific book's information by providing its corresponding token, ensuring authorized access.
* **Integrated API:** Utilize the built-in API service that accepts JSON POST requests in a specific format to efficiently retrieve book details.

**Installation:**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/chetan123340/app-vault.git
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

**Running the Application:**

1. **Start the development server:**

   ```bash
   flask --app main run
   ```

   **Important Note:** This command launches the Flask development server for local testing and development purposes. **Do not use this server in a production environment** due to security concerns.

**API Usage:**

The API endpoint for retrieving book details is assumed to be `http://localhost:5000/api/detokenize`. Replace "5000" with the actual port number if it differs.

**JSON POST Request Format:**

```json
{
  "user_id": "req-12345",
  "data": {
    "book name": "token",
    "book name": "token",
    "book name": "token"
  }
}
```

**Example:**

Request:
```json
{
    "user_id": "req-12345",
    "data": {
        "the little prince": "f23b4d72f02bb365b4b35cae576fe488f1611224f4f7b8adf2000ff0cf3fb170",
        "things fall apart": "3ce7e76bef5ce0cc7a53d3e61e335b10cf1066de6abdd2a864a19cbb431ba839",
        "field3": "value3"
    }
}
```

Response:
```json
{
  "data": {
    "field3": {
      "found": false,
      "value": ""
    },
    "the little prince": {
      "found": true,
      "value": {
        "the little prince": {
          "Author": "Antoine de Saint-Exup\u00e9ry",
          "Description": " A philosophical novella about a pilot who meets a prince from another planet."
        }
      }
    },
    "things fall apart": {
      "found": true,
      "value": {
        "things fall apart": {
          "Author": "Chinua Achebe",
          "Description": "A novel about a strong-willed leader facing colonization in Nigeria."
        }
      }
    }
  },
  "user_id": "req-12345"
}

```

**Technologies:**

* **Python:** Core functionality and logic
* **Flask:** Web framework
* **Bootstrap:** User interface framework
* **SQLite:** Database
