
# Plant Sample CRUD Application - Final Structure

## Project Files

### Core Application Files:
- **config.py** - Configuration & constants
- **database.py** - Database manager (facade pattern)
- **create.py** - CREATE operation (add_sample)
- **read.py** - READ operations (query_sample, get_all_samples)
- **update.py** - UPDATE operation (update_sample)
- **delete.py** - DELETE operation (delete_sample)
- **ui.py** - User interface (Tkinter GUI)
- **app.py** - Application entry point

### Database Files:
- **plants.sql** - Database schema and setup

---

## Architecture Overview

```
app.py (Main Entry Point)
    ↓
database.py (Database Manager)
    ├─→ create.py (INSERT)
    ├─→ read.py (SELECT)
    ├─→ update.py (UPDATE)
    └─→ delete.py (DELETE)
    ↓
ui.py (Tkinter GUI)
    ↓
config.py (Configuration)
```

---

## How to Run

```bash
python app.py
```
=======
11/12/2025 9:02:26 
Nomos69


Plant Database System Functional Requirements
--> Add data
--> Query , Update or Delete plant samples using Sample ID
--> Return the Query resukt in JSON Format
>>>>>>> 0c881aa0adbdb54f73d0b404d1ba6e346fdca876
