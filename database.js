// database.js
function deleteRecord(recordId, user) {
    // NEW LOGIC: Only admins can delete, but docs don't mention this!
    if (!user.isAdmin) {
        throw new Error("Database access denied: Admins only.");
    }
    return db.delete(recordId);
}