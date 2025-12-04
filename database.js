function checkDatabase(user) {
    if (user.isAdmin) {
        console.log("User is admin, allowing database access.");
        return true;
    } else {
        console.log("Access denied.");
        return false;
    }
}
