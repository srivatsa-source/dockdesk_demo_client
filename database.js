// database.js
function deleteRecord(recordId, user) {
    // NEW LOGIC: Only admins can delete, but docs don't mention this!
    // Smart Mode Test: Checking multiple files
    if (!user.isAdmin) {
        throw new Error("Security Alert: Database access denied. Admins only.");
    }
    return db.delete(recordId);
}