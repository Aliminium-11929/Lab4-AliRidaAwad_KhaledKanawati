# Lab 5 - Flask user API

This is an independent user-management API added to the Lab 4 repository. It does **not** alter the Tkinter/PyQt school-management system; it uses its own `lab5_api/database.db` SQLite file.

## Setup and run (Windows PowerShell)

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r lab5_api/requirements.txt
python -m lab5_api.app
```

If PowerShell blocks activation, use `.venv\Scripts\python.exe` in place of `python` without activating.
`sqlite3` is included in Python, so no extra database package is needed. The API listens at `http://127.0.0.1:5000`.

## Endpoints

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/users` | List users |
| GET | `/api/users/<user_id>` | Get user |
| POST | `/api/users/add` | Create user |
| PUT | `/api/users/update` | Update user |
| DELETE | `/api/users/delete/<user_id>` | Delete user |

Create and update expect JSON with `name`, `email`, `phone`, `address`, `country`; update additionally requires `user_id`. All five text fields must be nonempty. Successful creation returns HTTP 201. Missing records return 404; invalid JSON or fields return 400.

## Postman and graded exercise

Import both files in `postman/` into Postman. Select the **Flask user app - Local** environment. Use the **Flask user app** collection and send requests in this order: Add user, Get all users, Get user by ID, Update user, Get user by ID again, Delete user. The Add request saves the actual new ID as `userId` for later requests. Each request already contains a saved example response. The examples are sample snapshots, so click **Save response > Save as example** on a successful live request if the instructor wants examples captured from your own Postman run.

In the Postman collection, `{{baseUrl}}` is the environment base URL and `{{userId}}` refers to the created record. Be sure to export your collection and environment after you finish capturing live examples.

## Tests

With dependencies installed, run:

```powershell
python -m pytest lab5_api/test_api.py -v
```

The tests use a temporary SQLite database, so they do not change your real user data.

## Remaining manual steps

1. Start the Flask server and verify both GET endpoints in your browser.
2. Import, run and save live examples in Postman; export the collection and environment again if changed.
3. On GitHub, create the Lab 5 repository or use a new branch as requested in the handout. Commit database code, then the API code, and merge your branch into main after testing. GitHub actions cannot be performed from a ZIP archive alone.
4. Submit the project folder (or GitHub URL if requested), exported Postman collection, and environment according to your instructor's submission instructions. No explicit submission format is given in the handout.
