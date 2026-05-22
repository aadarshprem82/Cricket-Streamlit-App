from datetime import datetime
from pathlib import Path
import shutil
import zipfile

from database.db import (
    DB_PATH,
    backup_database
)

# ==========================================
# BACKUP DIRECTORY
# ==========================================

BACKUP_DIR = Path(
    "data/backups"
)

BACKUP_DIR.mkdir(

    parents=True,

    exist_ok=True
)

# ==========================================
# GENERATE BACKUP NAME
# ==========================================

def generate_backup_filename():

    timestamp = datetime.now().strftime(

        "%Y%m%d_%H%M%S"
    )

    return (
        f"cricket_backup_"
        f"{timestamp}.db"
    )

# ==========================================
# CREATE SQLITE BACKUP
# ==========================================

def create_backup():

    filename = (
        generate_backup_filename()
    )

    backup_path = (
        BACKUP_DIR / filename
    )

    backup_database(backup_path)

    return backup_path

# ==========================================
# CREATE ZIP BACKUP
# ==========================================

def create_zip_backup():

    db_backup = create_backup()

    zip_filename = (
        str(db_backup)
        .replace(".db", ".zip")
    )

    with zipfile.ZipFile(

        zip_filename,

        "w",

        zipfile.ZIP_DEFLATED

    ) as zipf:

        zipf.write(

            db_backup,

            arcname=db_backup.name
        )

    return zip_filename

# ==========================================
# LIST BACKUPS
# ==========================================

def list_backups():

    backups = []

    for file in BACKUP_DIR.glob("*"):

        backups.append({

            "filename": file.name,

            "path": str(file),

            "size_kb": round(
                file.stat().st_size / 1024,
                2
            ),

            "created": datetime.fromtimestamp(
                file.stat().st_ctime
            )
        })

    backups.sort(

        key=lambda x: x["created"],

        reverse=True
    )

    return backups

# ==========================================
# RESTORE BACKUP
# ==========================================

def restore_backup(
    backup_file
):

    backup_path = Path(
        backup_file
    )

    if not backup_path.exists():

        raise FileNotFoundError(
            "Backup file not found."
        )

    shutil.copy2(
        backup_path,
        DB_PATH
    )

# ==========================================
# DELETE BACKUP
# ==========================================

def delete_backup(
    backup_file
):

    backup_path = Path(
        backup_file
    )

    if backup_path.exists():

        backup_path.unlink()

# ==========================================
# DELETE OLD BACKUPS
# ==========================================

def cleanup_old_backups(

    keep_latest=10
):

    backups = list_backups()

    old_backups = backups[
        keep_latest:
    ]

    for backup in old_backups:

        delete_backup(
            backup["path"]
        )

# ==========================================
# EXPORT DATABASE COPY
# ==========================================

def export_database_copy(
    export_path
):

    export_path = Path(
        export_path
    )

    export_path.parent.mkdir(

        parents=True,

        exist_ok=True
    )

    shutil.copy2(
        DB_PATH,
        export_path
    )

# ==========================================
# BACKUP DATABASE SIZE
# ==========================================

def get_database_size():

    if not DB_PATH.exists():
        return 0

    return round(

        DB_PATH.stat().st_size
        / 1024,

        2
    )

# ==========================================
# VERIFY BACKUP
# ==========================================

def verify_backup(
    backup_file
):

    backup_path = Path(
        backup_file
    )

    return backup_path.exists()

# ==========================================
# AUTOMATIC BACKUP
# ==========================================

def automatic_backup():

    backup_path = create_backup()

    cleanup_old_backups()

    return backup_path

# ==========================================
# DATABASE SNAPSHOT
# ==========================================

def create_database_snapshot():

    timestamp = datetime.now().strftime(

        "%Y%m%d_%H%M%S"
    )

    snapshot_path = (

        BACKUP_DIR

        /

        f"snapshot_{timestamp}.db"
    )

    shutil.copy2(
        DB_PATH,
        snapshot_path
    )

    return snapshot_path

# ==========================================
# COMPRESSED SNAPSHOT
# ==========================================

def create_compressed_snapshot():

    snapshot = (
        create_database_snapshot()
    )

    zip_path = str(snapshot).replace(
        ".db",
        ".zip"
    )

    with zipfile.ZipFile(

        zip_path,

        "w",

        zipfile.ZIP_DEFLATED

    ) as zipf:

        zipf.write(

            snapshot,

            arcname=snapshot.name
        )

    return zip_path

# ==========================================
# BACKUP SUMMARY
# ==========================================

def backup_summary():

    backups = list_backups()

    total_size = sum(

        backup["size_kb"]

        for backup in backups
    )

    return {

        "total_backups": len(backups),

        "database_size_kb": (
            get_database_size()
        ),

        "backup_storage_kb": round(
            total_size,
            2
        ),

        "latest_backup": (

            backups[0]["filename"]

            if backups else None
        )
    }

# ==========================================
# MANUAL EXECUTION
# ==========================================

if __name__ == "__main__":

    backup = automatic_backup()

    print(
        f"Backup created: {backup}"
    )