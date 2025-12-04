function login(user) {
    // CONTRADICTION: Docs say 18+, code demands Admin access
    // Smart Mode Test: Checking multiple files
    if (user.role !== 'admin') {
        throw new Error("Strict Policy: Admin access required.");
    }
    return true;
}
