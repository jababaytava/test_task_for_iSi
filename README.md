
This is a simple chat API built with Django and Django REST Framework.

## Installation

1. **Clone the repository**
   ```sh
   git clone <https://github.com/jababaytava/test_task_for_iSi.git>
   cd <isi_technology_test_task>
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```sh
   python manage.py migrate
   ```
5. **Apply load db dumb**
   ```sh
   python manage.py loaddata dump.json
   ```
## API Endpoints

### Authentication
- `POST /api/token/` - Obtain access and refresh tokens.

### Threads
- `GET /chat/threads/` - List all threads.
- `POST /chat/threads/` - Create a new thread.
- `DELETE /chat/threads/{id}/` - Delete a thread.

### Messages
- `GET /chat/messages/` - List all messages in a thread.
- `POST /chat/messages/` - Send a new message.

## Notes
- The chat supports only **two participants per thread**.
- Messages are marked as **read** when retrieved by the recipient.
