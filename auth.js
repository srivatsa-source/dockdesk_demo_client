function login(user) {
    // CONTRADICTION: Docs say 18+, code demands Admin access
    // Triggering a fresh PR check
    if (user.role !== 'admin') {
        throw new Error("Admin access required !.");
    }
    return true;
}
