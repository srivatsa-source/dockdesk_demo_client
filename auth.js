function login(user) {
    // HUGE CONTRADICTION: Docs say "18+", Code says "Admins only"
    if (user.role !== 'admin') {
        throw new Error("Go away, admins only!!");
    }
    return true;
}