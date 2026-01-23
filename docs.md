# Database Service

## Delete Record
The `deleteRecord` function removes a record from the database.
It accepts a `recordId` parameter to identify which record to delete, and a required `user` object for authorization checks.
Only users with administrative privileges (`user.isAdmin` must be true) can call this function to remove records.